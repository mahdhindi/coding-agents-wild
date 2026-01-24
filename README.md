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

### 2) Create + activate a virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate

### 3) Install dependencies
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt


## Reproduction pipeline (run in this order)

###Step 0 — Sanity check the Hugging Face tables

- Validates that required tables exist and basic schemas look correct.
```bash
python scripts/00_sanity_check_tables.py

### Step 1 — Build PR-level agent dataset (≥ 500 stars)
- Produces the main PR-level file used throughout the analysis.
```bash
python scripts/01_build_aidev_pop_agent_prs.py
- Expected output (written locally):
  - data/derived/aidev_pop_ge500_agent_prs.csv

### Step 2 — Build review comments dataset + task_type
- Joins review comments to rejected APRs and infers task types from PR titles.
``` bash
python scripts/02_build_review_comments_with_task_type.py
- Expected output:
  - data/derived/aidev_pop_ge500_pr_review_comments_with_task_type.csv

### Step 3 — Build PR-level “commented rejected APRs” dataset
- Aggregates comment-level data into a PR-level dataset for commented rejected APRs.
```bash
python scripts/03_build_commented_raprs_pr_level.py
- Expected output:
  - data/derived/aidev_pop_ge500_commented_raprs_pr_level.csv

## Optional: Ground-truth sampling + exports (for qualitative labeling)
- These scripts support the ground-truth 200 workflow.
### Step 6 — Export review comments for ground-truth 200 PRs
```bash
python scripts/06_export_ground_truth_200_review_comments.py
### Step 7 — Export final blocking comment per PR (ground-truth 200)
```bash
python scripts/07_final_blocking_comment_per_pr.py

- Create a labeling sheet (CSV) from the final blocking comments file
```bash
python -c "import pandas as pd; p='data/derived/ground_truth_200_final_blocking_comment.csv'; df=pd.read_csv(p); keep=['full_name','number','agent_type','task_type','final_comment_time','path','final_blocking_comment']; keep=[c for c in keep if c in df.columns]; out=df[keep].copy(); out['manual_label']=''; out['manual_bucket']=''; out['notes']=''; out['labeler']=''; out['label_time']=''; out.to_csv('data/derived/ground_truth_200_labeling_sheet.csv', index=False); print('Wrote: data/derived/ground_truth_200_labeling_sheet.csv')"

## Running the notebooks (optional)
```bash
python -m pip install jupyter
jupyter notebook

## Configuration
- Edit config/config.yaml to change:
  - Hugging Face dataset id (default: hao-li/AIDev)
  - min_stars (default: 500)
  - agent list
 - output paths under paths

## Git tracking policy (important)
- data/derived/ and outputs/ are generated artifacts and should not be committed.
- Large machine-generated CSVs can:
  - trigger GitHub secret scanning (false positives happen),
  - bloat the repo
  - make replication harder.
This repo keeps code + configs in Git, and keeps generated results local.

## Citation
If you use this replication package, please cite the paper:
```bash
@article{hindi2026codingagents,
  title     = {Coding Agents in the Wild: Failure Modes and Rejection Patterns of AI-Generated Pull Requests},
  author    = {Hindi, Mahd and Mahmood, Yasir and Mohammed, Linda and Bouktif, Salah and Mediani, Mohamed},
  journal   = {IEEE Access},
  year      = {2026},
  note      = {Replication package: https://github.com/mahdhindi/coding-agents-wild}
}
- Please also cite the AIDev dataset according to its Hugging Face page and/or associated paper.

## License
MIT License. See LICENSE.

## Contact
For questions or issues:
  - Mahmoud AlHindi — mahmoud.alhindi@gmail.com
