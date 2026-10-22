"""
app.py — Single-page home + About / Docs / API / Cite / Feedback sections
"""

import html as _html
import json
import os
from datetime import datetime
from pathlib import Path

import streamlit as st

from PIL import Image as _PILImage
_page_icon = _PILImage.open(Path(__file__).parent / "static" / "icon.png")

from views.pipeline import render as _render_pipeline
from views.tools import render as _render_tools

st.set_page_config(
    page_title="CDDRi · Computational Drug Discovery Resource Index",
    page_icon=_page_icon, layout="wide",
    initial_sidebar_state="expanded",
)

VERSION     = "v2.0"
_NAVY       = "#1B3144"
_DARK_TEAL  = "#045C64"
_TEAL       = "#4C979F"
_LIGHT_TEAL = "#9DCDC0"
_LIME       = "#A7C947"

# ── Session-visit counter (counts unique browser sessions, not reruns) ─────────
_pv_file = Path(__file__).parent / "data" / "pageviews.json"
try:
    if "counted_visit" not in st.session_state:
        st.session_state.counted_visit = True
        _pv = json.loads(_pv_file.read_text()) if _pv_file.exists() else {"views": 0}
        _pv["views"] = _pv.get("views", 0) + 1
        _pv_file.write_text(json.dumps(_pv))
    _pv = json.loads(_pv_file.read_text()) if _pv_file.exists() else {"views": 0}
    _views = f"{_pv['views']:,}"
except Exception:
    _views = "—"

# ── Last-updated from tools.json mtime ───────────────────────────────────────
_tools_file = Path(__file__).parent / "data" / "tools.json"
try:
    _last_updated = datetime.fromtimestamp(
        os.path.getmtime(str(_tools_file))
    ).strftime("%d %b %Y")
except Exception:
    _last_updated = "2025"

# ── Section routing (URL query params keep back/forward working) ──────────────
_VALID = {"home", "about", "docs", "api", "cite", "feedback", "pipeline", "tools"}
_url_sec = st.query_params.get("section", "home")
if _url_sec not in _VALID:
    _url_sec = "home"
if "section" not in st.session_state or st.session_state.section != _url_sec:
    st.session_state.section = _url_sec
section = st.session_state.section

# ══════════════════════════════════════════════════════════════════════════════
# CSS — shared across all sections
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');
html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif !important; }

[data-testid="stToolbar"]        { display: none !important; }
[data-testid="stDecoration"]     { display: none !important; }
[data-testid="stStatusWidget"]   { display: none !important; }
footer    { display: none !important; }
#MainMenu { display: none !important; }
header    { display: none !important; }

[data-testid="stAppViewContainer"],
section[data-testid="stMain"],
.main { background: #eef5f4 !important; }

/* ── Left sidebar ── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg,#071520 0%,#0b2535 60%,#093540 100%) !important;
  border-right: 1px solid rgba(76,151,159,0.2) !important;
  min-width: 220px !important;
  max-width: 220px !important;
}
[data-testid="stSidebarContent"] { padding: 0 !important; }
[data-testid="stSidebar"] .stButton { margin: 0 !important; }
[data-testid="stSidebar"] .stButton > button {
  width: 100% !important; text-align: left !important;
  justify-content: flex-start !important;
  background: transparent !important; border: none !important;
  border-left: 3px solid transparent !important;
  border-radius: 0 !important; box-shadow: none !important;
  color: #9DCDC0 !important; padding: 0.6rem 1rem 0.6rem 1.1rem !important;
  font-size: 0.93rem !important; font-weight: 500 !important;
  min-height: unset !important; transition: background 0.12s, color 0.12s !important;
}
[data-testid="stSidebar"] .stButton > button p,
[data-testid="stSidebar"] .stButton > button div,
[data-testid="stSidebar"] .stButton > button span {
  text-align: left !important; width: 100% !important; display: block !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
  background: rgba(255,255,255,0.07) !important;
  color: #ffffff !important;
  border-left-color: rgba(76,151,159,0.4) !important;
}
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
  background: rgba(4,92,100,0.35) !important;
  color: #e8f4f2 !important;
  border-left-color: #4C979F !important;
  font-weight: 700 !important;
}

/* ── Fixed footer ── */
.page-footer {
  position: fixed; bottom: 0; left: 0; right: 0; z-index: 9999;
  background: linear-gradient(145deg, #1B3144 0%, #045C64 100%);
  padding: 0.8rem 2rem;
  display: flex; justify-content: space-between; align-items: center;
  font-size: 0.92rem; color: #9DCDC0;
}
.page-footer .footer-left {
  display: flex; align-items: center; gap: 1.25rem;
}
.sep { color: #1e5050; }

/* ── Section page cards ── */
.doc-grid-2 {
  display: grid; grid-template-columns: 1fr 1fr; gap: 0.85rem; margin-bottom: 0.85rem;
}
.doc-grid-14-1 {
  display: grid; grid-template-columns: 1.4fr 1fr; gap: 0.85rem; margin-bottom: 0.85rem;
}
.doc-sec-head {
  font-size: 1.0rem; font-weight: 700; color: #1B3144;
  margin: 1.1rem 0 0.6rem 0; padding-top: 0.5rem;
  border-top: 1px solid #c5ddd9;
}
.doc-card {
  background: #ffffff; border: 1px solid #c5ddd9; border-radius: 10px;
  padding: 1rem 1.2rem 0.9rem; margin-bottom: 0;
  box-shadow: 0 1px 8px rgba(4,92,100,0.07);
  display: flex; flex-direction: column;
}
.card-stripe-teal { height: 3px; background: linear-gradient(90deg, #1B3144, #045C64); margin: -1rem -1.2rem 0.75rem; border-radius: 10px 10px 0 0; }
.card-stripe-lime { height: 3px; background: linear-gradient(90deg, #A7C947, #045C64); margin: -1rem -1.2rem 0.75rem; border-radius: 10px 10px 0 0; }
.card-title { font-size: 1.02rem; font-weight: 700; color: #1B3144; margin-bottom: 0.5rem; }
.sec-label {
  font-size: 0.62rem; font-weight: 700; letter-spacing: 0.13em; text-transform: uppercase;
  color: #045C64; margin: 0.65rem 0 0.28rem 0;
}
.step {
  display: flex; gap: 0.55rem; padding: 0.32rem 0;
  border-bottom: 1px solid #e8f0ef; font-size: 0.86rem;
}
.step:last-child { border-bottom: none; }
.step-num {
  background: #045C64; color: #fff; font-size: 0.6rem; font-weight: 700;
  border-radius: 50%; width: 1.25rem; height: 1.25rem; min-width: 1.25rem;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0; margin-top: 0.08rem;
}
.step-text { color: #374151; line-height: 1.45; }
.step-text strong { color: #1B3144; }
.field-row {
  display: flex; gap: 0.5rem; padding: 0.26rem 0;
  border-bottom: 1px solid #e8f0ef; font-size: 0.84rem; align-items: flex-start;
}
.field-row:last-child { border-bottom: none; }
.field-name { font-family: 'IBM Plex Mono', monospace; font-size: 0.74rem; color: #045C64; min-width: 118px; flex-shrink: 0; }
.field-type {
  font-size: 0.62rem; font-weight: 600; padding: 0.08rem 0.32rem; border-radius: 3px;
  background: #e0f2fe; color: #0369a1; margin-right: 0.35rem; white-space: nowrap;
}
.field-desc { color: #4b5563; font-size: 0.84rem; }
.detail-row {
  display: flex; gap: 0.5rem; padding: 0.28rem 0;
  border-bottom: 1px solid #e8f0ef; font-size: 0.88rem; align-items: flex-start;
}
.detail-row:last-child { border-bottom: none; }
.detail-key { font-weight: 500; color: #374151; min-width: 200px; flex-shrink: 0; }
.detail-val { color: #4b5563; }
.badge-row {
  display: flex; gap: 0.55rem; padding: 0.2rem 0;
  border-bottom: 1px solid #e8f0ef; align-items: center;
}
.badge-row:last-child { border-bottom: none; }
.badge-desc { font-size: 0.83rem; color: #4b5563; }
.cite-block {
  font-family: 'IBM Plex Mono', monospace; font-size: 0.8rem; color: #1B3144;
  background: #f0f5f4; border-left: 3px solid #045C64; border-radius: 0 6px 6px 0;
  padding: 0.6rem 0.9rem; line-height: 1.75; margin: 0.3rem 0 0.75rem 0;
}
.fb-row {
  display: flex; gap: 0.5rem; padding: 0.32rem 0;
  border-bottom: 1px solid #e8f0ef; align-items: flex-start;
}
.fb-row:last-child { border-bottom: none; }
.fb-text { font-size: 0.86rem; color: #374151; line-height: 1.5; }
.fb-text strong { color: #1B3144; display: block; margin-bottom: 0.08rem; }
.fb-text a { color: #045C64; text-decoration: none; }
.rtype-badge {
  display: inline-block; font-size: 0.7rem; font-weight: 600;
  letter-spacing: 0.06em; text-transform: uppercase;
  padding: 0.18rem 0.55rem; border-radius: 3px; margin-right: 0.35rem;
}
.rtype-Software  { background: #e0f2fe; color: #0369a1; }
.rtype-Tools     { background: #dcfce7; color: #15803d; }
.rtype-Scripts   { background: #fef9c3; color: #854d0e; }
.rtype-Databases { background: #f3e8ff; color: #7e22ce; }
.rtype-Models    { background: #fee2e2; color: #b91c1c; }
</style>
""", unsafe_allow_html=True)

# ── Page layout CSS — unified for all sections ────────────────────────────────
st.markdown("""
<style>
html, body { overflow-x: hidden; overflow-y: auto; margin: 0; padding: 0; }
.block-container {
  padding: 0 2rem 80px 2rem !important;
  max-width: 100% !important;
  width: 100% !important;
  margin: 0 !important;
}
[data-testid="stSidebar"] > div:first-child { padding-bottom: 86px !important; }
.feature-card {
  background: #ffffff; border: 1px solid #c5ddd9; border-radius: 12px;
  overflow: hidden; box-shadow: 0 2px 14px rgba(4,92,100,0.09);
  display: flex; flex-direction: column; margin-bottom: 0.6rem;
}
.card-stripe     { height: 4px; flex-shrink: 0; }
.pipeline-stripe { background: linear-gradient(90deg, #1B3144, #045C64); }
.tools-stripe    { background: linear-gradient(90deg, #A7C947, #045C64); }
.card-body       { padding: 1.6rem 2rem 1.4rem; display: flex; flex-direction: column; }
.card-header     { display: flex; align-items: center; gap: 0.7rem; margin-bottom: 0.7rem; }
.card-title      { font-size: 1.2rem; font-weight: 600; color: #1B3144; margin: 0; }
.card-desc       { font-size: 1.0rem; color: #4b5563; line-height: 1.7; margin: 0 0 0.8rem 0; }
.card-list       { list-style: none; padding: 0; margin: 0; }
.card-list li    { font-size: 0.95rem; color: #374151; padding: 0.3rem 0;
                   border-bottom: 1px solid #e8f0ef;
                   display: flex; align-items: flex-start; gap: 0.4rem; }
.card-list li:last-child             { border-bottom: none; }
.card-list li::before                { font-weight: 700; flex-shrink: 0; content: '›'; margin-top:1px; }
.pipeline-card .card-list li::before { color: #045C64; }
.tools-card    .card-list li::before { color: #A7C947; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
_BG = "linear-gradient(135deg,#071520 0%,#0b2535 40%,#093540 100%)"

_LOGO_BRAND = (
    '<div style="display:flex;align-items:center;flex-shrink:0;">'
    '<img src="app/static/icon.png" alt="CDDRi icon" '
    'style="height:64px;width:auto;flex-shrink:0;">'
    '</div>'
)

# ── Left sidebar navigation ────────────────────────────────────────────────────
_SIDEBAR_NAV = [
    ("Home",                   "home"),
    ("Drug Discovery Pipeline","pipeline"),
    ("Method & Tools",         "tools"),
    ("Documentation",          "docs"),
    ("Feedback",               "feedback"),
]

with st.sidebar:
    st.markdown("""
<div style="padding:1.2rem 1rem 1rem;border-bottom:1px solid rgba(76,151,159,0.2);
  margin-bottom:0.25rem;display:flex;flex-direction:column;align-items:center;text-align:center;">
  <img src="app/static/icon.png" style="height:48px;width:auto;margin-bottom:0.6rem;display:block;">
  <div style="font-size:1.0rem;font-weight:800;letter-spacing:0.22em;text-transform:uppercase;
    color:#A7C947;margin-bottom:0.35rem;text-shadow:0 0 18px rgba(167,201,71,0.4);">CDDRi</div>
  <div style="font-size:0.78rem;font-weight:600;color:#fff;line-height:1.35;margin-bottom:0.18rem;">
    Computational Drug Discovery
  </div>
  <div style="font-size:0.78rem;font-weight:600;color:#4CC9C0;line-height:1.35;">
    Resource Index
  </div>
</div>
<div style="padding:0.6rem 1rem 0.15rem;font-size:0.58rem;font-weight:700;
  letter-spacing:0.14em;text-transform:uppercase;color:#4C979F;">
  Navigate
</div>
""", unsafe_allow_html=True)
    for _label, _key in _SIDEBAR_NAV:
        _active = section == _key
        if st.button(_label, key=f"sb_{_key}",
                     type="primary" if _active else "secondary",
                     width='stretch'):
            st.session_state.section = _key
            st.query_params["section"] = _key
            st.rerun()
    st.markdown(
        '<div style="margin:0.5rem 0 0;padding:0.8rem 1rem 0.7rem;'
        'border-top:1px solid rgba(76,151,159,0.18);">'
        '<div style="font-size:0.56rem;font-weight:700;letter-spacing:0.13em;'
        'text-transform:uppercase;color:#4C979F;margin-bottom:0.22rem;">Page Views</div>'
        f'<div style="font-size:1.05rem;font-weight:700;color:#e8f4f2;">{_views}</div>'
        '</div>',
        unsafe_allow_html=True,
    )

# ── Fixed header — compact dark two-line title, same on ALL pages ─────────────
# Dark bg strip extends to left:0 (behind sidebar) for seamless full-width look.
# Content starts at left:220px so it's visible in the content area.
_header_bg = (
    f'<div style="position:fixed;top:0;left:0;right:0;height:115px;'
    f'z-index:9996;background:{_BG};"></div>'
)
_header_content = (
    f'<div style="position:fixed;top:0;left:220px;right:0;z-index:9998;'
    f'background:{_BG};padding:1.8rem 2rem;'
    'box-shadow:0 4px 28px rgba(0,0,0,0.45);">'
    '<div style="font-size:1.6rem;font-weight:800;color:#fff;'
    'line-height:1.08;letter-spacing:-0.02em;">'
    'Computational Drug Discovery'
    '</div>'
    '<div style="font-size:1.6rem;font-weight:800;color:#4CC9C0;'
    'line-height:1.08;margin-top:0.1rem;">'
    'Resource Index'
    '</div>'
    '</div>'
)
st.markdown(_header_bg + _header_content, unsafe_allow_html=True)

# ── Section heading merged with header-clearance spacer ───────────────────────
# Title is anchored to the bottom of the spacer so no extra white gap appears.
_section_headings = {
    "pipeline": "Drug Discovery Pipeline",
    "tools":    "Method & Tools",
    "docs":     "Documentation",
    "feedback": "Feedback",
}
if section in _section_headings:
    st.markdown(
        f'<div style="position:relative;height:118px;margin-bottom:0.75rem;">'
        f'<h1 style="position:absolute;bottom:0;left:0;right:0;'
        f'font-size:1.45rem;font-weight:700;color:#1B3144;'
        f'margin:0;padding-bottom:0.4rem;'
        f'border-bottom:2px solid #c5ddd9;line-height:1.2;">'
        f'{_section_headings[section]}</h1>'
        f'</div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown('<div style="height:118px;"></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# CONTENT
# ══════════════════════════════════════════════════════════════════════════════
if section == "home":
    st.markdown("""
<div style="margin-bottom:1.4rem;">
  <div style="font-size:1.35rem;font-weight:700;color:#1B3144;line-height:1.2;margin-bottom:0.4rem;">
    Computational Drug Discovery Resource Index
  </div>
  <div style="font-size:0.95rem;color:#4b5563;line-height:1.65;max-width:860px;">
    An open, curated indexing directory of computational tools, AI protein prediction models,
    molecular docking engines, cheminformatics libraries, and ADMET predictors.
  </div>
</div>
""", unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
<div class="feature-card pipeline-card">
  <div class="card-stripe pipeline-stripe"></div>
  <div class="card-body">
    <div class="card-header">
      <span class="card-title">Drug Discovery Pipeline</span>
    </div>
    <p class="card-desc">Navigate tools organised by workflow stage — from
    target identification through to lead optimisation and ADMET. Each stage
    links directly to curated, filtered tool lists.</p>
    <ul class="card-list">
      <li>Target identification &amp; structure prediction</li>
      <li>Hit identification &amp; virtual screening</li>
      <li>Hit expansion &amp; generative design</li>
      <li>Lead generation &amp; free energy calculations</li>
      <li>Lead optimisation &amp; ADMET prediction</li>
      <li>Analysis, visualisation &amp; cheminformatics</li>
    </ul>
  </div>
</div>""", unsafe_allow_html=True)
        if st.button("Explore Pipeline \u2192", key="home_to_pipeline",
                     use_container_width=True, type="primary"):
            st.session_state.section = "pipeline"
            st.query_params["section"] = "pipeline"
            st.rerun()

    with col2:
        st.markdown("""
<div class="feature-card tools-card">
  <div class="card-stripe tools-stripe"></div>
  <div class="card-body">
    <div class="card-header">
      <span class="card-title">Method &amp; Tools</span>
    </div>
    <p class="card-desc">Search and filter the complete index by resource type,
    category, year, molecule type or access model. Includes a guided Tool
    Finder to match resources to your research goal.</p>
    <ul class="card-list">
      <li>346+ entries across 53 categories</li>
      <li>Filter by Software, Tools, Databases &amp; Models</li>
      <li>DOI links, GitHub repositories, license info</li>
      <li>Guided Tool Finder by research goal</li>
      <li>Inline curation &amp; expert review workflow</li>
      <li>Statistics &amp; publication trends</li>
    </ul>
  </div>
</div>""", unsafe_allow_html=True)
        if st.button("Browse Resources \u2192", key="home_to_tools",
                     use_container_width=True, type="primary"):
            st.session_state.section = "tools"
            st.query_params["section"] = "tools"
            st.rerun()
elif section == "docs":
    st.markdown("""
<!-- ── Resource Index ── -->
<div class="doc-grid-2">
  <div class="doc-card">
    <div class="card-stripe-teal"></div>
    <div class="card-title">Resource Index</div>
    <p style="font-size:0.88rem;color:#4b5563;line-height:1.6;margin:0 0 0.6rem 0;">
      A curated, continuously updated directory of open-source software, tools, databases,
      and predictive models for computational drug discovery — covering small molecules,
      macrocycles, PROTACs, and cyclic peptides.
    </p>
    <div class="sec-label">Journals Monitored</div>
    <div style="font-size:0.84rem;color:#4b5563;line-height:1.85;">
      J. Chem. Inf. Model. &nbsp;·&nbsp; J. Cheminformatics &nbsp;·&nbsp; J. Medicinal Chemistry<br>
      Mol. Informatics &nbsp;·&nbsp; J. Chem. Theory Comput. &nbsp;·&nbsp; Bioinformatics<br>
      Brief. Bioinformatics &nbsp;·&nbsp; Chemical Science &nbsp;·&nbsp; Sci. Reports<br>
      Nat. Machine Intelligence &nbsp;·&nbsp; ACS Med. Chem. Lett.
    </div>
  </div>
  <div class="doc-card">
    <div class="card-stripe-lime"></div>
    <div class="card-title">Classification</div>
    <p style="font-size:0.88rem;color:#4b5563;line-height:1.6;margin:0 0 0.55rem 0;">
      Each resource is assigned one of five types to aid filtering and discovery.
    </p>
    <div class="badge-row"><span class="rtype-badge rtype-Software">Software</span><span class="badge-desc">Simulation &amp; docking engines</span></div>
    <div class="badge-row"><span class="rtype-badge rtype-Tools">Tools</span><span class="badge-desc">Design &amp; analysis tools</span></div>
    <div class="badge-row"><span class="rtype-badge rtype-Scripts">Scripts</span><span class="badge-desc">Cheminformatics libraries &amp; scripts</span></div>
    <div class="badge-row"><span class="rtype-badge rtype-Databases">Databases</span><span class="badge-desc">Benchmark &amp; reference datasets</span></div>
    <div class="badge-row"><span class="rtype-badge rtype-Models">Models</span><span class="badge-desc">Predictive ML &amp; AI models</span></div>
  </div>
</div>

<!-- ── Using the Index ── -->
<div class="doc-sec-head">Using the Index</div>
<div class="doc-grid-2">
  <div class="doc-card">
    <div class="card-stripe-teal"></div>
    <div class="card-title">Drug Discovery Pipeline</div>
    <p style="font-size:0.88rem;color:#4b5563;line-height:1.6;margin:0 0 0.5rem 0;">
      Resources are organised by workflow stage — from target identification through to
      lead optimisation and ADMET. Click any stage tab to filter tools to that phase.
    </p>
    <div class="sec-label">Pipeline Stages</div>
    <div class="step"><div class="step-num">1</div><div class="step-text"><strong>Target Identification</strong> — protein structure prediction, binding site detection, homology modelling</div></div>
    <div class="step"><div class="step-num">2</div><div class="step-text"><strong>Hit Identification</strong> — molecular docking, virtual screening, pharmacophore search</div></div>
    <div class="step"><div class="step-num">3</div><div class="step-text"><strong>Hit Expansion</strong> — fragment growing, generative design, macrocycles, PROTACs</div></div>
    <div class="step"><div class="step-num">4</div><div class="step-text"><strong>Lead Generation</strong> — molecular dynamics, free energy perturbation, binding affinity prediction</div></div>
    <div class="step"><div class="step-num">5</div><div class="step-text"><strong>Lead Optimisation</strong> — ADMET prediction, SAR analysis, retrosynthesis planning</div></div>
    <div class="step"><div class="step-num">6</div><div class="step-text"><strong>Analysis &amp; Visualisation</strong> — cheminformatics, interaction analysis, reporting</div></div>
    <div class="sec-label">Search &amp; Filters</div>
    <p style="font-size:0.86rem;color:#4b5563;line-height:1.55;margin:0;">
      Use the <strong>Search</strong> box to match names, descriptions, or authors.
      Filter by <strong>Open Source</strong> status, <strong>Molecule type</strong>, or <strong>Category</strong>.
    </p>
  </div>
  <div class="doc-card">
    <div class="card-stripe-lime"></div>
    <div class="card-title">Method &amp; Tools Browser</div>
    <p style="font-size:0.88rem;color:#4b5563;line-height:1.6;margin:0 0 0.5rem 0;">
      The <strong>Method &amp; Tools</strong> page provides the full index with advanced
      filters, a detail panel for each entry, and a guided Tool Finder.
    </p>
    <div class="sec-label">Tabs</div>
    <div class="step"><div class="step-num">1</div><div class="step-text"><strong>Browse Resources</strong> — search and filter all 346+ entries by type, category, year, molecule type, or access model</div></div>
    <div class="step"><div class="step-num">2</div><div class="step-text"><strong>Resource Detail</strong> — click any row to view full metadata, DOI, GitHub repository, license, and key features</div></div>
    <div class="step"><div class="step-num">3</div><div class="step-text"><strong>Tool Finder</strong> — answer guided questions to receive a personalised tool recommendation</div></div>
    <div class="sec-label">Entry Fields</div>
    <div class="field-row"><div class="field-name">tool_name</div><div class="field-desc">Official name as published</div></div>
    <div class="field-row"><div class="field-name">resource_type</div><div class="field-desc">Software · Tools · Scripts · Databases · Models</div></div>
    <div class="field-row"><div class="field-name">category</div><div class="field-desc">Method category (e.g. Molecular Docking)</div></div>
    <div class="field-row"><div class="field-name">year</div><div class="field-desc">Publication year</div></div>
    <div class="field-row"><div class="field-name">doi</div><div class="field-desc">Primary paper DOI</div></div>
    <div class="field-row"><div class="field-name">github</div><div class="field-desc">Repository URL</div></div>
    <div class="field-row"><div class="field-name">molecule_type</div><div class="field-desc">Small molecules · Macrocycles · PROTACs · Peptides</div></div>
    <div class="field-row"><div class="field-name">open_source</div><div class="field-desc">True / False</div></div>
  </div>
</div>

<!-- ── API & Data ── -->
<div class="doc-sec-head">API &amp; Data</div>
<div class="doc-grid-2">
  <div class="doc-card">
    <div class="card-stripe-teal"></div>
    <div class="card-title">Data Access</div>
    <p style="font-size:0.88rem;color:#4b5563;line-height:1.6;margin:0 0 0.5rem 0;">
      All resource data is stored as a plain JSON file and refreshed regularly via GitHub Actions.
      Load it directly in Python or download it for offline use.
    </p>
    <div class="sec-label">Load in Python</div>
    <div style="font-family:'IBM Plex Mono',monospace;font-size:0.8rem;color:#1B3144;
      background:#f0f5f4;border-radius:7px;padding:0.65rem 0.9rem;line-height:1.85;margin-bottom:0.6rem;">
      import json<br>from pathlib import Path<br><br>
      tools = json.loads(<br>&nbsp;&nbsp;(Path("data") / "tools.json").read_text()<br>)<br><br>
      approved = [t for t in tools<br>&nbsp;&nbsp;if t.get("status") == "approved"]
    </div>
    <div class="sec-label">Filter Examples</div>
    <div style="font-family:'IBM Plex Mono',monospace;font-size:0.8rem;color:#1B3144;
      background:#f0f5f4;border-radius:7px;padding:0.65rem 0.9rem;line-height:1.85;">
      free = [t for t in tools if t.get("open_source")]<br><br>
      docking = [t for t in tools<br>&nbsp;&nbsp;if "Docking" in t.get("category","")]<br><br>
      recent = [t for t in tools<br>&nbsp;&nbsp;if (t.get("year") or 0) &gt;= 2022]
    </div>
  </div>
  <div class="doc-card">
    <div class="card-stripe-lime"></div>
    <div class="card-title">JSON Schema</div>
    <p style="font-size:0.88rem;color:#4b5563;line-height:1.6;margin:0 0 0.5rem 0;">
      Each entry in <code style="background:#f0f5f4;padding:0.08rem 0.3rem;border-radius:3px;font-size:0.8rem;">tools.json</code>
      is a JSON object with the following fields:
    </p>
    <div class="sec-label" style="margin-top:0.3rem;">Fields</div>
    <div class="field-row"><div class="field-name">tool_name</div><div class="field-desc"><span class="field-type">string</span>Official tool name</div></div>
    <div class="field-row"><div class="field-name">resource_type</div><div class="field-desc"><span class="field-type">string</span>Software | Tools | Scripts | Databases | Models</div></div>
    <div class="field-row"><div class="field-name">category</div><div class="field-desc"><span class="field-type">string</span>Method category (e.g. Molecular Docking)</div></div>
    <div class="field-row"><div class="field-name">year</div><div class="field-desc"><span class="field-type">int</span>Publication year</div></div>
    <div class="field-row"><div class="field-name">authors</div><div class="field-desc"><span class="field-type">string</span>First author et al.</div></div>
    <div class="field-row"><div class="field-name">doi</div><div class="field-desc"><span class="field-type">string</span>DOI (without https://doi.org/ prefix)</div></div>
    <div class="field-row"><div class="field-name">github</div><div class="field-desc"><span class="field-type">string</span>Full GitHub repository URL</div></div>
    <div class="field-row"><div class="field-name">key_features</div><div class="field-desc"><span class="field-type">string</span>Short description of capabilities</div></div>
    <div class="field-row"><div class="field-name">open_source</div><div class="field-desc"><span class="field-type">bool</span>True if freely available</div></div>
    <div class="field-row"><div class="field-name">license</div><div class="field-desc"><span class="field-type">string</span>License identifier (MIT, GPL-3.0, etc.)</div></div>
    <div class="field-row"><div class="field-name">molecule_type</div><div class="field-desc"><span class="field-type">string</span>Small molecules, Macrocycles, PROTACs, Peptides</div></div>
    <div class="field-row"><div class="field-name">status</div><div class="field-desc"><span class="field-type">string</span>approved | pending | rejected</div></div>
  </div>
</div>

""", unsafe_allow_html=True)

elif section == "feedback":
    st.markdown("""
<div class="doc-grid-2">
  <div class="doc-card">
    <div class="card-stripe-teal"></div>
    <div class="card-title">How to Contribute</div>
    <p style="font-size:0.88rem;color:#4b5563;line-height:1.55;margin:0 0 0.5rem 0;">
      COMPIS is a community resource. We welcome suggestions for new tools, corrections
      to existing entries, and feedback on the interface or content.
    </p>
    <div class="sec-label" style="margin-top:0.1rem;">Ways to contribute</div>
    <div class="fb-row">
      <div class="fb-text"><strong>Suggest a new tool</strong>
        Send the tool name, GitHub URL, and primary DOI to
        <a href="mailto:vasanthanathan.poongavanam@scilifelab.se">vasanthanathan.poongavanam@scilifelab.se</a>.
        We will review and add it to the Pending Review queue.
      </div>
    </div>
    <div class="fb-row">
      <div class="fb-text"><strong>Correct an entry</strong>
        If you spot an error in a tool's metadata (wrong category, outdated link, incorrect license),
        email us with the tool name and the correction.
      </div>
    </div>
    <div class="fb-row">
      <div class="fb-text"><strong>General feedback</strong>
        Feature requests, usability issues, or ideas for new pipeline stages or categories
        are welcome. Email or reach out via the SciLifeLab COMPIS network.
      </div>
    </div>
    <div class="fb-row">
      <div class="fb-text"><strong>Collaboration</strong>
        Interested in joining COMPIS or contributing to joint technology development?
        Contact the COMPIS coordination team at SciLifeLab.
      </div>
    </div>
  </div>
  <div class="doc-card">
    <div class="card-stripe-lime"></div>
    <div class="card-title">Contact</div>
    <div style="font-size:0.9rem;color:#4b5563;line-height:1.8;margin-top:0.3rem;">
      <strong style="color:#1B3144;font-size:0.98rem;">Vasanthanathan Poongavanam</strong><br>
      Drug Discovery and Development Platform<br>
      Uppsala University<br>
      SciLifeLab &nbsp;&middot;&nbsp; COMPIS<br>
      <a href="mailto:vasanthanathan.poongavanam@scilifelab.se"
         style="color:#045C64;text-decoration:none;font-weight:500;font-size:0.86rem;">
        vasanthanathan.poongavanam@scilifelab.se
      </a>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

elif section == "pipeline":
    _render_pipeline()

elif section == "tools":
    _render_tools()


# ══════════════════════════════════════════════════════════════════════════════
# FOOTER — fixed, full-width, multi-column dark design, same on all pages.
# Background extends left:0 (aligns with/behind sidebar) for a seamless look.
# Content starts at margin-left:220px (visible in the content area).
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div style="position:fixed;bottom:0;left:0;right:0;z-index:9996;
  background:linear-gradient(135deg,#071520 0%,#0b2535 100%);
  border-top:1px solid rgba(76,151,159,0.18);">
  <div style="margin-left:220px;padding:0.32rem 1.5rem 0.28rem;">
    <div style="display:grid;grid-template-columns:2fr 1.2fr 1.2fr;gap:1.8rem;align-items:center;">
      <div style="display:flex;align-items:center;gap:0.55rem;">
        <div style="width:22px;height:22px;background:#045C64;border-radius:4px;
          display:flex;align-items:center;justify-content:center;
          font-size:0.72rem;font-weight:800;color:#fff;flex-shrink:0;">C</div>
        <div>
          <div style="font-size:0.76rem;font-weight:700;color:#fff;line-height:1.2;">
            COMPIS — SciLifeLab Platform</div>
          <div style="font-size:0.59rem;color:#4C979F;">
            Computational Drug Discovery Infrastructure</div>
        </div>
      </div>
      <div>
        <div style="font-size:0.53rem;font-weight:700;letter-spacing:0.13em;text-transform:uppercase;
          color:#4C979F;margin-bottom:0.3rem;">Platform Resources</div>
        <ul style="list-style:none;padding:0;margin:0;">
          <li style="padding:0.1rem 0;border-bottom:1px solid rgba(76,151,159,0.12);">
            <a href="https://www.scilifelab.se" target="_blank"
               style="color:#9DCDC0;text-decoration:none;font-size:0.7rem;">
              &rsaquo; SciLifeLab Official Portal</a></li>
          <li style="padding:0.1rem 0;">
            <a href="https://www.scilifelab.se/units/ddd-platform/" target="_blank"
               style="color:#9DCDC0;text-decoration:none;font-size:0.7rem;">
              &rsaquo; DDD Platform Units</a></li>
        </ul>
      </div>
      <div>
        <div style="font-size:0.53rem;font-weight:700;letter-spacing:0.13em;text-transform:uppercase;
          color:#4C979F;margin-bottom:0.3rem;">Community &amp; Contact</div>
        <p style="font-size:0.7rem;color:#9DCDC0;line-height:1.45;margin:0 0 0.38rem 0;">
          Have a tool, database, or ML model to include?
        </p>
        <a href="mailto:vasanthanathan.poongavanam@scilifelab.se?subject=Submit Tool for CDDRi"
           style="display:inline-block;background:#045C64;color:#fff;
             padding:0.22rem 0.55rem;border-radius:4px;font-size:0.68rem;
             font-weight:600;text-decoration:none;">
          Submit a Tool
        </a>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
