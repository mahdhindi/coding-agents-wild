# coding-agents-wild

Replication package for:

**Coding Agents in the Wild: Failure Modes and Rejection Patterns of AI-Generated Pull Requests**  
Mahd Hindi, Yasir Mahmood, Linda Mohammed, Salah Bouktif, Mohamed Mediani  
(IEEE Access, 2026)

This repository contains scripts and notebooks to reproduce the main datasets, tables, and figures reported in the paper, using the **AIDev** dataset from Hugging Face.

---

## What this repo produces (high-level)

From the Hugging Face dataset, we reconstruct:

- A PR-level dataset of agent-generated PRs in repos with **≥ 500 stars** (through **2025-08-01**).
- Review-comment datasets for rejected APRs and task-type labeling.
- A ground-truth labeling sheet and exports used in the taxonomy / qualitative annotation workflow.

> Important: Generated/derived outputs are **not** meant to be committed to GitHub (they can be huge, may trigger secret scanners, and are machine-produced). You generate them locally.

---

## Data source

This replication package uses the Hugging Face dataset:

- Dataset id: `hao-li/AIDev`

You will download tables through the `datasets` / `huggingface_hub` stack automatically when running the scripts.

---

## Repository structure

- `config/`  
  - `config.yaml` (main config: dataset id, tables, paths, filters)
- `scripts/`  
  - numbered scripts to reproduce derived datasets step-by-step
- `notebooks/`  
  - optional Jupyter notebooks (analysis / exploration)
- `data/`  
  - `data/raw/` (optional local cache or manually downloaded artifacts)
  - `data/derived/` (generated locally by scripts — **ignored by git**)
- `outputs/`  
  - generated tables/figures — **ignored by git**

---

## Requirements

### Recommended environment
- **Python 3.12** (this is what the repo config targets)
  - Newer versions (e.g., 3.14) can cause some packages to compile from source on Windows and fail unless build tools are installed.

### OS
- Windows / macOS / Linux should work. The instructions below include Windows-friendly commands.

### Disk & time
- The dataset is large. Expect **several GB** of cache and some scripts to take time depending on your network and disk speed.

---

## Quickstart (Windows / PowerShell or CMD)

### 1) Clone
```bash
git clone https://github.com/mahdhindi/coding-agents-wild.git
cd coding-agents-wild
