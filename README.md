# 🧬 CADD Tools Tracker

A living, auto-updating web database of **open-source computational medicinal chemistry tools** — searchable, filterable, and automatically scanned for new publications weekly.

---

## Features

| Feature | Details |
|---|---|
| 📋 **Searchable database** | 70+ tools with full metadata |
| 🔍 **Smart filters** | Category, year, molecule type, free-text search |
| ⬇️ **Export** | Download as Excel or CSV with one click |
| 🔬 **Tool detail view** | Full info, links to DOI and GitHub |
| 🕐 **Pending review queue** | Human-in-the-loop approval for auto-detected tools |
| 🤖 **Auto-scan** | Weekly PubMed + CrossRef scan via GitHub Actions |
| 📊 **Statistics** | Category breakdown, year trends, pipeline coverage |

---

## Quick Start (Local)

```bash
git clone https://github.com/YOUR_USERNAME/cadd-tools-tracker
cd cadd-tools-tracker
pip install -r requirements.txt
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## Deploy for Free

### Option A — Streamlit Community Cloud (recommended)

1. Push this repo to GitHub (public or private)
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select your repo, branch `main`, file `app.py`
4. Click **Deploy** — live in ~2 minutes

### Option B — Hugging Face Spaces

1. Create a new Space at [huggingface.co/spaces](https://huggingface.co/spaces)
2. Select **Streamlit** SDK
3. Clone the Space repo and push all files

---

## Auto-Update Setup (GitHub Actions)

The scanner runs automatically every Sunday at 06:00 UTC.

**Optional: Get a free NCBI API key** for 10x faster scans:
1. Register at https://www.ncbi.nlm.nih.gov/account/
2. Go to Settings → API Key Management → Create API Key
3. In your GitHub repo: Settings → Secrets → Actions → New secret
   - Name: `NCBI_API_KEY`
   - Value: your key

**To trigger a manual scan:**
- Go to your repo → Actions → "Weekly CADD Tools Auto-Scan" → Run workflow

---

## How the Scanner Works

```
Every Sunday (or on-demand)
  ├── PubMed Entrez API
  │     • Searches 11 target journals
  │     • Keywords: "open source" + "github" + drug discovery terms
  │     • Returns title, authors, DOI, abstract
  │
  ├── CrossRef API
  │     • Searches by journal ISSN + keyword
  │     • Catches papers not in PubMed
  │
  ├── Confidence scoring (0–1)
  │     • Tool keywords: github.com, open source, pip install, etc.
  │     • Domain keywords: docking, ADMET, PROTAC, generative, etc.
  │     • Threshold: 0.35 to be flagged as candidate
  │
  └── Pending Review queue
        • Candidates appear in the app's "Pending Review" tab
        • You edit fields → Approve or Reject
        • Approved tools join the main database instantly
```

---

## Project Structure

```
cadd_tracker/
├── app.py                    ← Streamlit web app (main entry point)
├── requirements.txt
├── data/
│   ├── tools.json            ← Main approved tools database
│   ├── pending.json          ← Auto-scan candidates awaiting review
│   └── scan_history.json     ← Tracks seen DOIs & last scan time
├── utils/
│   ├── scanner.py            ← PubMed + CrossRef auto-scanner
│   └── export.py             ← Excel / CSV export utilities
└── .github/
    └── workflows/
        └── weekly_scan.yml   ← GitHub Actions scheduled workflow
```

---

## Journals Monitored

- Journal of Chemical Information and Modeling (ACS)
- Journal of Cheminformatics (Springer)
- Journal of Medicinal Chemistry (ACS)
- Molecular Informatics (Wiley)
- Journal of Chemical Theory and Computation (ACS)
- Bioinformatics (Oxford)
- Briefings in Bioinformatics (Oxford)
- Chemical Science (RSC)
- Nature Machine Intelligence
- ACS Medicinal Chemistry Letters
- Scientific Reports (Nature)

---

## Adding a Tool Manually

Edit `data/tools.json` and add an entry following this schema:

```json
{
  "tool_name": "MyTool",
  "task": "What it does",
  "category": "Molecular Docking",
  "year": 2024,
  "authors": "Smith J et al.",
  "doi": "10.1021/acs.jcim.4c00000",
  "journal": "Journal of Chemical Information and Modeling",
  "github": "https://github.com/author/mytool",
  "language": "Python",
  "open_source": true,
  "license": "MIT",
  "molecule_type": "Small Molecules",
  "role": "Hit identification / Virtual screening",
  "key_features": "GPU-accelerated; deep learning scoring",
  "dependencies": "PyTorch, RDKit",
  "status": "approved",
  "notes": "Optional notes"
}
```

---

## License

MIT License — free for academic and commercial use.
