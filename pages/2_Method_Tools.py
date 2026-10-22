"""
pages/2_Method_Tools.py — Method & Tools browser
Full resource index with filters, detail view, tool finder and pending review.
"""

import json, datetime, sys, os
from pathlib import Path
from collections import Counter

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.export import load_tools

# ── Page config ───────────────────────────────────────────────────────────────
from PIL import Image as _PILImage
_page_icon = _PILImage.open(Path(__file__).parent.parent / "static" / "icon.png")
st.set_page_config(
    page_title="Method & Tools · CDDRi",
    page_icon=_page_icon, layout="wide",
    initial_sidebar_state="collapsed",
)

# SciLifeLab brand colours (mirrors home page)
_NAVY      = "#1B3144"
_DARK_TEAL = "#045C64"
_TEAL      = "#4C979F"
_LIGHT_TEAL= "#9DCDC0"
_LIME      = "#A7C947"
_VERSION   = "v2.0"
_CONTACT   = "vasanthanathan.poongavanam@scilifelab.se"

# ── Paths ─────────────────────────────────────────────────────────────────────
DATA_DIR     = Path(__file__).parent.parent / "data"
TOOLS_FILE   = DATA_DIR / "tools.json"
PENDING_FILE = DATA_DIR / "pending.json"
HISTORY_FILE = DATA_DIR / "scan_history.json"

# ── Resource-type classification ──────────────────────────────────────────────
# Each tool is classified into one of five resource types based on its category.
RESOURCE_TYPES = {
    "Software":  [
        "Molecular Docking", "Molecular Docking / Benchmarking",
        "Molecular Docking / Validation", "Molecular Docking / Representation Learning",
        "Molecular Dynamics", "Molecular Dynamics Analysis",
        "Protein Structure Prediction", "Protein Structure / Co-folding",
        "Homology Modeling",
        "Molecular Preparation", "Ligand Preparation",
        "Binding Site Prediction",
        "Free Energy Calculations", "ML/DL Platform", "ML Platform / Benchmarking",
        "Educational / Workflow",
        "Conformational Sampling", "QM / Semi-empirical",
        "Molecular Visualization",
    ],
    "Tools":     [
        "Generative Molecular Design", "Generative Molecular Design / LLM",
        "De Novo Design", "Linker Design", "PROTAC Design",
        "Fragment-Based Drug Discovery", "Macrocycle / Cyclic Peptide",
        "Macrocycle / Conformer Generation", "Molecular Design / Assembly",
        "SAR / Lead Optimization", "Pharmacophore / Virtual Screening",
        "Interaction Analysis", "Scaffold Analysis",
    ],
    "Scripts":   [
        "Cheminformatics", "Cheminformatics / Fingerprints",
        "Cheminformatics Platform", "Reaction Chemistry",
        "Synthesis Planning / Retrosynthesis",
        "Molecular Representation / Pre-training",
        "Drug-Target Interaction / KG",
        "Physicochemical Properties",
        "File Format Conversion",
    ],
    "Databases": [
        "Benchmark / Dataset", "Dataset / Benchmark",
        "Macrocycle Database",
        "Compound Database", "Binding Affinity Database",
        "Ligand-Target Database", "Drug Database",
        "Protein Structure Database", "Decoy / Benchmark Set",
    ],
    "Models":    [
        "Property Prediction / QSAR", "ADMET Prediction",
        "3D-QSAR",
    ],
}

def get_resource_type(category: str) -> str:
    for rtype, cats in RESOURCE_TYPES.items():
        if category in cats:
            return rtype
    return "Tools"   # fallback

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
  font-family: 'IBM Plex Sans', sans-serif !important;
}
.main {
  background: #eef5f4 !important;
  color: #1a1d23 !important;
}
.block-container {
  padding: 0 2rem 4rem 2rem !important;
  max-width: 100% !important;
}

/* ── Hide Streamlit chrome ── */
[data-testid="stToolbar"]        { display: none !important; }
[data-testid="stDecoration"]     { display: none !important; }
[data-testid="stStatusWidget"]   { display: none !important; }
footer    { display: none !important; }
#MainMenu { display: none !important; }
header    { display: none !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: #ffffff !important;
  border-right: 1px solid #e2e5ea !important;
}
[data-testid="stSidebar"] > div:first-child {
  padding-top: 0.75rem;
}

/* ── Sidebar header ── */
.sidebar-brand {
  padding: 0 0.25rem 1.25rem 0.25rem;
  border-bottom: 1px solid #e2e5ea;
  margin-bottom: 1.25rem;
}
.sidebar-brand-title {
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #6b7280;
  margin: 0 0 0.2rem 0;
}
.sidebar-brand-sub {
  font-size: 0.82rem;
  color: #374151;
  font-weight: 500;
  margin: 0;
  line-height: 1.4;
}

/* ── Sidebar nav group label ── */
.nav-group-label {
  font-size: 0.65rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #9ca3af;
  padding: 0.75rem 0 0.35rem 0;
  margin: 0;
}

/* ── Resource type badge ── */
.rtype-badge {
  display: inline-block;
  font-size: 0.65rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  padding: 0.18rem 0.55rem;
  border-radius: 3px;
  margin-right: 0.35rem;
  vertical-align: middle;
}
.rtype-Software  { background: #e0f2fe; color: #0369a1; }
.rtype-Tools     { background: #dcfce7; color: #15803d; }
.rtype-Scripts   { background: #fef9c3; color: #854d0e; }
.rtype-Databases { background: #f3e8ff; color: #7e22ce; }
.rtype-Models    { background: #fee2e2; color: #b91c1c; }

/* ── Search bar ── */
.search-wrap {
  background: #ffffff;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.85rem;
  margin-bottom: 1rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  transition: border-color 0.15s;
}
.search-wrap:focus-within {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59,130,246,0.1);
}
.search-icon { color: #9ca3af; font-size: 0.9rem; flex-shrink: 0; }
.search-input {
  border: none; outline: none; width: 100%;
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 1.0rem; color: #1f2937;
  background: transparent;
}
.search-input::placeholder { color: #9ca3af; }

/* ── Toolbar row ── */
.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.75rem;
  gap: 0.75rem;
  flex-wrap: wrap;
}
.result-count {
  font-size: 0.8rem;
  color: #6b7280;
  font-weight: 400;
}
.result-count strong { color: #374151; }

/* ── View-mode tabs (resource type selector) ── */
.rtype-tabs {
  display: flex; gap: 0.35rem; flex-wrap: wrap; margin-bottom: 1rem;
}
.rtype-tab {
  padding: 0.32rem 0.85rem;
  border-radius: 4px;
  font-size: 0.78rem;
  font-weight: 500;
  border: 1px solid #e5e7eb;
  background: #ffffff;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.12s;
  text-decoration: none;
}
.rtype-tab-active {
  background: #045C64;
  border-color: #045C64;
  color: #ffffff;
}

/* ── Data table ── */
.stDataFrame {
  border-radius: 8px !important;
  overflow: hidden !important;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
}
[data-testid="stDataFrameResizable"] {
  background: #ffffff !important;
  border: 1px solid #e5e7eb !important;
  border-radius: 8px !important;
}

/* ── Section label ── */
.sec-label {
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #9ca3af;
  margin: 1rem 0 0.45rem 0;
}

/* ── Detail panel ── */
.detail-card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 0.75rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.detail-title {
  font-size: 1.35rem;
  font-weight: 600;
  color: #1B3144;
  margin: 0 0 0.2rem 0;
  font-family: 'IBM Plex Sans', sans-serif;
}
.detail-meta {
  font-size: 0.78rem;
  color: #6b7280;
  margin-bottom: 0.85rem;
}
.detail-row {
  display: flex;
  gap: 0.5rem;
  padding: 0.45rem 0;
  border-bottom: 1px solid #f3f4f6;
  font-size: 0.95rem;
  align-items: flex-start;
}
.detail-row:last-child { border-bottom: none; }
.detail-key {
  font-weight: 500;
  color: #374151;
  min-width: 140px;
  flex-shrink: 0;
}
.detail-val { color: #4b5563; }
.detail-link { color: #045C64; text-decoration: none; }
.detail-link:hover { text-decoration: underline; }

/* ── Stats card ── */
.stats-card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1.25rem 1.5rem;
  margin-bottom: 0.75rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.stats-card h4 {
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #9ca3af;
  margin: 0 0 0.85rem 0;
}

/* ── Pending review ── */
.pending-card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-left: 3px solid #f59e0b;
  border-radius: 0 8px 8px 0;
  padding: 1rem 1.25rem;
  margin-bottom: 0.65rem;
  font-size: 0.83rem;
}
.pending-title { font-weight: 600; color: #1f2937; margin-bottom: 0.3rem; }
.conf-track { background: #f3f4f6; border-radius: 99px; height: 5px; margin: 4px 0 8px 0; }
.conf-fill  { height: 5px; border-radius: 99px; background: linear-gradient(90deg,#16a34a,#2563eb); }

/* ── Download buttons ── */
.stDownloadButton > button {
  background: #045C64 !important;
  color: #ffffff !important;
  border: none !important;
  border-radius: 5px !important;
  font-size: 0.8rem !important;
  font-weight: 500 !important;
  padding: 0.4rem 0.9rem !important;
}
.stDownloadButton > button:hover {
  background: #1B3144 !important;
}

/* ── Primary button ── */
.stButton > button {
  background: #ffffff !important;
  color: #374151 !important;
  border: 1px solid #d1d5db !important;
  border-radius: 5px !important;
  font-size: 0.82rem !important;
}
.stButton > button:hover {
  border-color: #045C64 !important;
  color: #045C64 !important;
}

/* ── Approve/reject ── */
button[kind="primaryFormSubmit"], .approve-btn button {
  background: #16a34a !important; color: #fff !important;
}
button[data-testid*="reject"] { background: #fff !important; color: #dc2626 !important; border-color: #fca5a5 !important; }

/* ── Selectbox ── */
.stSelectbox > div > div, .stMultiSelect > div > div {
  background: #ffffff !important;
  border-color: #d1d5db !important;
  font-size: 0.84rem !important;
}
.stTextInput > div > div > input {
  background: #ffffff !important;
  border-color: #d1d5db !important;
  font-size: 0.84rem !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: transparent;
  border-bottom: 2px solid #e5e7eb;
  gap: 0;
}
.stTabs [data-baseweb="tab"] {
  font-size: 0.84rem !important;
  font-weight: 500;
  color: #6b7280 !important;
  padding: 0.5rem 1.1rem !important;
  border-radius: 0 !important;
  border-bottom: 2px solid transparent !important;
  margin-bottom: -2px !important;
}
.stTabs [aria-selected="true"] {
  color: #045C64 !important;
  border-bottom-color: #045C64 !important;
  background: transparent !important;
}

/* ── Slider ── */
.stSlider > div { padding-top: 0.25rem; }

/* ── Footer ── */
.footer {
  margin-top: 2.5rem;
  padding-top: 0.85rem;
  border-top: 1px solid #e5e7eb;
  font-size: 0.73rem;
  color: #9ca3af;
  text-align: center;
}
.footer a { color: #6b7280; text-decoration: none; }

/* ── Expander ── */
.streamlit-expanderHeader {
  font-size: 0.84rem !important;
  font-weight: 500 !important;
  color: #374151 !important;
  background: #ffffff !important;
  border: 1px solid #e5e7eb !important;
  border-radius: 6px !important;
}

/* ── Fixed page header — matches home page ── */
.page-header {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 9998;
  background: linear-gradient(135deg,#071520 0%,#0b2535 40%,#093540 100%);
  padding: 0.6rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 4px 28px rgba(0,0,0,0.45);
}
.page-header-left {
  display: flex; align-items: center; gap: 1rem;
}
.page-header-badge {
  font-size: 0.78rem; font-weight: 600;
  letter-spacing: 0.15em; text-transform: uppercase;
  color: #A7C947;
  background: rgba(167,201,71,0.12);
  border: 1px solid rgba(167,201,71,0.4);
  border-radius: 99px; padding: 0.18rem 0.75rem;
}
.page-header-title {
  font-size: 1.6rem;
  font-weight: 700;
  color: #ffffff;
  letter-spacing: 0.01em;
  margin: 0;
}
.page-header-sub {
  font-size: 1.05rem;
  color: #9DCDC0;
  margin: 0;
}
.page-header-home {
  font-size: 0.85rem; font-weight: 500;
  color: #A7C947; text-decoration: none;
  white-space: nowrap;
}
.page-header-home:hover { color: #ffffff; }

/* ── Fixed footer — matches home page ── */
.page-footer {
  position: fixed;
  bottom: 0; left: 0; right: 0;
  z-index: 9999;
  background: linear-gradient(145deg, #1B3144 0%, #045C64 100%);
  padding: 0.75rem 2rem;
  display: flex;
  justify-content: space-between; align-items: center;
  font-size: 0.92rem; color: #9DCDC0;
}
.page-footer a {
  color: #9DCDC0; text-decoration: none; font-weight: 500;
}
.page-footer a:hover { color: #ffffff; }
.page-footer .sep { color: #1e5050; }

/* ── Hide sidebar entirely ── */
[data-testid="stSidebar"]        { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
</style>
""", unsafe_allow_html=True)


# ── Data loaders ──────────────────────────────────────────────────────────────
@st.cache_data(ttl=60)
def load_all_tools():
    if not TOOLS_FILE.exists():
        return []
    with open(TOOLS_FILE) as f:
        return json.load(f)

@st.cache_data(ttl=30)
def load_pending():
    if not PENDING_FILE.exists():
        return []
    with open(PENDING_FILE) as f:
        return json.load(f)

def load_history():
    if not HISTORY_FILE.exists():
        return {}
    with open(HISTORY_FILE) as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)

def rtype_badge(rtype: str) -> str:
    return f'<span class="rtype-badge rtype-{rtype}">{rtype}</span>'


# ── Load data ─────────────────────────────────────────────────────────────────
all_tools = load_all_tools()
approved  = [t for t in all_tools if t.get("status", "approved") == "approved"]
pending   = load_pending()
history   = load_history()

# Attach resource_type to each tool.
# If a valid type is already stored (manual curation), preserve it;
# otherwise derive from category.
_valid_types = set(RESOURCE_TYPES.keys())
for t in approved:
    if t.get("resource_type") not in _valid_types:
        t["resource_type"] = get_resource_type(t.get("category", ""))

# ── Filter logic ──────────────────────────────────────────────────────────────
def apply_filters(
    tools: list[dict],
    search: str = "",
    rtype: str = "All",
    category: str = "All",
    yr_from: int = 0,
    molecule: str = "All",
    access: str = "All",
) -> list[dict]:
    r = tools
    if rtype != "All":
        r = [t for t in r if t.get("resource_type") == rtype]
    if category != "All":
        r = [t for t in r if t.get("category") == category]
    if yr_from:
        r = [t for t in r if (t.get("year") or 0) >= yr_from]
    if molecule != "All":
        r = [t for t in r if molecule in (t.get("molecule_type") or "")]
    if access == "Open Source":
        r = [t for t in r if t.get("open_source", True)]
    elif access == "Commercial":
        r = [t for t in r if not t.get("open_source", True)]
    if search:
        sl = search.lower()
        r = [t for t in r if any(
            sl in str(t.get(f, "")).lower()
            for f in ["tool_name","task","category","authors",
                      "key_features","role","journal","notes","doi"]
        )]
    return r


# ── Fixed page header ─────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
  <div class="page-header-left">
    <img src="app/static/icon.png" alt="CDDRi" style="height:58px;width:auto;flex-shrink:0;">
    <span style="width:1px;height:36px;background:rgba(157,205,192,0.25);flex-shrink:0;display:inline-block;"></span>
    <span class="page-header-title">Method &amp; Tools</span>
    <span class="page-header-sub">Resource Index</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div style="height:72px;"></div>', unsafe_allow_html=True)

# ── Main tabs ─────────────────────────────────────────────────────────────────
tab_browse, tab_detail, tab_finder, tab_pending = st.tabs([
    "Browse Resources",
    "Resource Detail",
    "Tool Finder",
    "Pending Review",
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — BROWSE
# ══════════════════════════════════════════════════════════════════════════════
with tab_browse:

    # ── Compact filter row ────────────────────────────────────────────────────
    fc = st.columns([3.5, 1.1, 1.5, 0.9, 1.3, 1.0])

    with fc[0]:
        search_q = st.text_input(
            "Search", placeholder="Search by name, task, category, author, journal, DOI…",
            label_visibility="collapsed", key="browse_search",
        )
    with fc[1]:
        f_rtype = st.selectbox(
            "Resource type", ["All"] + list(RESOURCE_TYPES.keys()),
            label_visibility="collapsed", key="browse_rtype",
        )
    with fc[2]:
        if f_rtype == "All":
            cat_opts = sorted(set(t.get("category", "") for t in approved if t.get("category", "")))
        else:
            cat_opts = sorted(RESOURCE_TYPES.get(f_rtype, []))
        f_cat = st.selectbox(
            "Category", ["All"] + cat_opts,
            label_visibility="collapsed", key="browse_cat",
        )
    with fc[3]:
        all_years = sorted(set(t.get("year", 0) for t in approved if t.get("year")), reverse=True)
        f_yr = st.selectbox(
            "Year", ["All"] + [str(y) for y in all_years],
            label_visibility="collapsed", key="browse_yr",
        )
        yr_from = int(f_yr) if f_yr != "All" else 0
    with fc[4]:
        mol_set = sorted({
            m.strip()
            for t in approved
            for m in (t.get("molecule_type") or "").split(",")
            if m.strip()
        })
        f_mol = st.selectbox(
            "Molecule type", ["All"] + mol_set,
            label_visibility="collapsed", key="browse_mol",
        )
    with fc[5]:
        f_access = st.selectbox(
            "Access", ["All", "Open Source", "Commercial"],
            label_visibility="collapsed", key="browse_access",
        )

    filtered = apply_filters(
        approved, search_q,
        rtype=f_rtype, category=f_cat, yr_from=yr_from,
        molecule=f_mol, access=f_access,
    )

    # Result count
    label = f_rtype if f_rtype != "All" else "resources"
    st.markdown(
        f'<div class="result-count"><strong>{len(filtered)}</strong> {label} found'
        + (f' · filtered from {len(approved)}' if len(filtered) < len(approved) else '')
        + '</div>',
        unsafe_allow_html=True,
    )

    # ── Resource-type summary row ──
    rtype_counts = Counter(t.get("resource_type","") for t in approved)
    cols = st.columns(len(RESOURCE_TYPES) + 1)
    all_total   = len(approved)
    active_total = len(filtered)
    with cols[0]:
        st.markdown(
            f'<div style="background:#f8fafc;border:1px solid #e5e7eb;border-radius:6px;'
            f'padding:0.5rem 0.75rem;text-align:center;">'
            f'<div style="font-size:1.15rem;font-weight:600;color:#1B3144;">{all_total}</div>'
            f'<div style="font-size:0.67rem;color:#9ca3af;text-transform:uppercase;letter-spacing:.08em;">All</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    type_colors = {
        "Software":  ("#e0f2fe","#0369a1"),
        "Tools":     ("#dcfce7","#15803d"),
        "Scripts":   ("#fef9c3","#854d0e"),
        "Databases": ("#f3e8ff","#7e22ce"),
        "Models":    ("#fee2e2","#b91c1c"),
    }
    for i, (rtype, (bg, fg)) in enumerate(type_colors.items(), 1):
        cnt = rtype_counts.get(rtype, 0)
        with cols[i]:
            st.markdown(
                f'<div style="background:{bg};border:1px solid {fg}22;border-radius:6px;'
                f'padding:0.5rem 0.75rem;text-align:center;">'
                f'<div style="font-size:1.15rem;font-weight:600;color:{fg};">{cnt}</div>'
                f'<div style="font-size:0.67rem;color:{fg};opacity:.85;text-transform:uppercase;letter-spacing:.08em;">{rtype}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<div style='margin-top:0.85rem'></div>", unsafe_allow_html=True)

    # ── Table ──
    if filtered:
        rows = []
        for t in filtered:
            doi = t.get("doi","")
            gh  = t.get("github","")
            rows.append({
                "Resource Type":  t.get("resource_type",""),
                "Name":           t.get("tool_name",""),
                "Access":         "Open Source" if t.get("open_source", True) else "Commercial",
                "Category":       t.get("category",""),
                "Year":           t.get("year",""),
                "Task":           t.get("task",""),
                "Role":           t.get("role",""),
                "Authors":        t.get("authors",""),
                "Journal":        t.get("journal",""),
                "DOI":            f"https://doi.org/{doi}" if doi else "",
                "GitHub":         gh,
                "Language":       t.get("language",""),
                "License":        t.get("license",""),
                "Molecule Type":  t.get("molecule_type",""),
                "Key Features":   t.get("key_features",""),
                "Dependencies":   t.get("dependencies",""),
                "Notes":          t.get("notes",""),
            })
        df = pd.DataFrame(rows)

        # Collect all known categories across ALL approved tools (not just filtered)
        all_cats = sorted(set(t.get("category","") for t in approved if t.get("category","")))

        edited_df = st.data_editor(
            df,
            width='stretch',
            height=540,
            column_config={
                "Resource Type": st.column_config.SelectboxColumn(
                    "Type",
                    options=list(RESOURCE_TYPES.keys()),
                    required=True,
                    width=110,
                ),
                "Category": st.column_config.SelectboxColumn(
                    "Category",
                    options=all_cats,
                    width=210,
                ),
                "Name":          st.column_config.TextColumn("Name",     width=170),
                "Access":        st.column_config.TextColumn("Access",   width=100),
                "Year":          st.column_config.NumberColumn("Year",   width=65, format="%d"),
                "Task":          st.column_config.TextColumn("Task / Application", width=260),
                "Role":          st.column_config.TextColumn("Role in Discovery",  width=200),
                "Authors":       st.column_config.TextColumn("Authors",   width=170),
                "Journal":       st.column_config.TextColumn("Journal",   width=230),
                "DOI":           st.column_config.LinkColumn("DOI",       width=100, display_text="Open ↗"),
                "GitHub":        st.column_config.LinkColumn("GitHub",    width=100, display_text="Repo ↗"),
                "Language":      st.column_config.TextColumn("Language",  width=100),
                "License":       st.column_config.TextColumn("License",   width=100),
                "Molecule Type": st.column_config.TextColumn("Mol. Type", width=180),
                "Key Features":  st.column_config.TextColumn("Key Features", width=340),
                "Dependencies":  st.column_config.TextColumn("Dependencies", width=160),
                "Notes":         st.column_config.TextColumn("Notes",     width=300),
            },
            disabled=["Name","Access","Year","Task","Role","Authors","Journal",
                      "DOI","GitHub","Language","License","Molecule Type",
                      "Key Features","Dependencies","Notes"],
            hide_index=True,
            key="browse_editor",
        )

        # ── Detect changes and offer save ──
        orig_slice = df[["Resource Type","Category"]]
        edit_slice = edited_df[["Resource Type","Category"]]
        changed_mask = (orig_slice != edit_slice).any(axis=1)
        n_changed = changed_mask.sum()

        if n_changed:
            st.markdown(
                f'<div style="font-size:0.8rem;color:#92400e;background:#fffbeb;'
                f'border:1px solid #fde68a;border-radius:6px;padding:0.5rem 0.85rem;margin-top:0.5rem;">'
                f'{n_changed} row(s) edited — click Save to persist.</div>',
                unsafe_allow_html=True,
            )
            if st.button("💾 Save Changes", type="primary", key="save_browse_edits"):
                all_tools_data = load_all_tools()
                for idx in edited_df.index[changed_mask]:
                    name         = edited_df.at[idx, "Name"]
                    new_rtype    = edited_df.at[idx, "Resource Type"]
                    new_category = edited_df.at[idx, "Category"]
                    for tool_entry in all_tools_data:
                        if tool_entry.get("tool_name") == name:
                            tool_entry["resource_type"] = new_rtype
                            tool_entry["category"]      = new_category
                            break
                save_json(TOOLS_FILE, all_tools_data)
                # Clear editor state so it picks up fresh data after rerun
                if "browse_editor" in st.session_state:
                    del st.session_state["browse_editor"]
                st.success(f"Saved {n_changed} change(s).")
                st.cache_data.clear()
                st.rerun()
    else:
        st.info("No resources match the current filters.")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — DETAIL
# ══════════════════════════════════════════════════════════════════════════════
with tab_detail:
    sorted_names = sorted(t["tool_name"] for t in approved)
    sel = st.selectbox("Select resource", options=sorted_names, label_visibility="visible")
    tool = next((t for t in approved if t["tool_name"] == sel), None)

    if tool:
        doi_url = f"https://doi.org/{tool.get('doi','')}" if tool.get("doi") else ""
        github  = tool.get("github","")
        rtype   = tool.get("resource_type","")
        bg, fg  = type_colors.get(rtype, ("#f3f4f6","#374151"))

        col_main, col_side = st.columns([3, 1.2])
        with col_main:
            st.markdown(f"""
            <div class="detail-card">
              <div style="margin-bottom:0.6rem;">
                <span class="rtype-badge rtype-{rtype}">{rtype}</span>
                <span style="font-size:0.75rem;color:#9ca3af;">{tool.get('category','')}</span>
              </div>
              <div class="detail-title">{tool.get('tool_name','')}</div>
              <div class="detail-meta">
                {tool.get('authors','')} &nbsp;·&nbsp;
                {tool.get('journal','')} &nbsp;·&nbsp;
                {tool.get('year','')}
              </div>

              <div class="detail-row">
                <div class="detail-key">Task</div>
                <div class="detail-val">{tool.get('task','')}</div>
              </div>
              <div class="detail-row">
                <div class="detail-key">Role in Discovery</div>
                <div class="detail-val">{tool.get('role','')}</div>
              </div>
              <div class="detail-row">
                <div class="detail-key">Molecule Type</div>
                <div class="detail-val">{tool.get('molecule_type','')}</div>
              </div>
              <div class="detail-row">
                <div class="detail-key">Key Features</div>
                <div class="detail-val">{tool.get('key_features','')}</div>
              </div>
              <div class="detail-row">
                <div class="detail-key">Language</div>
                <div class="detail-val">{tool.get('language','')}</div>
              </div>
              <div class="detail-row">
                <div class="detail-key">License</div>
                <div class="detail-val">{tool.get('license','')}</div>
              </div>
              <div class="detail-row">
                <div class="detail-key">Dependencies</div>
                <div class="detail-val">{tool.get('dependencies','')}</div>
              </div>
              <div class="detail-row">
                <div class="detail-key">Notes</div>
                <div class="detail-val">{tool.get('notes','')}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        with col_side:
            st.markdown('<div class="sec-label">Links</div>', unsafe_allow_html=True)
            if doi_url:
                st.markdown(f"[View Publication]({doi_url})")
                st.caption(f"DOI: {tool.get('doi','')}")
            if github:
                st.markdown(f"[GitHub Repository]({github})")

            st.markdown('<div class="sec-label">Classification</div>', unsafe_allow_html=True)
            st.markdown(
                f'<span class="rtype-badge rtype-{rtype}">{rtype}</span>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div style="font-size:0.78rem;color:#6b7280;margin-top:0.35rem;">'
                f'{tool.get("category","")}</div>',
                unsafe_allow_html=True,
            )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — TOOL FINDER
# ══════════════════════════════════════════════════════════════════════════════

# ── Mapping: user goal → primary + supporting categories ─────────────────────
GOAL_CATEGORIES = {
    "Molecular Docking & Virtual Screening": {
        "primary":    ["Molecular Docking","Pharmacophore / Virtual Screening",
                       "Molecular Docking / Benchmarking"],
        "supporting": ["Ligand Preparation","Molecular Preparation",
                       "Binding Site Prediction","Compound Database","Decoy / Benchmark Set"],
    },
    "De Novo / Generative Molecule Design": {
        "primary":    ["Generative Molecular Design","Generative Molecular Design / LLM",
                       "De Novo Design"],
        "supporting": ["SAR / Lead Optimization","Cheminformatics Platform",
                       "Fragment-Based Drug Discovery"],
    },
    "Protein Structure Prediction": {
        "primary":    ["Protein Structure Prediction","Protein Structure / Co-folding",
                       "Homology Modeling"],
        "supporting": ["Molecular Visualization","Binding Site Prediction"],
    },
    "Molecular Dynamics Simulation": {
        "primary":    ["Molecular Dynamics"],
        "supporting": ["Molecular Dynamics Analysis","Molecular Preparation",
                       "Free Energy Calculations","Molecular Visualization"],
    },
    "Free Energy Calculations": {
        "primary":    ["Free Energy Calculations"],
        "supporting": ["Molecular Dynamics","Ligand Preparation","Molecular Preparation"],
    },
    "ADMET / Toxicity Prediction": {
        "primary":    ["ADMET Prediction"],
        "supporting": ["Physicochemical Properties","Property Prediction / QSAR",
                       "Cheminformatics Platform"],
    },
    "Physicochemical Property Prediction": {
        "primary":    ["Physicochemical Properties","Property Prediction / QSAR"],
        "supporting": ["Cheminformatics Platform","ADMET Prediction"],
    },
    "Protein-Ligand Interaction Analysis": {
        "primary":    ["Interaction Analysis","Binding Site Prediction"],
        "supporting": ["Molecular Visualization","Molecular Docking"],
    },
    "QSAR / ML Model Building": {
        "primary":    ["Property Prediction / QSAR","ML/DL Platform","3D-QSAR"],
        "supporting": ["Physicochemical Properties","Benchmark / Dataset",
                       "Cheminformatics Platform","Binding Affinity Database"],
    },
    "Compound / Database Search": {
        "primary":    ["Compound Database","Drug Database","Binding Affinity Database",
                       "Ligand-Target Database","Decoy / Benchmark Set"],
        "supporting": ["Cheminformatics Platform","Cheminformatics"],
    },
    "Scaffold & SAR Analysis": {
        "primary":    ["SAR / Lead Optimization","Scaffold Analysis"],
        "supporting": ["Cheminformatics Platform","Property Prediction / QSAR",
                       "Molecular Visualization"],
    },
    "Conformer Generation": {
        "primary":    ["Conformational Sampling"],
        "supporting": ["Ligand Preparation","QM / Semi-empirical"],
    },
    "QM / Semi-empirical Calculations": {
        "primary":    ["QM / Semi-empirical"],
        "supporting": ["Conformational Sampling","Molecular Dynamics"],
    },
    "Retrosynthesis / Synthesis Planning": {
        "primary":    ["Synthesis Planning / Retrosynthesis","Reaction Chemistry"],
        "supporting": ["Cheminformatics Platform"],
    },
    "Fragment-Based Drug Discovery": {
        "primary":    ["Fragment-Based Drug Discovery"],
        "supporting": ["Molecular Docking","Binding Site Prediction","Conformational Sampling"],
    },
    "Peptide / Macrocycle Design": {
        "primary":    ["Macrocycle / Cyclic Peptide","Macrocycle / Conformer Generation",
                       "Macrocycle Database"],
        "supporting": ["Molecular Docking","Conformational Sampling","Physicochemical Properties"],
    },
    "PROTAC / Molecular Glue Design": {
        "primary":    ["PROTAC Design"],
        "supporting": ["Molecular Docking","Linker Design"],
    },
    "Linker Design": {
        "primary":    ["Linker Design"],
        "supporting": ["Molecular Docking","Fragment-Based Drug Discovery"],
    },
    "Molecular Visualisation": {
        "primary":    ["Molecular Visualization"],
        "supporting": ["Interaction Analysis","Molecular Dynamics Analysis"],
    },
    "Cheminformatics / File Handling": {
        "primary":    ["Cheminformatics","Cheminformatics Platform","File Format Conversion"],
        "supporting": ["Physicochemical Properties"],
    },
}

# AI/ML-leaning categories
_ML_CATS = {
    "Generative Molecular Design","Generative Molecular Design / LLM","De Novo Design",
    "Property Prediction / QSAR","ADMET Prediction","ML/DL Platform",
    "ML Platform / Benchmarking","Drug-Target Interaction / KG",
    "Molecular Representation / Pre-training","Protein Structure Prediction",
}
# Physics-leaning categories
_PHY_CATS = {
    "Molecular Dynamics","Molecular Dynamics Analysis","Free Energy Calculations",
    "QM / Semi-empirical","Conformational Sampling","Molecular Docking",
    "Homology Modeling","Molecular Preparation","Ligand Preparation",
}

def _score_tool(tool: dict, mol_filter: str, approach: str) -> bool:
    """Return True if tool passes the molecule-type and approach filters."""
    if mol_filter != "Any":
        mt = (tool.get("molecule_type") or "").lower()
        if mol_filter.lower() not in mt and "any" not in mt:
            return False
    if approach == "AI / ML-based":
        if tool.get("category") not in _ML_CATS:
            return False
    elif approach == "Physics-based":
        if tool.get("category") not in _PHY_CATS:
            return False
    return True

with tab_finder:
    st.markdown("""
    <div style="font-size:0.82rem;color:#374151;background:#f0f9ff;border:1px solid
    #bae6fd;border-radius:6px;padding:0.6rem 1rem;margin-bottom:1.1rem;">
    Answer the questions below and click <strong>Find Tools</strong> to get
    personalised recommendations from the index.
    </div>""", unsafe_allow_html=True)

    # ── Question layout ───────────────────────────────────────────────────────
    q1, q2 = st.columns(2)

    with q1:
        st.markdown('<div style="font-size:0.8rem;font-weight:600;color:#6b7280;'
                    'text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px;">'
                    'What do you want to do?</div>', unsafe_allow_html=True)
        goal = st.selectbox("Goal", ["— select —"] + list(GOAL_CATEGORIES.keys()),
                            label_visibility="collapsed", key="finder_goal")

        st.markdown('<div style="font-size:0.8rem;font-weight:600;color:#6b7280;'
                    'text-transform:uppercase;letter-spacing:.06em;margin:10px 0 4px;">'
                    'Molecule type</div>', unsafe_allow_html=True)
        mol_type = st.radio("Molecule type",
            ["Any","Small Molecules","Proteins","Peptides / Cyclic Peptides",
             "Macrocycles","Nucleic Acids"],
            horizontal=True, label_visibility="collapsed", key="finder_mol")

    with q2:
        st.markdown('<div style="font-size:0.8rem;font-weight:600;color:#6b7280;'
                    'text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px;">'
                    'Access type</div>', unsafe_allow_html=True)
        access = st.radio("Access", ["Any","Open Source","Commercial"],
                          horizontal=True, label_visibility="collapsed", key="finder_access")

        st.markdown('<div style="font-size:0.8rem;font-weight:600;color:#6b7280;'
                    'text-transform:uppercase;letter-spacing:.06em;margin:10px 0 4px;">'
                    'Preferred approach</div>', unsafe_allow_html=True)
        approach = st.radio("Approach",
            ["Any","AI / ML-based","Physics-based"],
            horizontal=True, label_visibility="collapsed", key="finder_approach")

        st.markdown('<div style="font-size:0.8rem;font-weight:600;color:#6b7280;'
                    'text-transform:uppercase;letter-spacing:.06em;margin:10px 0 4px;">'
                    'Resource types to include</div>', unsafe_allow_html=True)
        incl_types = st.multiselect("Resource types",
            options=list(RESOURCE_TYPES.keys()),
            default=list(RESOURCE_TYPES.keys()),
            label_visibility="collapsed", key="finder_rtypes")

    run_finder = st.button("Find Tools", type="primary", width='content',
                           key="finder_run")

    # ── Results ───────────────────────────────────────────────────────────────
    if run_finder or st.session_state.get("finder_results_shown"):
        if goal == "— select —":
            st.warning("Please select what you want to do first.")
        else:
            st.session_state["finder_results_shown"] = True
            cats_map   = GOAL_CATEGORIES[goal]
            primary_cats   = set(cats_map["primary"])
            supporting_cats = set(cats_map["supporting"])

            primary_tools   = []
            supporting_tools = []

            for t in approved:
                cat   = t.get("category","")
                rtype = t.get("resource_type","")

                # resource-type filter
                if incl_types and rtype not in incl_types:
                    continue

                # access filter
                if access == "Open Source" and not t.get("open_source", True):
                    continue
                if access == "Commercial" and t.get("open_source", True):
                    continue

                # molecule type + approach filter
                if not _score_tool(t, mol_type, approach):
                    continue

                if cat in primary_cats:
                    primary_tools.append(t)
                elif cat in supporting_cats:
                    supporting_tools.append(t)

            total = len(primary_tools) + len(supporting_tools)
            if total == 0:
                st.info("No tools match these filters — try widening the access or approach.")
            else:
                st.markdown(
                    f'<div style="font-size:0.82rem;color:#15803d;background:#f0fdf4;'
                    f'border:1px solid #bbf7d0;border-radius:6px;padding:0.5rem 1rem;'
                    f'margin:0.75rem 0;">'
                    f'<strong>{total}</strong> tools found — '
                    f'<strong>{len(primary_tools)}</strong> primary · '
                    f'<strong>{len(supporting_tools)}</strong> supporting</div>',
                    unsafe_allow_html=True,
                )

                def _render_tool_card(t: dict, badge: str, badge_color: str):
                    doi    = t.get("doi","")
                    gh     = t.get("github","")
                    rtype  = t.get("resource_type","")
                    bg, fg = type_colors.get(rtype, ("#f3f4f6","#374151"))
                    links  = ""
                    if doi:
                        links += (f'<a href="https://doi.org/{doi}" target="_blank" '
                                  f'style="font-size:0.72rem;color:#2563eb;'
                                  f'text-decoration:none;margin-right:8px;">DOI ↗</a>')
                    if gh:
                        links += (f'<a href="{gh}" target="_blank" '
                                  f'style="font-size:0.72rem;color:#16a34a;'
                                  f'text-decoration:none;">GitHub ↗</a>')
                    os_tag = ('<span style="font-size:0.68rem;background:#dcfce7;'
                              'color:#15803d;border-radius:3px;padding:1px 5px;">'
                              'Open Source</span>'
                              if t.get("open_source") else
                              '<span style="font-size:0.68rem;background:#fee2e2;'
                              'color:#b91c1c;border-radius:3px;padding:1px 5px;">'
                              'Commercial</span>')
                    st.markdown(f"""
                    <div style="border:1px solid #e5e7eb;border-radius:8px;
                    padding:0.7rem 1rem;margin-bottom:0.5rem;background:#fff;">
                      <div style="display:flex;align-items:center;gap:0.5rem;
                      flex-wrap:wrap;margin-bottom:0.3rem;">
                        <span style="font-size:0.92rem;font-weight:600;color:#1f2937;">
                          {t.get('tool_name','')}</span>
                        <span style="font-size:0.68rem;background:{badge_color}22;
                        color:{badge_color};border:1px solid {badge_color}44;
                        border-radius:3px;padding:1px 6px;">{badge}</span>
                        <span style="font-size:0.68rem;background:{bg};color:{fg};
                        border-radius:3px;padding:1px 5px;">{rtype}</span>
                        {os_tag}
                        <span style="font-size:0.68rem;color:#9ca3af;">
                          {t.get('year','')}</span>
                      </div>
                      <div style="font-size:0.8rem;color:#374151;margin-bottom:0.25rem;">
                        {t.get('task','')}</div>
                      <div style="font-size:0.75rem;color:#6b7280;margin-bottom:0.3rem;">
                        {t.get('key_features','')}</div>
                      <div style="display:flex;gap:0.5rem;align-items:center;">
                        {links}
                        <span style="font-size:0.7rem;color:#9ca3af;">
                          {t.get('authors','')}</span>
                      </div>
                    </div>""", unsafe_allow_html=True)

                if primary_tools:
                    st.markdown(
                        '<div style="font-size:0.78rem;font-weight:700;color:#1B3144;'
                        'text-transform:uppercase;letter-spacing:.07em;'
                        'margin:1rem 0 0.4rem;">Primary Tools</div>',
                        unsafe_allow_html=True)
                    cols = st.columns(2)
                    for idx, t in enumerate(sorted(primary_tools,
                                                   key=lambda x: x.get("year",0),
                                                   reverse=True)):
                        with cols[idx % 2]:
                            _render_tool_card(t, "Primary", "#1B3144")

                if supporting_tools:
                    st.markdown(
                        '<div style="font-size:0.78rem;font-weight:700;color:#6b7280;'
                        'text-transform:uppercase;letter-spacing:.07em;'
                        'margin:1.2rem 0 0.4rem;">Supporting / Pipeline Tools</div>',
                        unsafe_allow_html=True)
                    cols = st.columns(2)
                    for idx, t in enumerate(sorted(supporting_tools,
                                                   key=lambda x: x.get("year",0),
                                                   reverse=True)):
                        with cols[idx % 2]:
                            _render_tool_card(t, "Supporting", "#6b7280")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — PENDING REVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tab_pending:
    pending_data = load_pending()

    # ── Scan trigger ─────────────────────────────────────────────────────────
    sc1, sc2, sc3 = st.columns([2, 1, 3])
    with sc1:
        if st.button("Run Scan Now", width='stretch', key="run_scan_btn"):
            with st.spinner("Scanning PubMed & CrossRef…"):
                try:
                    from utils.scanner import run_scan
                    stats = run_scan(days_back=90)
                    st.success(f"{stats['unique_new']} new candidates found.")
                    st.cache_data.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"Scan failed: {e}")
    with sc2:
        last_scan = history.get("last_scan")
        if last_scan:
            try:
                dt  = datetime.datetime.fromisoformat(last_scan)
                ago = (datetime.datetime.now(datetime.UTC) - dt).days
                st.caption(f"Last scan: {ago}d ago")
            except Exception:
                st.caption(f"Last scan: {last_scan[:10]}")
        else:
            st.caption("Last scan: never")

    st.markdown("<div style='margin-top:0.5rem'></div>", unsafe_allow_html=True)

    if not pending_data:
        st.markdown("""
        <div style="text-align:center;padding:3rem 1rem;color:#9ca3af;">
          <div style="font-size:2rem;margin-bottom:0.5rem;color:#16a34a;font-weight:700;">&#10003;</div>
          <div style="font-weight:500;color:#6b7280;">No entries pending review</div>
          <div style="font-size:0.8rem;margin-top:0.25rem;">
            Run a scan above to check for new publications.
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(
            f'<div style="font-size:0.82rem;color:#92400e;background:#fffbeb;'
            f'border:1px solid #fde68a;border-radius:6px;padding:0.6rem 1rem;margin-bottom:1rem;">'
            f'<strong>{len(pending_data)}</strong> entries await review. '
            f'Approve ✓ or Reject ✗ inline — expand a row to edit details first.</div>',
            unsafe_allow_html=True,
        )

        # ── Column header row ──
        h0, h1, h2, h3, h4, h5 = st.columns([2.8, 1.0, 1.2, 0.8, 0.9, 0.9])
        for col, label in zip(
            [h0, h1, h2, h3, h4, h5],
            ["Tool", "Year", "Journal", "Conf %", "", ""],
        ):
            col.markdown(
                f'<div style="font-size:0.72rem;font-weight:600;color:#6b7280;'
                f'text-transform:uppercase;letter-spacing:0.05em;padding-bottom:4px;">'
                f'{label}</div>',
                unsafe_allow_html=True,
            )
        st.markdown('<hr style="margin:0 0 0.4rem 0;border-color:#e5e7eb;">', unsafe_allow_html=True)

        for entry in pending_data:
            # Stable unique ID per entry — derived from content, NOT index.
            # This means session-state keys never shift when items are removed.
            import hashlib as _hl
            _uid = _hl.md5(
                f"{entry.get('tool_name','')}{entry.get('doi','')}{entry.get('year','')}".encode()
            ).hexdigest()[:10]

            conf_pct = int(entry.get("confidence", 0) * 100)
            doi_url  = f"https://doi.org/{entry.get('doi','')}" if entry.get("doi") else ""
            github   = entry.get("github", "")

            # ── Inline action row ──
            r0, r1, r2, r3, r4, r5 = st.columns([2.8, 1.0, 1.2, 0.8, 0.9, 0.9])
            r0.markdown(
                f'<div style="font-size:0.85rem;font-weight:600;color:#1f2937;'
                f'padding:6px 0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">'
                f'{entry.get("tool_name","")}</div>',
                unsafe_allow_html=True,
            )
            r1.markdown(f'<div style="padding:6px 0;font-size:0.84rem;">{entry.get("year","")}</div>', unsafe_allow_html=True)
            r2.markdown(f'<div style="padding:6px 0;font-size:0.84rem;color:#374151;">{entry.get("journal","")[:20]}</div>', unsafe_allow_html=True)
            r3.markdown(f'<div style="padding:6px 0;font-size:0.84rem;">{conf_pct}%</div>', unsafe_allow_html=True)

            with r4:
                if st.button("✓ Approve", key=f"app_{_uid}", width='stretch', type="primary"):
                    # Merge any in-progress edits from session state back into entry
                    entry["tool_name"]    = st.session_state.get(f"nm_{_uid}",  entry.get("tool_name",""))
                    entry["category"]     = st.session_state.get(f"ct_{_uid}",  entry.get("category",""))
                    entry["role"]         = st.session_state.get(f"ro_{_uid}",  entry.get("role",""))
                    entry["task"]         = st.session_state.get(f"ta_{_uid}",  entry.get("task",""))
                    entry["key_features"] = st.session_state.get(f"kf_{_uid}",  entry.get("key_features",""))
                    entry["status"]       = "approved"
                    entry["resource_type"] = get_resource_type(entry.get("category", ""))
                    tl = load_all_tools(); tl.append(entry)
                    save_json(TOOLS_FILE, tl)
                    new_p = [p for p in pending_data
                             if _hl.md5(f"{p.get('tool_name','')}{p.get('doi','')}{p.get('year','')}".encode()).hexdigest()[:10] != _uid]
                    save_json(PENDING_FILE, new_p)
                    st.cache_data.clear(); st.rerun()

            with r5:
                if st.button("✗ Reject", key=f"rej_{_uid}", width='stretch'):
                    new_p = [p for p in pending_data
                             if _hl.md5(f"{p.get('tool_name','')}{p.get('doi','')}{p.get('year','')}".encode()).hexdigest()[:10] != _uid]
                    save_json(PENDING_FILE, new_p)
                    st.cache_data.clear(); st.rerun()

            # ── Collapsible detail / edit panel — label is unique so expander
            #    state never bleeds between entries when the list length changes ──
            with st.expander(f"Edit — {entry.get('tool_name','')[:55]}", expanded=False):
                c1, c2 = st.columns([2.5, 1.5])
                with c1:
                    st.markdown(f"**Authors:** {entry.get('authors','')}")
                    if doi_url:
                        st.markdown(f"**DOI:** [{entry.get('doi','')}]({doi_url})")
                    if github:
                        st.markdown(f"**GitHub:** [{github}]({github})")
                    st.markdown(
                        f'<div class="conf-track">'
                        f'<div class="conf-fill" style="width:{conf_pct}%"></div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(f"**Abstract:** {entry.get('notes','')[:350]}")
                with c2:
                    entry["tool_name"]    = st.text_input("Name",         value=entry.get("tool_name",""),    key=f"nm_{_uid}")
                    entry["category"]     = st.selectbox("Category",
                        options=sorted(set(t.get("category","Other") for t in approved)),
                        index=0, key=f"ct_{_uid}")
                    entry["role"]         = st.text_input("Role",         value=entry.get("role",""),         key=f"ro_{_uid}")
                    entry["task"]         = st.text_input("Task",         value=entry.get("task",""),         key=f"ta_{_uid}")
                    entry["key_features"] = st.text_input("Key features", value=entry.get("key_features",""), key=f"kf_{_uid}")

            st.markdown('<hr style="margin:0.25rem 0;border-color:#f3f4f6;">', unsafe_allow_html=True)


# ── Fixed footer — matches home page ─────────────────────────────────────────
try:
    _mtime_mt     = os.path.getmtime(str(TOOLS_FILE))
    _updated_mt   = datetime.datetime.fromtimestamp(_mtime_mt).strftime("%d %b %Y")
except Exception:
    _updated_mt = "2025"

_footer_html = (
    '<div class="page-footer">'
    '<div style="display:flex;align-items:center;gap:1rem;">'
    f'<span>Updated&nbsp;<strong style="color:#e8f4f2;">{_updated_mt}</strong>'
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
st.markdown(_footer_html, unsafe_allow_html=True)
