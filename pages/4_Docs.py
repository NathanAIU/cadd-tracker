"""
pages/4_Docs.py — Documentation
"""

import os
from datetime import datetime
from pathlib import Path

import streamlit as st

from PIL import Image as _PILImage
_page_icon = _PILImage.open(Path(__file__).parent.parent / "static" / "icon.png")
st.set_page_config(page_title="Documentation · CDDRi", page_icon=_page_icon, layout="wide", initial_sidebar_state="collapsed")

_VERSION = "v2.0"; _CONTACT = "vasanthanathan.poongavanam@scilifelab.se"

_tools_file = Path(__file__).parent.parent / "data" / "tools.json"
try:
    _last_updated = datetime.fromtimestamp(os.path.getmtime(str(_tools_file))).strftime("%d %b %Y")
except Exception:
    _last_updated = "2025"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');
html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif !important; }
html, body { overflow-x: hidden; }
[data-testid="stSidebar"]        { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stToolbar"]        { display: none !important; }
[data-testid="stDecoration"]     { display: none !important; }
[data-testid="stStatusWidget"]   { display: none !important; }
footer { display: none !important; }
#MainMenu { display: none !important; }
header { display: none !important; }
[data-testid="stAppViewContainer"], section[data-testid="stMain"], .main { background: #eef5f4 !important; }
.block-container { padding: 0 2rem 4rem 2rem !important; max-width: 1520px !important; margin: 0 auto !important; }

.page-header {
  position: fixed; top: 0; left: 0; right: 0; z-index: 9998;
  background: linear-gradient(135deg,#071520 0%,#0b2535 40%,#093540 100%);
  padding: 0.6rem 2rem; display: flex; align-items: center; justify-content: space-between;
  box-shadow: 0 4px 28px rgba(0,0,0,0.45);
}
.page-header-left { display: flex; align-items: center; gap: 1rem; }
.page-header-badge {
  font-size: 0.7rem; font-weight: 600; letter-spacing: 0.15em; text-transform: uppercase;
  color: #A7C947; background: rgba(167,201,71,0.12); border: 1px solid rgba(167,201,71,0.4);
  border-radius: 99px; padding: 0.18rem 0.75rem;
}
.page-header-title { font-size: 1.3rem; font-weight: 700; color: #fff; margin: 0; }
.page-header-sub   { font-size: 0.85rem; color: #9DCDC0; margin: 0; }
.page-footer {
  position: fixed; bottom: 0; left: 0; right: 0; z-index: 9999;
  background: linear-gradient(145deg, #1B3144 0%, #045C64 100%);
  padding: 0.75rem 2rem; display: flex; justify-content: space-between; align-items: center;
  font-size: 0.82rem; color: #9DCDC0;
}
.page-footer a { color: #9DCDC0; text-decoration: none; font-weight: 500; }
.page-footer a:hover { color: #ffffff; }
.sep { color: #1e5050; }
.doc-card {
  background: #ffffff; border: 1px solid #c5ddd9; border-radius: 12px;
  padding: 1.6rem 1.8rem 1.4rem; margin-bottom: 1.25rem;
  box-shadow: 0 2px 14px rgba(4,92,100,0.08);
}
.card-stripe-teal { height: 4px; background: linear-gradient(90deg, #1B3144, #045C64); margin: -1.6rem -1.8rem 1.3rem; }
.card-stripe-lime { height: 4px; background: linear-gradient(90deg, #A7C947, #045C64); margin: -1.6rem -1.8rem 1.3rem; }
.sec-label {
  font-size: 0.68rem; font-weight: 600; letter-spacing: 0.13em; text-transform: uppercase;
  color: #045C64; margin: 1rem 0 0.5rem 0;
}
.step { display: flex; gap: 0.75rem; padding: 0.55rem 0; border-bottom: 1px solid #e8f0ef; font-size: 0.84rem; }
.step:last-child { border-bottom: none; }
.step-num {
  background: #045C64; color: #fff; font-size: 0.65rem; font-weight: 700;
  border-radius: 50%; width: 1.4rem; height: 1.4rem; display: flex; align-items: center;
  justify-content: center; flex-shrink: 0; margin-top: 0.1rem;
}
.step-text { color: #374151; line-height: 1.5; }
.step-text strong { color: #1B3144; }
.field-row { display: flex; gap: 0.5rem; padding: 0.4rem 0; border-bottom: 1px solid #e8f0ef; font-size: 0.82rem; }
.field-row:last-child { border-bottom: none; }
.field-name { font-family: 'IBM Plex Mono', monospace; font-size: 0.75rem; color: #045C64; min-width: 140px; flex-shrink: 0; }
.field-desc { color: #4b5563; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
  <div class="page-header-left">
    <img src="app/static/icon.png" alt="CDDRi" style="height:58px;width:auto;flex-shrink:0;">
    <span style="width:1px;height:36px;background:rgba(157,205,192,0.25);flex-shrink:0;display:inline-block;"></span>
    <span class="page-header-title">Documentation</span>
    <span class="page-header-sub">How to use the resource</span>
  </div>
</div>
""", unsafe_allow_html=True)
st.markdown('<div style="height:72px;"></div>', unsafe_allow_html=True)

col_l, col_r = st.columns([1, 1], gap="large")

with col_l:
    st.markdown("""
<div class="doc-card">
  <div class="card-stripe-teal"></div>
  <div style="font-size:1.1rem;font-weight:700;color:#1B3144;margin-bottom:0.9rem;">Explore the Pipeline</div>
  <p style="font-size:0.85rem;color:#4b5563;line-height:1.7;margin:0 0 1rem 0;">
    The <strong>Drug Discovery Pipeline</strong> view organises all resources by workflow stage.
    Click any stage tab to filter tools to that phase of drug discovery.
  </p>
  <div class="sec-label">Pipeline Stages</div>
  <div class="step"><div class="step-num">1</div><div class="step-text"><strong>Target Identification</strong> — protein structure prediction, binding site detection, homology modelling</div></div>
  <div class="step"><div class="step-num">2</div><div class="step-text"><strong>Hit Identification</strong> — molecular docking, virtual screening, pharmacophore search</div></div>
  <div class="step"><div class="step-num">3</div><div class="step-text"><strong>Hit Expansion</strong> — fragment growing, generative design, macrocycles, PROTACs</div></div>
  <div class="step"><div class="step-num">4</div><div class="step-text"><strong>Lead Generation</strong> — molecular dynamics, free energy calculations, binding affinity</div></div>
  <div class="step"><div class="step-num">5</div><div class="step-text"><strong>Lead Optimisation</strong> — ADMET prediction, SAR analysis, retrosynthesis</div></div>
  <div class="step"><div class="step-num">6</div><div class="step-text"><strong>Analysis</strong> — visualisation, cheminformatics, interaction analysis</div></div>
  <div class="sec-label" style="margin-top:1.1rem;">Filters</div>
  <p style="font-size:0.83rem;color:#4b5563;line-height:1.65;margin:0;">
    Use the <strong>Search</strong> box to match tool names, features, or authors.
    Filter by <strong>Access</strong> (Free / Commercial) or <strong>Molecule type</strong>
    to narrow the list further.
  </p>
</div>
""", unsafe_allow_html=True)

with col_r:
    st.markdown("""
<div class="doc-card">
  <div class="card-stripe-lime"></div>
  <div style="font-size:1.1rem;font-weight:700;color:#1B3144;margin-bottom:0.9rem;">Browse Resources</div>
  <p style="font-size:0.85rem;color:#4b5563;line-height:1.7;margin:0 0 1rem 0;">
    The <strong>Method &amp; Tools</strong> page gives access to the full index with advanced filters,
    a detail panel for each entry, and a guided Tool Finder.
  </p>
  <div class="sec-label">Tabs</div>
  <div class="step"><div class="step-num">1</div><div class="step-text"><strong>Browse Resources</strong> — search and filter all 346+ entries by type, category, year, molecule type or access model</div></div>
  <div class="step"><div class="step-num">2</div><div class="step-text"><strong>Resource Detail</strong> — click any row to see full metadata, DOI link, GitHub, license, and key features</div></div>
  <div class="step"><div class="step-num">3</div><div class="step-text"><strong>Tool Finder</strong> — answer guided questions to get a personalised tool recommendation</div></div>
  <div class="step"><div class="step-num">4</div><div class="step-text"><strong>Pending Review</strong> — curators can approve, edit, or reject auto-discovered candidates before publication</div></div>
  <div class="sec-label" style="margin-top:1.1rem;">Tool Card Fields</div>
  <div class="field-row"><div class="field-name">tool_name</div><div class="field-desc">Official name as published</div></div>
  <div class="field-row"><div class="field-name">resource_type</div><div class="field-desc">Software · Tools · Scripts · Databases · Models</div></div>
  <div class="field-row"><div class="field-name">category</div><div class="field-desc">Detailed method category (e.g. Molecular Docking)</div></div>
  <div class="field-row"><div class="field-name">year</div><div class="field-desc">Publication year</div></div>
  <div class="field-row"><div class="field-name">doi</div><div class="field-desc">Primary paper DOI</div></div>
  <div class="field-row"><div class="field-name">github</div><div class="field-desc">GitHub repository URL</div></div>
  <div class="field-row"><div class="field-name">molecule_type</div><div class="field-desc">Small molecules · Macrocycles · PROTACs · Peptides</div></div>
  <div class="field-row"><div class="field-name">open_source</div><div class="field-desc">True / False</div></div>
</div>
""", unsafe_allow_html=True)

_footer = (
    '<div class="page-footer">'
    '<div style="display:flex;align-items:center;gap:1rem;">'
    f'<span>Updated&nbsp;<strong style="color:#e8f4f2;">{_last_updated}</strong>'
    f'&nbsp;&nbsp;<span class="sep">&middot;</span>&nbsp;&nbsp;'
    f'<strong style="color:#e8f4f2;">{_VERSION}</strong></span>'
    '<span class="sep">|</span>'
    '<a href="/" style="color:#9DCDC0;text-decoration:none;font-weight:500;">&#8592; Home</a>'
    '</div>'
    '<span style="font-size:0.72rem;font-weight:600;letter-spacing:0.13em;text-transform:uppercase;'
    'color:#A7C947;background:rgba(167,201,71,0.12);border:1px solid rgba(167,201,71,0.35);'
    'border-radius:99px;padding:0.16rem 0.7rem;">SciLifeLab &nbsp;&middot;&nbsp; COMPIS</span>'
    '</div>'
)
st.markdown(_footer, unsafe_allow_html=True)
