"""
scanner.py — Auto-scan PubMed & CrossRef for new computational drug discovery tools.
Runs weekly via GitHub Actions or manually from the Streamlit UI.
"""

import json
import time
import datetime
import re
import requests
from pathlib import Path

# ─── Config ───────────────────────────────────────────────────────────────────
DATA_DIR     = Path(__file__).parent.parent / "data"
TOOLS_FILE   = DATA_DIR / "tools.json"
PENDING_FILE = DATA_DIR / "pending.json"
HISTORY_FILE = DATA_DIR / "scan_history.json"

# Journals to monitor (PubMed journal abbreviations + CrossRef ISSNs)
TARGET_JOURNALS_PUBMED = [
    "J Chem Inf Model",
    "J Cheminform",
    "J Med Chem",
    "Mol Inform",
    "J Chem Theory Comput",
    "Bioinformatics",
    "Brief Bioinform",
    "Chem Sci",
    "Nat Mach Intell",
    "ACS Med Chem Lett",
    "Sci Rep",
]

# CrossRef ISSNs for key journals
TARGET_JOURNALS_CROSSREF = {
    "Journal of Chemical Information and Modeling": "1549-9596",
    "Journal of Cheminformatics": "1758-2946",
    "Journal of Medicinal Chemistry": "0022-2623",
    "Molecular Informatics": "1868-1743",
    "Bioinformatics": "1367-4803",
    "Scientific Reports": "2045-2322",
    "ACS Medicinal Chemistry Letters": "1948-5875",
}

# Keywords that strongly suggest a software tool publication
TOOL_KEYWORDS = [
    "github.com", "open source", "open-source", "python package",
    "software", "toolkit", "web server", "freely available",
    "command-line", "command line", "pip install", "conda install",
    "source code", "implementation", "framework", "platform",
    "tool", "workflow", "pipeline",
]

# Drug-discovery relevance keywords
DOMAIN_KEYWORDS = [
    "drug discovery", "virtual screening", "molecular docking",
    "qsar", "admet", "lead optimization", "hit identification",
    "de novo", "molecular generation", "free energy",
    "binding affinity", "protein-ligand", "cheminformatics",
    "chemoinformatics", "molecular dynamics", "pharmacophore",
    "scaffold", "fragment", "protac", "macrocycle", "cyclic peptide",
    "deep learning", "machine learning", "neural network", "generative",
    "conformer", "retrosynthesis", "synthesis planning",
]

# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_json(path: Path) -> dict | list:
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {} if "history" in path.name else []


def save_json(path: Path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)


def get_existing_dois() -> set:
    tools   = load_json(TOOLS_FILE)
    pending = load_json(PENDING_FILE)
    history = load_json(HISTORY_FILE)
    dois = set()
    for t in tools + pending:
        if t.get("doi"):
            dois.add(t["doi"].lower().strip())
    for d in history.get("seen_dois", []):
        dois.add(d.lower().strip())
    return dois


def is_tool_paper(title: str, abstract: str) -> tuple[bool, float]:
    """
    Returns (is_tool, confidence_score 0-1).
    Heuristic: checks for tool keywords + domain keywords.
    """
    text = (title + " " + abstract).lower()
    tool_hits   = sum(1 for k in TOOL_KEYWORDS   if k in text)
    domain_hits = sum(1 for k in DOMAIN_KEYWORDS if k in text)
    github_mentioned = "github.com" in text

    score = 0.0
    score += min(tool_hits   * 0.15, 0.6)
    score += min(domain_hits * 0.08, 0.3)
    score += 0.3 if github_mentioned else 0.0
    score = min(score, 1.0)

    return score >= 0.35, round(score, 2)


def extract_github(abstract: str) -> str:
    """Extract first GitHub URL from abstract text."""
    match = re.search(r"https?://github\.com/[\w\-./]+", abstract or "")
    return match.group(0).rstrip(".,)") if match else ""


# ─── PubMed Scanner ───────────────────────────────────────────────────────────

def build_pubmed_query(days_back: int = 90) -> str:
    """Build PubMed esearch query for recent tool papers."""
    date_end   = datetime.date.today()
    date_start = date_end - datetime.timedelta(days=days_back)
    date_range = f'{date_start.strftime("%Y/%m/%d")}:{date_end.strftime("%Y/%m/%d")}[dp]'

    journals = " OR ".join(f'"{j}"[ta]' for j in TARGET_JOURNALS_PUBMED)
    keywords = (
        '("open source"[tiab] OR "python package"[tiab] OR '
        '"github.com"[tiab] OR "web server"[tiab] OR "software"[tiab] OR "toolkit"[tiab])'
    )
    domain = (
        '("drug discovery"[tiab] OR "virtual screening"[tiab] OR '
        '"molecular docking"[tiab] OR "cheminformatics"[tiab] OR '
        '"qsar"[tiab] OR "admet"[tiab] OR "machine learning"[tiab] OR '
        '"deep learning"[tiab] OR "lead optimization"[tiab] OR '
        '"protac"[tiab] OR "macrocycle"[tiab] OR "molecular generation"[tiab])'
    )
    return f"({journals}) AND {keywords} AND {domain} AND {date_range}"


def scan_pubmed(days_back: int = 90, max_results: int = 100) -> list[dict]:
    """Query PubMed Entrez API and return candidate tool entries."""
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    query = build_pubmed_query(days_back)

    # esearch
    try:
        r = requests.get(f"{base}/esearch.fcgi", params={
            "db": "pubmed", "term": query, "retmax": max_results,
            "retmode": "json", "usehistory": "y",
        }, timeout=20)
        r.raise_for_status()
    except Exception as e:
        return [{"error": f"PubMed esearch failed: {e}"}]

    data = r.json()
    ids  = data.get("esearchresult", {}).get("idlist", [])
    if not ids:
        return []

    time.sleep(0.4)  # NCBI rate limit

    # efetch summaries in batches of 20
    candidates = []
    existing_dois = get_existing_dois()

    for i in range(0, len(ids), 20):
        batch = ids[i:i+20]
        try:
            r2 = requests.get(f"{base}/esummary.fcgi", params={
                "db": "pubmed", "id": ",".join(batch), "retmode": "json",
            }, timeout=20)
            r2.raise_for_status()
        except Exception:
            continue

        summaries = r2.json().get("result", {})

        for pmid in batch:
            rec = summaries.get(pmid, {})
            if not rec or "title" not in rec:
                continue

            title    = rec.get("title", "")
            doi      = next((a["value"] for a in rec.get("articleids", [])
                             if a.get("idtype") == "doi"), "")
            journal  = rec.get("source", "")
            year_str = rec.get("pubdate", "")[:4]
            year     = int(year_str) if year_str.isdigit() else 0
            authors_raw = rec.get("authors", [])
            authors  = ", ".join(a.get("name", "") for a in authors_raw[:3])
            if len(authors_raw) > 3:
                authors += " et al."

            if doi and doi.lower() in existing_dois:
                continue

            # Fetch abstract via efetch
            abstract = ""
            try:
                time.sleep(0.4)
                r3 = requests.get(f"{base}/efetch.fcgi", params={
                    "db": "pubmed", "id": pmid, "rettype": "abstract",
                    "retmode": "text",
                }, timeout=15)
                raw = r3.text[:2000]
                # ── Consistency check ──────────────────────────────────────────
                # PubMed occasionally returns a neighbouring paper's abstract
                # (likely due to server-side clustering). Verify the DOI we got
                # from esummary actually appears in the abstract text; if not,
                # discard the abstract so the entry isn't poisoned.
                if doi:
                    doi_in_abstract = re.search(
                        r'doi[:\s]+' + re.escape(doi), raw, re.IGNORECASE
                    )
                    if doi_in_abstract:
                        abstract = raw          # consistent — use it
                    # else: keep abstract="" and rely on title alone
                else:
                    abstract = raw              # no DOI to cross-check against
            except Exception:
                pass

            is_tool, confidence = is_tool_paper(title, abstract)
            if not is_tool:
                continue

            github = extract_github(abstract)

            candidates.append({
                "tool_name":    title[:80],
                "task":         "",
                "category":     "Uncategorized",
                "year":         year,
                "authors":      authors,
                "doi":          doi,
                "journal":      journal,
                "github":       github,
                "language":     "Python" if "python" in abstract.lower() else "",
                "open_source":  True,
                "license":      "",
                "molecule_type":"Small Molecules",
                "role":         "",
                "key_features": "",
                "dependencies": "",
                "status":       "pending",
                "notes":        abstract[:300].replace("\n", " "),
                "pmid":         pmid,
                "confidence":   confidence,
                "source":       "PubMed auto-scan",
                "scanned_at":   datetime.datetime.utcnow().isoformat(),
            })

        time.sleep(0.4)

    return candidates


# ─── CrossRef Scanner ─────────────────────────────────────────────────────────

def scan_crossref(days_back: int = 90, rows: int = 50) -> list[dict]:
    """Query CrossRef API for recent papers mentioning GitHub + drug discovery."""
    from_date = (datetime.date.today() - datetime.timedelta(days=days_back)).isoformat()
    base      = "https://api.crossref.org/works"
    headers   = {"User-Agent": "CADD-Tracker/1.0 (computational chemistry tool tracker)"}
    existing  = get_existing_dois()
    candidates = []

    for journal_name, issn in TARGET_JOURNALS_CROSSREF.items():
        try:
            r = requests.get(base, params={
                "filter":  f"issn:{issn},from-pub-date:{from_date}",
                "query":   "open source software python drug discovery github",
                "rows":    rows,
                "select":  "DOI,title,author,published,abstract,container-title",
            }, headers=headers, timeout=20)
            r.raise_for_status()
        except Exception:
            continue

        items = r.json().get("message", {}).get("items", [])

        for item in items:
            doi   = item.get("DOI", "").lower()
            title = " ".join(item.get("title", [""])) or ""
            abstract = item.get("abstract", "") or ""
            # strip JATS XML tags
            abstract = re.sub(r"<[^>]+>", " ", abstract)

            if doi in existing:
                continue

            is_tool, confidence = is_tool_paper(title, abstract)
            if not is_tool:
                continue

            pub_date = item.get("published", {}).get("date-parts", [[0]])[0]
            year = pub_date[0] if pub_date else 0

            authors_raw = item.get("author", [])
            authors = ", ".join(
                f"{a.get('family', '')} {a.get('given', '')[:1]}".strip()
                for a in authors_raw[:3]
            )
            if len(authors_raw) > 3:
                authors += " et al."

            github = extract_github(abstract)

            candidates.append({
                "tool_name":    title[:80],
                "task":         "",
                "category":     "Uncategorized",
                "year":         year,
                "authors":      authors,
                "doi":          doi,
                "journal":      journal_name,
                "github":       github,
                "language":     "Python" if "python" in abstract.lower() else "",
                "open_source":  True,
                "license":      "",
                "molecule_type":"Small Molecules",
                "role":         "",
                "key_features": "",
                "dependencies": "",
                "status":       "pending",
                "notes":        abstract[:300].replace("\n", " "),
                "confidence":   confidence,
                "source":       "CrossRef auto-scan",
                "scanned_at":   datetime.datetime.utcnow().isoformat(),
            })

        time.sleep(0.5)

    return candidates


# ─── Main entry point ─────────────────────────────────────────────────────────

def run_scan(days_back: int = 90) -> dict:
    """
    Full scan: PubMed + CrossRef → deduplicate → append to pending.json.
    Returns summary stats dict.
    """
    print(f"[scanner] Starting scan (last {days_back} days)...")

    pubmed_hits   = scan_pubmed(days_back=days_back)
    crossref_hits = scan_crossref(days_back=days_back)

    # Merge and deduplicate by DOI
    all_candidates = pubmed_hits + crossref_hits
    seen_in_run: set[str] = set()
    unique = []
    for c in all_candidates:
        if c.get("error"):
            continue
        doi_key = (c.get("doi") or c.get("tool_name", "")).lower().strip()
        if doi_key and doi_key not in seen_in_run:
            seen_in_run.add(doi_key)
            unique.append(c)

    # Load + append to pending
    pending = load_json(PENDING_FILE)
    existing_pending_dois = {(p.get("doi") or "").lower() for p in pending}
    new_entries = [c for c in unique
                   if (c.get("doi") or "").lower() not in existing_pending_dois]
    pending.extend(new_entries)
    save_json(PENDING_FILE, pending)

    # Update scan history
    history = load_json(HISTORY_FILE)
    seen_dois = set(history.get("seen_dois", []))
    seen_dois.update(c.get("doi", "").lower() for c in all_candidates if c.get("doi"))
    history["seen_dois"]  = list(seen_dois)
    history["last_scan"]  = datetime.datetime.utcnow().isoformat()
    save_json(HISTORY_FILE, history)

    stats = {
        "pubmed_found":    len(pubmed_hits),
        "crossref_found":  len(crossref_hits),
        "unique_new":      len(new_entries),
        "total_pending":   len(pending),
        "scan_time":       datetime.datetime.utcnow().isoformat(),
    }
    print(f"[scanner] Done. {stats}")
    return stats


if __name__ == "__main__":
    import sys
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 90
    run_scan(days_back=days)
