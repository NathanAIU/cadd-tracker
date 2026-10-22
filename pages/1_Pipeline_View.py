"""
pages/1_Pipeline_View.py — Drug Discovery Pipeline View
Visual, stage-based guide to computational drug discovery tools.
"""

import json
import html as _html
import os
import sys
from datetime import datetime
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))

# ── Page config ───────────────────────────────────────────────────────────────
from PIL import Image as _PILImage
_page_icon = _PILImage.open(Path(__file__).parent.parent / "static" / "icon.png")
st.set_page_config(
    page_title="Pipeline View · CDDRi",
    page_icon=_page_icon, layout="wide",
    initial_sidebar_state="collapsed",
)

# SciLifeLab brand colours
_NAVY       = "#1B3144"
_DARK_TEAL  = "#045C64"
_TEAL       = "#4C979F"
_LIGHT_TEAL = "#9DCDC0"
_LIME       = "#A7C947"
_VERSION    = "v2.0"
_CONTACT    = "vasanthanathan.poongavanam@scilifelab.se"

# ── Data ──────────────────────────────────────────────────────────────────────
_DATA = Path(__file__).parent.parent / "data" / "tools.json"

try:
    _last_updated = datetime.fromtimestamp(os.path.getmtime(str(_DATA))).strftime("%d %b %Y")
except Exception:
    _last_updated = "2025"


@st.cache_data(ttl=120)
def _load_tools() -> list[dict]:
    if not _DATA.exists():
        return []
    with open(_DATA) as f:
        raw = json.load(f)
    return [t for t in raw if t.get("status", "approved") not in ("pending", "rejected")]


ALL_TOOLS = _load_tools()

# ── Pipeline stage definitions ────────────────────────────────────────────────
STAGES = [
    {
        "id": "target",
        "label": "Target Identification",
        "short": "Target ID",
        "icon": "🎯",
        "color": "#1e3a5f",
        "light": "#e8f0fa",
        "desc": "Protein structure prediction, binding site detection & homology modelling",
        "categories": [
            "Protein Structure Prediction",
            "Protein Structure / Co-folding",
            "Homology Modeling",
            "Binding Site Prediction",
            "Protein Structure Database",
        ],
    },
    {
        "id": "hit",
        "label": "Hit Identification",
        "short": "Hit ID",
        "icon": "🔍",
        "color": "#2563eb",
        "light": "#eff6ff",
        "desc": "Virtual screening, molecular docking & pharmacophore search",
        "categories": [
            "Molecular Docking",
            "Molecular Docking / Benchmarking",
            "Molecular Docking / Validation",
            "Molecular Docking / Representation Learning",
            "Pharmacophore / Virtual Screening",
            "Compound Database",
            "Decoy / Benchmark Set",
            "Ligand-Target Database",
        ],
    },
    {
        "id": "expansion",
        "label": "Hit Expansion",
        "short": "Hit Expansion",
        "icon": "🧩",
        "color": "#0891b2",
        "light": "#ecfeff",
        "desc": "Fragment growing, generative design, de novo design, macrocycles & PROTACs",
        "categories": [
            "Fragment-Based Drug Discovery",
            "De Novo Design",
            "Generative Molecular Design",
            "Generative Molecular Design / LLM",
            "Macrocycle / Cyclic Peptide",
            "Macrocycle / Conformer Generation",
            "Macrocycle Database",
            "PROTAC Design",
            "Linker Design",
            "Molecular Design / Assembly",
        ],
    },
    {
        "id": "lead",
        "label": "Lead Generation",
        "short": "Lead Gen",
        "icon": "⚗️",
        "color": "#7c3aed",
        "light": "#f5f3ff",
        "desc": "Molecular dynamics, free energy calculations & binding affinity prediction",
        "categories": [
            "Molecular Dynamics",
            "Molecular Dynamics Analysis",
            "Free Energy Calculations",
            "Binding Affinity Database",
            "Ligand Preparation",
            "Molecular Preparation",
            "Conformational Sampling",
            "QM / Semi-empirical",
        ],
    },
    {
        "id": "optim",
        "label": "Lead Optimization",
        "short": "Lead Opt",
        "icon": "🔧",
        "color": "#059669",
        "light": "#ecfdf5",
        "desc": "ADMET prediction, SAR analysis & retrosynthesis planning",
        "categories": [
            "ADMET Prediction",
            "Property Prediction / QSAR",
            "3D-QSAR",
            "SAR / Lead Optimization",
            "Synthesis Planning / Retrosynthesis",
        ],
    },
    {
        "id": "analysis",
        "label": "Analysis & Cheminformatics",
        "short": "Analysis",
        "icon": "📊",
        "color": "#dc2626",
        "light": "#fef2f2",
        "desc": "Visualization, cheminformatics toolkits, interaction analysis & benchmarking",
        "categories": [
            "Molecular Visualization",
            "Interaction Analysis",
            "Scaffold Analysis",
            "Cheminformatics",
            "Cheminformatics / Fingerprints",
            "Cheminformatics Platform",
            "Reaction Chemistry",
            "Drug-Target Interaction / KG",
            "Physicochemical Properties",
            "File Format Conversion",
            "ML/DL Platform",
            "ML Platform / Benchmarking",
            "Educational / Workflow",
            "Drug Database",
            "Benchmark / Dataset",
            "Dataset / Benchmark",
            "Molecular Representation / Pre-training",
        ],
    },
]

STAGE_IDS = {s["id"] for s in STAGES}

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif !important; }

html, body { overflow-x: hidden; }

/* ── Streamlit chrome: hide everything ── */
[data-testid="stSidebar"]        { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stToolbar"]        { display: none !important; }
[data-testid="stDecoration"]     { display: none !important; }
[data-testid="stStatusWidget"]   { display: none !important; }
footer    { display: none !important; }
#MainMenu { display: none !important; }
header    { display: none !important; }

/* ── Page background ── */
[data-testid="stAppViewContainer"],
section[data-testid="stMain"],
.main { background: #eef5f4 !important; }

/* ── Block container ── */
.block-container {
  padding: 0 2rem 4rem 2rem !important;
  max-width: 100% !important;
  width: 100% !important;
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
.page-header-title { font-size: 1.6rem; font-weight: 700; color: #fff; margin: 0; }
.page-header-sub   { font-size: 1.05rem; color: #9DCDC0; margin: 0; }
.page-header-home  {
  font-size: 0.85rem; font-weight: 500;
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

/* ── Pipeline stage selector (buttons styled as tab bar) ── */
div:has(.pipe-stage-sentinel) + [data-testid="stHorizontalBlock"] {
  background: #ffffff;
  border: 1px solid #c5ddd9;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 1.5rem;
  box-shadow: 0 1px 4px rgba(4,92,100,0.07);
  gap: 0 !important;
  align-items: stretch !important;
}
div:has(.pipe-stage-sentinel) + [data-testid="stHorizontalBlock"] [data-testid="column"] {
  padding: 0 !important;
  border-right: 1px solid #e5e7eb;
  flex: 1 !important;
}
div:has(.pipe-stage-sentinel) + [data-testid="stHorizontalBlock"] [data-testid="column"]:last-child {
  border-right: none !important;
}
div:has(.pipe-stage-sentinel) + [data-testid="stHorizontalBlock"] button {
  background: transparent !important;
  border: none !important;
  border-radius: 0 !important;
  box-shadow: none !important;
  color: #374151 !important;
  font-size: 0.74rem !important;
  font-weight: 600 !important;
  padding: 0.85rem 0.4rem !important;
  min-height: 76px !important;
  width: 100% !important;
  white-space: pre-line !important;
  line-height: 1.5 !important;
  text-align: center !important;
  transition: background 0.12s !important;
}
div:has(.pipe-stage-sentinel) + [data-testid="stHorizontalBlock"] button:hover {
  background: #f0f7f6 !important;
  color: #1B3144 !important;
}
div:has(.pipe-stage-sentinel) + [data-testid="stHorizontalBlock"] button[kind="primary"] {
  background: #e8f4f3 !important;
  color: #045C64 !important;
  border-bottom: 3px solid #045C64 !important;
}

/* ── Stage section header ── */
.stage-header {
  display: flex; align-items: center; gap: 1rem;
  padding: 0.85rem 1.25rem; border-radius: 8px;
  margin-bottom: 1rem; border-left: 4px solid;
}
.stage-hicon { font-size: 1.75rem; flex-shrink: 0; }
.stage-htitle { font-size: 1.25rem; font-weight: 600; margin: 0; line-height: 1.3; }
.stage-hdesc { font-size: 1.0rem; color: #6b7280; margin: 0.15rem 0 0 0; }
.stage-hcount {
  margin-left: auto; font-size: 0.77rem; font-weight: 600;
  padding: 0.28rem 0.8rem; border-radius: 99px; white-space: nowrap; color: #fff;
}

/* ── Tool card ── */
.tool-card {
  background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px;
  padding: 1rem 1.1rem; margin-bottom: 0.75rem;
  box-shadow: 0 1px 3px rgba(4,92,100,0.06);
  transition: box-shadow 0.12s; height: 100%;
}
.tool-card:hover { box-shadow: 0 3px 10px rgba(4,92,100,0.12); }
.tc-name { font-size: 1.1rem; font-weight: 600; color: #1B3144; margin: 0 0 0.4rem 0; line-height: 1.35; }
.tc-meta { display: flex; gap: 0.35rem; flex-wrap: wrap; align-items: center; margin-bottom: 0.45rem; }
.tc-cat {
  font-size: 0.61rem; font-weight: 600; text-transform: uppercase;
  letter-spacing: 0.05em; padding: 0.14rem 0.48rem; border-radius: 3px;
  background: #e0f2fe; color: #0369a1;
}
.tc-year {
  font-size: 0.67rem; color: #6b7280;
  background: #f3f4f6; padding: 0.1rem 0.4rem; border-radius: 3px;
}
.tc-open {
  font-size: 0.61rem; font-weight: 600; padding: 0.14rem 0.48rem;
  border-radius: 3px; background: #dcfce7; color: #15803d;
}
.tc-commercial {
  font-size: 0.61rem; font-weight: 600; padding: 0.14rem 0.48rem;
  border-radius: 3px; background: #fee2e2; color: #b91c1c;
}
.tc-authors { font-size: 0.82rem; color: #6b7280; margin-bottom: 0.42rem; font-style: italic; }
.tc-features { font-size: 0.97rem; color: #4b5563; margin-bottom: 0.55rem; line-height: 1.5; }
.tc-links { display: flex; gap: 0.7rem; }
.tc-link {
  font-size: 0.72rem; font-weight: 500; color: #045C64;
  text-decoration: none; display: inline-flex; align-items: center; gap: 0.2rem;
}
.tc-link:hover { text-decoration: underline; }

/* ── Empty state ── */
.empty-state { text-align: center; padding: 3rem 1rem; color: #9ca3af; }
.empty-icon { font-size: 2.5rem; margin-bottom: 0.5rem; }
.empty-text { font-size: 0.85rem; }

/* ── Streamlit widget overrides ── */
.stTextInput > div > div > input {
  background: #fff !important; border-color: #c5ddd9 !important;
  font-size: 0.84rem !important;
}
.stSelectbox > div > div { background: #fff !important; border-color: #c5ddd9 !important; font-size: 0.84rem !important; }
</style>
""", unsafe_allow_html=True)


# ── Resolve active stage ───────────────────────────────────────────────────────
if "pipe_stage" not in st.session_state or st.session_state.pipe_stage not in STAGE_IDS:
    st.session_state.pipe_stage = "target"
active_id = st.session_state.pipe_stage
active_stage = next(s for s in STAGES if s["id"] == active_id)


# ── Fixed header ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
  <div class="page-header-left">
    <img src="app/static/icon.png" alt="CDDRi" style="height:58px;width:auto;flex-shrink:0;">
    <span style="width:1px;height:36px;background:rgba(157,205,192,0.25);flex-shrink:0;display:inline-block;"></span>
    <span class="page-header-title">Drug Discovery Pipeline</span>
    <span class="page-header-sub">Navigate by workflow stage</span>
  </div>
</div>
""", unsafe_allow_html=True)
st.markdown('<div style="height:72px;"></div>', unsafe_allow_html=True)


# ── Tool count per stage ──────────────────────────────────────────────────────
def _count(stage: dict) -> int:
    cats = set(stage["categories"])
    return sum(1 for t in ALL_TOOLS if t.get("category", "") in cats)


# ── Pipeline stage selector ───────────────────────────────────────────────────
st.markdown('<span class="pipe-stage-sentinel"></span>', unsafe_allow_html=True)
stage_cols = st.columns(len(STAGES))
for col, s in zip(stage_cols, STAGES):
    n = _count(s)
    with col:
        if st.button(
            f"{s['icon']}\n{s['short']}\n{n} tools",
            key=f"sb_{s['id']}",
            use_container_width=True,
            type="primary" if s["id"] == active_id else "secondary",
        ):
            st.session_state.pipe_stage = s["id"]
            st.rerun()


# ── Stage section header ──────────────────────────────────────────────────────
color = active_stage["color"]
light = active_stage["light"]
stage_cats = set(active_stage["categories"])
stage_tools = [t for t in ALL_TOOLS if t.get("category", "") in stage_cats]

st.markdown(f"""
<div class="stage-header" style="background:{light}; border-left-color:{color};">
  <div>
    <p class="stage-htitle" style="color:{color};">{_html.escape(active_stage['label'])}</p>
    <p class="stage-hdesc">{_html.escape(active_stage['desc'])}</p>
  </div>
  <span class="stage-hcount" style="background:{color};">{len(stage_tools)} tools</span>
</div>
""", unsafe_allow_html=True)


# ── Filters ───────────────────────────────────────────────────────────────────
fc1, fc2, fc3 = st.columns([3, 1.3, 1.3])
with fc1:
    q = st.text_input("", placeholder="Search by name, feature or keyword…",
                      key="pipe_q", label_visibility="collapsed")
with fc2:
    access_f = st.selectbox(
        "", ["All", "Free / Open Source", "Commercial"],
        key="pipe_access", label_visibility="collapsed",
    )
with fc3:
    mol_opts = ["All"] + sorted(
        {t.get("molecule_type", "") for t in stage_tools if t.get("molecule_type", "").strip()}
    )
    mol_f = st.selectbox("", mol_opts, key="pipe_mol", label_visibility="collapsed")


# ── Apply filters ─────────────────────────────────────────────────────────────
filtered = stage_tools
if q:
    ql = q.lower()
    filtered = [
        t for t in filtered
        if ql in (t.get("tool_name") or "").lower()
        or ql in (t.get("key_features") or "").lower()
        or ql in (t.get("notes") or "").lower()
        or ql in (t.get("category") or "").lower()
        or ql in (t.get("authors") or "").lower()
    ]
if access_f == "Free / Open Source":
    filtered = [t for t in filtered if t.get("open_source")]
elif access_f == "Commercial":
    filtered = [t for t in filtered if not t.get("open_source")]
if mol_f != "All":
    filtered = [t for t in filtered if mol_f in (t.get("molecule_type") or "")]

filtered = sorted(
    filtered,
    key=lambda t: (-int(t.get("year") or 0), (t.get("tool_name") or "").lower()),
)


# ── Tool card HTML builder ────────────────────────────────────────────────────
def _card(t: dict) -> str:
    name     = _html.escape((t.get("tool_name") or "Unknown")[:90])
    cat      = _html.escape(t.get("category") or "")
    year     = t.get("year") or ""
    authors  = _html.escape(t.get("authors") or "")
    doi      = t.get("doi") or ""
    github   = t.get("github") or ""
    features = _html.escape((t.get("key_features") or t.get("notes") or "").strip())
    is_open  = t.get("open_source", True)
    lic      = _html.escape(t.get("license") or "")
    mol      = _html.escape(t.get("molecule_type") or "")

    # Safe URL validation
    doi_href    = f"https://doi.org/{doi}" if doi and doi.startswith("10.") else ""
    github_href = github if github and github.startswith("https://github.com/") else ""

    links = []
    if doi_href:
        links.append(f'<a href="{doi_href}" target="_blank" class="tc-link">📄 Paper</a>')
    if github_href:
        links.append(f'<a href="{_html.escape(github_href)}" target="_blank" class="tc-link">🔗 GitHub</a>')
    links_html = "&nbsp;&nbsp;".join(links)

    access_cls   = "tc-open" if is_open else "tc-commercial"
    access_label = (f"Open · {lic}" if lic else "Open Source") if is_open else "Commercial"

    feat = (features[:140] + "…") if len(features) > 140 else features

    parts = [f'<div class="tool-card">']
    parts.append(f'<div class="tc-name">{name}</div>')
    parts.append('<div class="tc-meta">')
    if cat:
        parts.append(f'<span class="tc-cat">{cat}</span>')
    if year:
        parts.append(f'<span class="tc-year">{year}</span>')
    if mol:
        parts.append(f'<span class="tc-year">{mol}</span>')
    parts.append(f'<span class="{access_cls}">{access_label}</span>')
    parts.append('</div>')
    if authors:
        parts.append(f'<div class="tc-authors">{authors}</div>')
    if feat:
        parts.append(f'<div class="tc-features">{feat}</div>')
    if links_html:
        parts.append(f'<div class="tc-links">{links_html}</div>')
    parts.append('</div>')
    return "".join(parts)


# ── Render tool grid ──────────────────────────────────────────────────────────
if not filtered:
    st.markdown("""
    <div class="empty-state">
      <div class="empty-icon">🔎</div>
      <div class="empty-text">No tools match the current filters. Try broadening the search.</div>
    </div>
    """, unsafe_allow_html=True)
else:
    cols = st.columns(3)
    for i, tool in enumerate(filtered):
        with cols[i % 3]:
            st.markdown(_card(tool), unsafe_allow_html=True)


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
