"""
views/admin.py — Admin Panel section (requires admin_password from st.secrets)
"""

import json
from datetime import datetime
from pathlib import Path

import streamlit as st

DATA_DIR     = Path(__file__).parent.parent / "data"
TOOLS_FILE   = DATA_DIR / "tools.json"
PENDING_FILE = DATA_DIR / "pending.json"


def _load_tools():
    if not TOOLS_FILE.exists():
        return []
    return json.loads(TOOLS_FILE.read_text())


def _save_tools(data):
    TOOLS_FILE.write_text(json.dumps(data, indent=2, default=str))


def _load_pending():
    if not PENDING_FILE.exists():
        return []
    return json.loads(PENDING_FILE.read_text())


def _save_pending(data):
    PENDING_FILE.write_text(json.dumps(data, indent=2, default=str))


def render() -> None:
    st.markdown("""
<style>
.admin-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1.2rem 1.5rem;
  margin-bottom: 0.75rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.admin-badge {
  display: inline-block;
  font-size: 0.72rem;
  font-weight: 600;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
  background: #fef9c3;
  color: #854d0e;
  margin-left: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

    tab_pending, tab_add, tab_edit = st.tabs([
        "Pending Review",
        "Add Tool",
        "Edit Tool",
    ])

    # ── TAB 1: Pending Review ─────────────────────────────────────────────────
    with tab_pending:
        pending = _load_pending()
        approved_pending = [p for p in pending if p.get("status") == "pending"]

        if not approved_pending:
            st.info("No tools pending review.")
        else:
            st.markdown(
                f'<div style="font-size:0.82rem;color:#6b7280;margin-bottom:0.75rem;">'
                f'{len(approved_pending)} tool(s) awaiting review</div>',
                unsafe_allow_html=True,
            )
            for i, p in enumerate(approved_pending):
                with st.expander(f"{p.get('tool_name', 'Unnamed')} — {p.get('year', '')}"):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown(f"**Task:** {p.get('task','')}")
                        st.markdown(f"**Category:** {p.get('category','')}")
                        st.markdown(f"**Authors:** {p.get('authors','')}")
                        st.markdown(f"**Journal:** {p.get('journal','')}")
                    with c2:
                        doi = p.get("doi", "")
                        if doi:
                            st.markdown(f"[Publication](https://doi.org/{doi})")
                        gh = p.get("github", "")
                        if gh:
                            st.markdown(f"[GitHub]({gh})")
                        st.markdown(f"**License:** {p.get('license','')}")
                        st.markdown(f"**Open Source:** {p.get('open_source', '')}")
                    st.markdown(f"**Key Features:** {p.get('key_features','')}")
                    st.markdown(f"**Notes:** {p.get('notes','')}")

                    b1, b2 = st.columns(2)
                    with b1:
                        if st.button("Approve", key=f"approve_{i}", type="primary"):
                            all_tools = _load_tools()
                            p["status"] = "approved"
                            all_tools.append(p)
                            _save_tools(all_tools)
                            remaining = [x for x in pending if x.get("tool_name") != p.get("tool_name")]
                            _save_pending(remaining)
                            st.cache_data.clear()
                            st.success(f"Approved: {p.get('tool_name')}")
                            st.rerun()
                    with b2:
                        if st.button("Reject", key=f"reject_{i}"):
                            remaining = [x for x in pending if x.get("tool_name") != p.get("tool_name")]
                            _save_pending(remaining)
                            st.warning(f"Rejected: {p.get('tool_name')}")
                            st.rerun()

    # ── TAB 2: Add Tool ───────────────────────────────────────────────────────
    with tab_add:
        st.markdown(
            '<div style="font-size:0.82rem;color:#374151;background:#f0f9ff;'
            'border:1px solid #bae6fd;border-radius:6px;padding:0.6rem 1rem;margin-bottom:1rem;">'
            'Fill in the fields below and click <strong>Add Tool</strong> to add directly '
            'to the approved index.</div>',
            unsafe_allow_html=True,
        )

        with st.form("add_tool_form"):
            r1c1, r1c2 = st.columns(2)
            with r1c1:
                n_name = st.text_input("Tool Name *", key="add_name")
                n_task = st.text_input("Task / Application", key="add_task")
                n_category = st.text_input("Category", key="add_category")
                n_role = st.text_input("Role in Discovery", key="add_role")
                n_mol = st.text_input("Molecule Type (comma-separated)", key="add_mol")
            with r1c2:
                n_authors = st.text_input("Authors", key="add_authors")
                n_journal = st.text_input("Journal", key="add_journal")
                n_year = st.number_input("Year", min_value=1990, max_value=2030,
                                         value=datetime.now().year, key="add_year")
                n_doi = st.text_input("DOI (without https://doi.org/)", key="add_doi")
                n_github = st.text_input("GitHub URL", key="add_github")

            r2c1, r2c2 = st.columns(2)
            with r2c1:
                n_features = st.text_area("Key Features", height=80, key="add_features")
                n_license = st.text_input("License", key="add_license")
                n_lang = st.text_input("Language", key="add_lang")
            with r2c2:
                n_deps = st.text_input("Dependencies", key="add_deps")
                n_notes = st.text_area("Notes", height=80, key="add_notes")
                n_opensource = st.checkbox("Open Source", value=True, key="add_os")

            submitted = st.form_submit_button("Add Tool", type="primary")
            if submitted:
                if not n_name.strip():
                    st.error("Tool Name is required.")
                else:
                    all_tools = _load_tools()
                    names_lower = {t.get("tool_name", "").lower() for t in all_tools}
                    if n_name.strip().lower() in names_lower:
                        st.error(f'"{n_name}" already exists in the index.')
                    else:
                        new_entry = {
                            "tool_name":    n_name.strip(),
                            "task":         n_task.strip(),
                            "category":     n_category.strip(),
                            "role":         n_role.strip(),
                            "key_features": n_features.strip(),
                            "molecule_type": n_mol.strip(),
                            "language":     n_lang.strip(),
                            "open_source":  n_opensource,
                            "license":      n_license.strip(),
                            "dependencies": n_deps.strip(),
                            "doi":          n_doi.strip(),
                            "journal":      n_journal.strip(),
                            "authors":      n_authors.strip(),
                            "year":         int(n_year),
                            "github":       n_github.strip(),
                            "notes":        n_notes.strip(),
                            "status":       "approved",
                        }
                        all_tools.append(new_entry)
                        _save_tools(all_tools)
                        st.cache_data.clear()
                        st.success(f'Added: {n_name.strip()}')

    # ── TAB 3: Edit Tool ──────────────────────────────────────────────────────
    with tab_edit:
        all_tools = _load_tools()
        approved_names = sorted(
            t["tool_name"] for t in all_tools if t.get("status", "approved") == "approved"
        )

        if not approved_names:
            st.info("No approved tools found.")
        else:
            edit_sel = st.selectbox("Select tool to edit", approved_names, key="edit_sel")
            tool_idx = next(
                (i for i, t in enumerate(all_tools) if t.get("tool_name") == edit_sel), None
            )
            if tool_idx is not None:
                t = all_tools[tool_idx]
                with st.form("edit_tool_form"):
                    ec1, ec2 = st.columns(2)
                    with ec1:
                        e_name     = st.text_input("Tool Name", value=t.get("tool_name",""), key="edit_name")
                        e_task     = st.text_input("Task / Application", value=t.get("task",""), key="edit_task")
                        e_category = st.text_input("Category", value=t.get("category",""), key="edit_cat")
                        e_role     = st.text_input("Role in Discovery", value=t.get("role",""), key="edit_role")
                        e_mol      = st.text_input("Molecule Type", value=t.get("molecule_type",""), key="edit_mol")
                    with ec2:
                        e_authors  = st.text_input("Authors", value=t.get("authors",""), key="edit_authors")
                        e_journal  = st.text_input("Journal", value=t.get("journal",""), key="edit_journal")
                        e_year     = st.number_input("Year", min_value=1990, max_value=2030,
                                                      value=int(t.get("year") or datetime.now().year), key="edit_year")
                        e_doi      = st.text_input("DOI", value=t.get("doi",""), key="edit_doi")
                        e_github   = st.text_input("GitHub URL", value=t.get("github",""), key="edit_github")

                    ef1, ef2 = st.columns(2)
                    with ef1:
                        e_features = st.text_area("Key Features", value=t.get("key_features",""), height=80, key="edit_feat")
                        e_license  = st.text_input("License", value=t.get("license",""), key="edit_lic")
                        e_lang     = st.text_input("Language", value=t.get("language",""), key="edit_lang")
                    with ef2:
                        e_deps     = st.text_input("Dependencies", value=t.get("dependencies",""), key="edit_deps")
                        e_notes    = st.text_area("Notes", value=t.get("notes",""), height=80, key="edit_notes")
                        e_os       = st.checkbox("Open Source", value=bool(t.get("open_source", True)), key="edit_os")

                    save_edit = st.form_submit_button("Save Changes", type="primary")
                    if save_edit:
                        all_tools[tool_idx].update({
                            "tool_name":    e_name.strip(),
                            "task":         e_task.strip(),
                            "category":     e_category.strip(),
                            "role":         e_role.strip(),
                            "key_features": e_features.strip(),
                            "molecule_type": e_mol.strip(),
                            "language":     e_lang.strip(),
                            "open_source":  e_os,
                            "license":      e_license.strip(),
                            "dependencies": e_deps.strip(),
                            "doi":          e_doi.strip(),
                            "journal":      e_journal.strip(),
                            "authors":      e_authors.strip(),
                            "year":         int(e_year),
                            "github":       e_github.strip(),
                            "notes":        e_notes.strip(),
                        })
                        _save_tools(all_tools)
                        st.cache_data.clear()
                        st.success(f'Updated: {e_name.strip()}')
                        st.rerun()
