"""
views/pipeline.py — Drug Discovery Pipeline section
Rendered inline from app.py as ?section=pipeline
"""

import json
import html as _html
from pathlib import Path

import streamlit as st

_DATA = Path(__file__).parent.parent / "data" / "tools.json"

STAGES = [
    {
        "id": "target",
        "label": "Target Identification",
        "short": "Target ID",
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


@st.cache_data(ttl=120)
def _load_tools() -> list[dict]:
    if not _DATA.exists():
        return []
    with open(_DATA) as f:
        raw = json.load(f)
    return [t for t in raw if t.get("status", "approved") not in ("pending", "rejected")]


def _count(stage: dict, all_tools: list) -> int:
    cats = set(stage["categories"])
    return sum(1 for t in all_tools if t.get("category", "") in cats)


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

    doi_href    = f"https://doi.org/{doi}" if doi and doi.startswith("10.") else ""
    github_href = github if github and github.startswith("https://github.com/") else ""

    links = []
    if doi_href:
        links.append(f'<a href="{doi_href}" target="_blank" class="tc-link">Paper</a>')
    if github_href:
        links.append(f'<a href="{_html.escape(github_href)}" target="_blank" class="tc-link">GitHub</a>')
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


def render() -> None:
    st.markdown("""
<style>
.block-container { max-width: 100% !important; }

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
  font-size: 0.78rem !important;
  font-weight: 600 !important;
  padding: 0.85rem 0.4rem !important;
  min-height: 60px !important;
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

.stage-header {
  display: flex; align-items: center; gap: 1rem;
  padding: 0.85rem 1.25rem; border-radius: 8px;
  margin-bottom: 1rem; border-left: 4px solid;
}
.stage-htitle { font-size: 1.25rem; font-weight: 600; margin: 0; line-height: 1.3; }
.stage-hdesc  { font-size: 1.0rem; color: #6b7280; margin: 0.15rem 0 0 0; }
.stage-hcount {
  margin-left: auto; font-size: 0.77rem; font-weight: 600;
  padding: 0.28rem 0.8rem; border-radius: 99px; white-space: nowrap; color: #fff;
}

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
.tc-year { font-size: 0.67rem; color: #6b7280; background: #f3f4f6; padding: 0.1rem 0.4rem; border-radius: 3px; }
.tc-open       { font-size: 0.61rem; font-weight: 600; padding: 0.14rem 0.48rem; border-radius: 3px; background: #dcfce7; color: #15803d; }
.tc-commercial { font-size: 0.61rem; font-weight: 600; padding: 0.14rem 0.48rem; border-radius: 3px; background: #fee2e2; color: #b91c1c; }
.tc-authors  { font-size: 0.82rem; color: #6b7280; margin-bottom: 0.42rem; font-style: italic; }
.tc-features { font-size: 0.97rem; color: #4b5563; margin-bottom: 0.55rem; line-height: 1.5; }
.tc-links    { display: flex; gap: 0.7rem; }
.tc-link {
  font-size: 0.72rem; font-weight: 500; color: #045C64;
  text-decoration: none; display: inline-flex; align-items: center; gap: 0.2rem;
}
.tc-link:hover { text-decoration: underline; }

.empty-state { text-align: center; padding: 3rem 1rem; color: #9ca3af; }
.empty-text  { font-size: 0.85rem; }

.stTextInput > div > div > input {
  background: #fff !important; border-color: #c5ddd9 !important; font-size: 0.84rem !important;
}
.stSelectbox > div > div {
  background: #fff !important; border-color: #c5ddd9 !important; font-size: 0.84rem !important;
}
</style>
""", unsafe_allow_html=True)

    all_tools = _load_tools()

    if "pipe_stage" not in st.session_state or st.session_state.pipe_stage not in STAGE_IDS:
        st.session_state.pipe_stage = "target"
    active_id = st.session_state.pipe_stage
    active_stage = next(s for s in STAGES if s["id"] == active_id)

    # Stage selector
    st.markdown('<span class="pipe-stage-sentinel"></span>', unsafe_allow_html=True)
    stage_cols = st.columns(len(STAGES))
    for col, s in zip(stage_cols, STAGES):
        n = _count(s, all_tools)
        with col:
            if st.button(
                f"{s['short']}\n{n} tools",
                key=f"sb_{s['id']}",
                width="stretch",
                type="primary" if s["id"] == active_id else "secondary",
            ):
                st.session_state.pipe_stage = s["id"]
                st.rerun()

    # Stage header
    color = active_stage["color"]
    light = active_stage["light"]
    stage_cats = set(active_stage["categories"])
    stage_tools = [t for t in all_tools if t.get("category", "") in stage_cats]

    st.markdown(f"""
<div class="stage-header" style="background:{light}; border-left-color:{color};">
  <div>
    <p class="stage-htitle" style="color:{color};">{_html.escape(active_stage['label'])}</p>
    <p class="stage-hdesc">{_html.escape(active_stage['desc'])}</p>
  </div>
  <span class="stage-hcount" style="background:{color};">{len(stage_tools)} tools</span>
</div>
""", unsafe_allow_html=True)

    # Filters
    fc1, fc2, fc3 = st.columns([3, 1.3, 1.3])
    with fc1:
        q = st.text_input("Search", placeholder="Search by name, feature or keyword…",
                          key="pipe_q", label_visibility="collapsed")
    with fc2:
        access_f = st.selectbox(
            "Access", ["All", "Free / Open Source", "Commercial"],
            key="pipe_access", label_visibility="collapsed",
        )
    with fc3:
        mol_opts = ["All"] + sorted(
            {t.get("molecule_type", "") for t in stage_tools if t.get("molecule_type", "").strip()}
        )
        mol_f = st.selectbox("Molecule type", mol_opts, key="pipe_mol", label_visibility="collapsed")

    # Apply filters
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

    # Tool grid
    if not filtered:
        st.markdown("""
<div class="empty-state">
  <div class="empty-text">No tools match the current filters. Try broadening the search.</div>
</div>""", unsafe_allow_html=True)
    else:
        cols = st.columns(3)
        for i, tool in enumerate(filtered):
            with cols[i % 3]:
                st.markdown(_card(tool), unsafe_allow_html=True)
