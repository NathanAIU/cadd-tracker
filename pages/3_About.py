"""
pages/3_About.py — About this resource
SciLifeLab Computational Drug Discovery Resource Index
"""

import os
from datetime import datetime
from pathlib import Path

import streamlit as st

from PIL import Image as _PILImage
_page_icon = _PILImage.open(Path(__file__).parent.parent / "static" / "icon.png")
st.set_page_config(
    page_title="About · CDDRi",
    page_icon=_page_icon, layout="wide",
    initial_sidebar_state="collapsed",
)

_NAVY      = "#1B3144"
_DARK_TEAL = "#045C64"
_TEAL      = "#4C979F"
_LIGHT_TEAL= "#9DCDC0"
_LIME      = "#A7C947"
_VERSION   = "v2.0"
_CONTACT   = "vasanthanathan.poongavanam@scilifelab.se"

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
footer    { display: none !important; }
#MainMenu { display: none !important; }
header    { display: none !important; }

[data-testid="stAppViewContainer"],
section[data-testid="stMain"],
.main { background: #eef5f4 !important; }

.block-container {
  padding: 0 2rem 4rem 2rem !important;
  max-width: 1520px !important;
  margin: 0 auto !important;
}

/* ── Fixed header ── */
.page-header {
  position: fixed; top: 0; left: 0; right: 0; z-index: 9998;
  background: linear-gradient(135deg,#071520 0%,#0b2535 40%,#093540 100%);
  padding: 0.6rem 2rem;
  display: flex; align-items: center; justify-content: space-between;
  box-shadow: 0 4px 28px rgba(0,0,0,0.45);
}
.page-header-left { display: flex; align-items: center; gap: 1rem; }
.page-header-badge {
  font-size: 0.78rem; font-weight: 600;
  letter-spacing: 0.15em; text-transform: uppercase;
  color: #A7C947; background: rgba(167,201,71,0.12);
  border: 1px solid rgba(167,201,71,0.4);
  border-radius: 99px; padding: 0.18rem 0.75rem;
}
.page-header-title { font-size: 1.45rem; font-weight: 700; color: #fff; margin: 0; }
.page-header-sub   { font-size: 0.95rem; color: #9DCDC0; margin: 0; }
.page-header-home  {
  font-size: 0.78rem; font-weight: 500;
  color: #A7C947; text-decoration: none; white-space: nowrap;
}
.page-header-home:hover { color: #ffffff; }

/* ── Fixed footer ── */
.page-footer {
  position: fixed; bottom: 0; left: 0; right: 0; z-index: 9999;
  background: linear-gradient(145deg, #1B3144 0%, #045C64 100%);
  padding: 0.75rem 2rem;
  display: flex; justify-content: space-between; align-items: center;
  font-size: 0.92rem; color: #9DCDC0;
}
.page-footer a { color: #9DCDC0; text-decoration: none; font-weight: 500; }
.page-footer a:hover { color: #ffffff; }
.sep { color: #1e5050; }

/* ── Cards ── */
.about-card {
  background: #ffffff;
  border: 1px solid #c5ddd9;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 14px rgba(4,92,100,0.09);
  padding: 1.8rem 2rem 1.6rem;
  margin-bottom: 1.25rem;
}
.card-stripe-teal { height: 4px; background: linear-gradient(90deg, #1B3144, #045C64); margin: -1.8rem -2rem 1.4rem -2rem; }
.card-stripe-lime { height: 4px; background: linear-gradient(90deg, #A7C947, #045C64); margin: -1.8rem -2rem 1.4rem -2rem; }
.sec-label {
  font-size: 0.68rem; font-weight: 600;
  letter-spacing: 0.13em; text-transform: uppercase;
  color: #045C64; margin: 1.1rem 0 0.55rem 0;
}
.detail-row {
  display: flex; gap: 0.5rem; padding: 0.35rem 0;
  border-bottom: 1px solid #e8f0ef; font-size: 0.83rem;
  align-items: flex-start;
}
.detail-row:last-child { border-bottom: none; }
.detail-key { font-weight: 500; color: #374151; min-width: 160px; flex-shrink: 0; }
.detail-val { color: #4b5563; }
.badge-row {
  display: flex; gap: 0.65rem; padding: 0.25rem 0;
  border-bottom: 1px solid #e8f0ef; align-items: center;
}
.badge-row:last-child { border-bottom: none; }
.badge-desc { font-size: 0.82rem; color: #4b5563; }
.rtype-badge {
  display: inline-block; font-size: 0.65rem; font-weight: 600;
  letter-spacing: 0.06em; text-transform: uppercase;
  padding: 0.18rem 0.55rem; border-radius: 3px;
  margin-right: 0.35rem; vertical-align: middle;
}
.rtype-Software  { background: #e0f2fe; color: #0369a1; }
.rtype-Tools     { background: #dcfce7; color: #15803d; }
.rtype-Scripts   { background: #fef9c3; color: #854d0e; }
.rtype-Databases { background: #f3e8ff; color: #7e22ce; }
.rtype-Models    { background: #fee2e2; color: #b91c1c; }
</style>
""", unsafe_allow_html=True)

# ── Fixed header ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
  <div class="page-header-left">
    <img src="app/static/icon.png" alt="CDDRi" style="height:58px;width:auto;flex-shrink:0;">
    <span style="width:1px;height:36px;background:rgba(157,205,192,0.25);flex-shrink:0;display:inline-block;"></span>
    <span class="page-header-title">About</span>
    <span class="page-header-sub">CADD Resource Index</span>
  </div>
  <a href="/" class="page-header-home">&#8592; Home</a>
</div>
""", unsafe_allow_html=True)

st.markdown('<div style="height:80px;"></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# CONTENT
# ══════════════════════════════════════════════════════════════════════════════
col_main, col_side = st.columns([2.2, 1], gap="large")

with col_main:
    st.markdown("""
<div class="about-card">
  <div class="card-stripe-teal"></div>
  <div style="font-size:1.5rem;font-weight:700;color:#1B3144;margin-bottom:0.25rem;">COMPIS</div>
  <div style="font-size:0.75rem;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;
    color:#045C64;margin-bottom:1.15rem;">
    Computational Chemistry &amp; Cheminformatics at SciLifeLab
  </div>
  <p style="color:#4b5563;font-size:0.88rem;line-height:1.75;margin:0 0 0.9rem 0;">
    Computational chemistry and cheminformatics are indispensable tools in modern early drug discovery,
    with a demonstrated track record of reducing both lead times and costs in drug development. With the
    recent advent of AI, computational chemistry has the potential to revolutionize the field further by
    accelerating hit identification, optimizing lead compounds, and enabling more accurate predictions of
    relevant properties.
  </p>
  <p style="color:#4b5563;font-size:0.88rem;line-height:1.75;margin:0 0 0.9rem 0;">
    At SciLifeLab, computational chemistry and cheminformatics are applied across multiple platforms and
    nodes, including CBGE and DDDP, with active groups in Stockholm, Uppsala, and Umeå. Computational
    chemists from these sites have now joined forces in COMPIS — <em>COMPutational chemistry and
    chemInformatics at SciLifeLab</em> — to exchange expertise on software, tools, and workflows, and to
    collaborate on joint technology development projects.
  </p>
  <p style="color:#4b5563;font-size:0.88rem;line-height:1.75;margin:0;">
    For scientists at SciLifeLab and beyond, COMPIS will serve as a central resource for computational
    chemistry expertise and support, lowering the barrier to adopting state-of-the-art methods and
    strengthening cross-disciplinary collaboration across the Swedish life science community.
  </p>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="about-card">
  <div class="card-stripe-lime"></div>
  <div class="sec-label" style="margin-top:0;">COMPIS Members</div>
  <div class="detail-row">
    <div class="detail-key">Vasanthanathan Poongavanam</div>
    <div class="detail-val">Drug Discovery and Development Platform, Uppsala University</div>
  </div>
  <div class="detail-row">
    <div class="detail-key">Flavio Ballante</div>
    <div class="detail-val">Chemical Biology Consortium Sweden, KI</div>
  </div>
  <div class="detail-row">
    <div class="detail-key">Evert J. Homan</div>
    <div class="detail-val">Chemical Biology Consortium Sweden, KI</div>
  </div>
  <div class="detail-row">
    <div class="detail-key">Chandan Kumar</div>
    <div class="detail-val">Chemical Biology Consortium Sweden, Umeå University</div>
  </div>
  <div class="detail-row">
    <div class="detail-key">Lars Sandberg</div>
    <div class="detail-val">Drug Discovery and Development Platform, Stockholm University</div>
  </div>
  <div class="detail-row">
    <div class="detail-key">Mats Dahlberg</div>
    <div class="detail-val">Chemical Biology Consortium Sweden, KI</div>
  </div>
  <div class="detail-row">
    <div class="detail-key">Safa Karagöz</div>
    <div class="detail-val">Chemical Biology Consortium Sweden, KI</div>
  </div>
</div>
""", unsafe_allow_html=True)

with col_side:
    st.markdown("""
<div class="about-card">
  <div class="card-stripe-teal"></div>

  <div class="sec-label" style="margin-top:0;">Resource Index</div>
  <p style="font-size:0.82rem;color:#4b5563;line-height:1.65;margin:0 0 1rem 0;">
    A curated, continuously updated guide to open-source software, tools, databases,
    and predictive models for computational drug discovery — covering small molecules,
    macrocycles, PROTACs, and cyclic peptides.
  </p>

  <div class="sec-label">Classification</div>
  <div class="badge-row"><span class="rtype-badge rtype-Software">Software</span><span class="badge-desc">Simulation &amp; docking engines</span></div>
  <div class="badge-row"><span class="rtype-badge rtype-Tools">Tools</span><span class="badge-desc">Design &amp; analysis tools</span></div>
  <div class="badge-row"><span class="rtype-badge rtype-Scripts">Scripts</span><span class="badge-desc">Cheminformatics libraries</span></div>
  <div class="badge-row"><span class="rtype-badge rtype-Databases">Databases</span><span class="badge-desc">Benchmark datasets</span></div>
  <div class="badge-row"><span class="rtype-badge rtype-Models">Models</span><span class="badge-desc">Predictive ML models</span></div>

  <div class="sec-label" style="margin-top:1.1rem;">Journals Monitored</div>
  <div style="font-size:0.78rem;color:#4b5563;line-height:2.0;">
    J. Chem. Inf. Model. &nbsp;·&nbsp; J. Cheminformatics<br>
    J. Medicinal Chemistry &nbsp;·&nbsp; Mol. Informatics<br>
    J. Chem. Theory Comput.<br>
    Bioinformatics &nbsp;·&nbsp; Brief. Bioinformatics<br>
    Chemical Science &nbsp;·&nbsp; Sci. Reports<br>
    Nat. Machine Intelligence &nbsp;·&nbsp; ACS Med. Chem. Lett.
  </div>

  <div class="sec-label">Contact</div>
  <div style="font-size:0.82rem;color:#4b5563;line-height:1.8;">
    <strong style="color:#1B3144;">Vasanthanathan Poongavanam</strong><br>
    SciLifeLab &nbsp;&middot;&nbsp; COMPIS<br>
    <a href="mailto:vasanthanathan.poongavanam@scilifelab.se"
       style="color:#045C64;text-decoration:none;font-size:0.78rem;">
      vasanthanathan.poongavanam@scilifelab.se
    </a>
  </div>

  <div class="sec-label">Quick Start</div>
  <div style="font-size:0.78rem;color:#4b5563;line-height:1.85;
    font-family:'IBM Plex Mono',monospace;
    background:#f0f5f4;border-radius:6px;padding:0.65rem 0.85rem;">
    pip install -r requirements.txt<br>
    streamlit run app.py
  </div>
</div>
""", unsafe_allow_html=True)

# ── Fixed footer ──────────────────────────────────────────────────────────────
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
