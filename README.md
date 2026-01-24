# coding-agents-wild

Replication package for: **Coding Agents in the Wild: Failure Modes and Rejection Patterns of AI-Generated Pull Requests**  
Mahd Hindi, Yasir Mahmood, Linda Mohammed, Salah Bouktif, Mohammed Mediani  
(IEEE Access, 2026)

This repository contains code to reproduce the main datasets and analyses used in the paper, using the **AIDev** dataset hosted on Hugging Face.

---

## Repository structure

- `config/` — configuration (Hugging Face dataset id, table names, output paths)
- `scripts/` — reproducible pipeline scripts (00–07)
- `notebooks/` — analysis / plotting notebooks (optional)
- `data/derived/` — generated CSV outputs (ignored by git via `.gitignore`)
- `outputs/` — generated figures/tables (may be ignored depending on size)

> Note: large derived artifacts are intentionally not tracked in Git to keep the repo lightweight and avoid accidental secret scanning / large file pushes.

---

## Data source

We use the Hugging Face dataset:

- **Hugging Face:** `hao-li/AIDev`

Your scripts read directly from Hugging Face via the dataset id in `config/config.yaml`.

---

## Setup (Windows / macOS / Linux)

### 1) Create and activate a virtual environment

**Windows (cmd):**
```bat
python -m venv .venv
.venv\Scripts\activate
