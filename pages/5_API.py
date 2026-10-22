"""
pages/5_API.py — Data & API
"""

import os
from datetime import datetime
from pathlib import Path

import streamlit as st

from PIL import Image as _PILImage
_page_icon = _PILImage.open(Path(__file__).parent.parent / "static" / "icon.png")
st.set_page_config(page_title="Data & API · CDDRi", page_icon=_page_icon, layout="wide", initial_sidebar_state="collapsed")

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
.sec-label { font-size: 0.68rem; font-weight: 600; letter-spacing: 0.13em; text-transform: uppercase; color: #045C64; margin: 1rem 0 0.5rem 0; }
.field-row { display: flex; gap: 0.5rem; padding: 0.42rem 0; border-bottom: 1px solid #e8f0ef; font-size: 0.83rem; align-items: flex-start; }
.field-row:last-child { border-bottom: none; }
.field-name { font-family: 'IBM Plex Mono', monospace; font-size: 0.75rem; color: #045C64; min-width: 150px; flex-shrink: 0; }
.field-type { font-size: 0.65rem; font-weight: 600; padding: 0.1rem 0.4rem; border-radius: 3px; background: #e0f2fe; color: #0369a1; margin-right: 0.4rem; vertical-align: middle; }
.field-desc { color: #4b5563; }
code-block {
  font-family: 'IBM Plex Mono', monospace; font-size: 0.78rem; color: #1B3144;
  background: #f0f5f4; border-radius: 8px; padding: 1rem 1.2rem; line-height: 1.85;
  display: block; overflow-x: auto; margin: 0.6rem 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
  <div class="page-header-left">
    <img src="app/static/icon.png" alt="CDDRi" style="height:58px;width:auto;flex-shrink:0;">
    <span style="width:1px;height:36px;background:rgba(157,205,192,0.25);flex-shrink:0;display:inline-block;"></span>
    <span class="page-header-title">Data &amp; API</span>
    <span class="page-header-sub">Programmatic access to COMPIS data</span>
  </div>
</div>
""", unsafe_allow_html=True)
st.markdown('<div style="height:72px;"></div>', unsafe_allow_html=True)

col_l, col_r = st.columns([1, 1], gap="large")

with col_l:
    st.markdown("""
<div class="doc-card">
  <div class="card-stripe-teal"></div>
  <div style="font-size:1.1rem;font-weight:700;color:#1B3144;margin-bottom:0.9rem;">Data Access</div>
  <p style="font-size:0.85rem;color:#4b5563;line-height:1.7;margin:0 0 0.9rem 0;">
    All resource data is stored as a plain JSON file and updated weekly via GitHub Actions.
    You can load it directly in Python or download it for offline use.
  </p>
  <div class="sec-label">Load in Python</div>
  <div style="font-family:'IBM Plex Mono',monospace;font-size:0.78rem;color:#1B3144;
    background:#f0f5f4;border-radius:8px;padding:1rem 1.2rem;line-height:1.85;margin-bottom:1rem;">
    import json<br>
    from pathlib import Path<br><br>
    tools = json.loads(<br>
    &nbsp;&nbsp;(Path("data") / "tools.json").read_text()<br>
    )<br><br>
    approved = [t for t in tools<br>
    &nbsp;&nbsp;if t.get("status") == "approved"]
  </div>
  <div class="sec-label">Filter examples</div>
  <div style="font-family:'IBM Plex Mono',monospace;font-size:0.78rem;color:#1B3144;
    background:#f0f5f4;border-radius:8px;padding:1rem 1.2rem;line-height:1.85;">
    free = [t for t in tools if t.get("open_source")]<br><br>
    docking = [t for t in tools<br>
    &nbsp;&nbsp;if "Docking" in t.get("category","")]<br><br>
    recent = [t for t in tools<br>
    &nbsp;&nbsp;if (t.get("year") or 0) &gt;= 2022]
  </div>
</div>
""", unsafe_allow_html=True)

with col_r:
    st.markdown("""
<div class="doc-card">
  <div class="card-stripe-lime"></div>
  <div style="font-size:1.1rem;font-weight:700;color:#1B3144;margin-bottom:0.9rem;">JSON Schema</div>
  <p style="font-size:0.85rem;color:#4b5563;line-height:1.7;margin:0 0 0.9rem 0;">
    Each entry in <code style="background:#f0f5f4;padding:0.1rem 0.35rem;border-radius:3px;font-size:0.8rem;">tools.json</code>
    is a JSON object with the following fields:
  </p>
  <div class="sec-label" style="margin-top:0;">Fields</div>
  <div class="field-row"><div class="field-name">tool_name</div><div class="field-desc"><span class="field-type">string</span>Official tool name</div></div>
  <div class="field-row"><div class="field-name">resource_type</div><div class="field-desc"><span class="field-type">string</span>Software | Tools | Scripts | Databases | Models</div></div>
  <div class="field-row"><div class="field-name">category</div><div class="field-desc"><span class="field-type">string</span>Method category (e.g. Molecular Docking)</div></div>
  <div class="field-row"><div class="field-name">year</div><div class="field-desc"><span class="field-type">int</span>Publication year</div></div>
  <div class="field-row"><div class="field-name">authors</div><div class="field-desc"><span class="field-type">string</span>First author et al.</div></div>
  <div class="field-row"><div class="field-name">doi</div><div class="field-desc"><span class="field-type">string</span>Primary paper DOI (without https://doi.org/)</div></div>
  <div class="field-row"><div class="field-name">github</div><div class="field-desc"><span class="field-type">string</span>Full GitHub repository URL</div></div>
  <div class="field-row"><div class="field-name">key_features</div><div class="field-desc"><span class="field-type">string</span>Short description of capabilities</div></div>
  <div class="field-row"><div class="field-name">open_source</div><div class="field-desc"><span class="field-type">bool</span>True if freely available</div></div>
  <div class="field-row"><div class="field-name">license</div><div class="field-desc"><span class="field-type">string</span>License identifier (MIT, GPL-3, etc.)</div></div>
  <div class="field-row"><div class="field-name">molecule_type</div><div class="field-desc"><span class="field-type">string</span>Small molecules, Macrocycles, PROTACs, Peptides</div></div>
  <div class="field-row"><div class="field-name">status</div><div class="field-desc"><span class="field-type">string</span>approved | pending | rejected</div></div>
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
