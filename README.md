# Coding Agents in the Wild

**Replication package for:**

*Coding Agents in the Wild: Failure Modes and Rejection Patterns of AI-Generated Pull Requests*  
Mahd Hindi, Yasir Mahmood, Linda Mohammed, Salah Bouktif, Mohamed Mediani  
IEEE Access, 2026

---

## Overview

This repository contains the replication package for our empirical study analyzing 12,433 agent-generated pull requests across 1,495 GitHub repositories. The package includes scripts and notebooks to reproduce all datasets, tables, and figures reported in the paper using the **AIDev** dataset from Hugging Face.

### Key Outputs

From the Hugging Face dataset, this package reconstructs:

- PR-level dataset of agent-generated PRs in repositories with **≥500 stars** (through 2025-08-01)
- Review-comment datasets for rejected agent PRs
- Task-type classifications and rejection taxonomies
- Ground-truth labeling datasets used in qualitative annotation

> **Important:** Generated/derived outputs are **not** committed to GitHub. They can be large, may trigger secret scanners, and are meant to be reproduced locally.

---

## Data Source

This replication package uses:
- **Dataset:** `hao-li/AIDev` (Hugging Face)
- Tables are downloaded automatically via the `datasets`/`huggingface_hub` libraries when running scripts

---

## Repository Structure
```
coding-agents-wild/
├── config/
│   └── config.yaml              # Main configuration: dataset id, paths, filters
├── scripts/
│   ├── 00_sanity_check_tables.py
│   ├── 01_build_aidev_pop_agent_prs.py
│   ├── 02_build_review_comments_with_task_type.py
│   ├── 03_build_commented_raprs_pr_level.py
│   ├── 06_export_ground_truth_200_review_comments.py
│   └── 07_final_blocking_comment_per_pr.py
├── notebooks/                   # Optional Jupyter notebooks for exploration
├── data/
│   ├── raw/                     # Optional local cache (git-ignored)
│   └── derived/                 # Generated datasets (git-ignored)
├── outputs/                     # Generated tables/figures (git-ignored)
├── requirements.txt
└── README.md
```

---

## Requirements

### Python Environment
- **Python 3.12** (recommended)
  - Newer versions (e.g., 3.14) may require build tools on Windows due to source compilation

### Operating System
- Windows, macOS, or Linux

### Resources
- **Disk space:** Several GB for dataset cache
- **Time:** Variable depending on network and disk speed

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/mahdhindi/coding-agents-wild.git
cd coding-agents-wild
```

### 2. Create Virtual Environment

**Windows (PowerShell/CMD):**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## Reproduction Pipeline

Run the following scripts **in order** to reproduce the main results:

### Step 0: Sanity Check

Validates that required Hugging Face tables exist and schemas are correct.
```bash
python scripts/00_sanity_check_tables.py
```

### Step 1: Build PR-Level Agent Dataset

Produces the main PR-level dataset (repos with ≥500 stars).
```bash
python scripts/01_build_aidev_pop_agent_prs.py
```

**Output:** `data/derived/aidev_pop_ge500_agent_prs.csv`

### Step 2: Build Review Comments with Task Types

Joins review comments to rejected agent PRs and infers task types from PR titles.
```bash
python scripts/02_build_review_comments_with_task_type.py
```

**Output:** `data/derived/aidev_pop_ge500_pr_review_comments_with_task_type.csv`

### Step 3: Build PR-Level Commented Rejected APRs

Aggregates comment-level data into PR-level dataset for commented rejected agent PRs.
```bash
python scripts/03_build_commented_raprs_pr_level.py
```

**Output:** `data/derived/aidev_pop_ge500_commented_raprs_pr_level.csv`

---

## Optional: Ground-Truth Labeling Workflow

These scripts support the ground-truth 200-sample workflow used for taxonomy validation.

### Step 6: Export Review Comments for Ground-Truth PRs
```bash
python scripts/06_export_ground_truth_200_review_comments.py
```

### Step 7: Export Final Blocking Comments
```bash
python scripts/07_final_blocking_comment_per_pr.py
```

### Step 8: Create Labeling Sheet

Generate a CSV template for manual annotation:
```bash
python -c "import pandas as pd; p='data/derived/ground_truth_200_final_blocking_comment.csv'; df=pd.read_csv(p); keep=['full_name','number','agent_type','task_type','final_comment_time','path','final_blocking_comment']; keep=[c for c in keep if c in df.columns]; out=df[keep].copy(); out['manual_label']=''; out['manual_bucket']=''; out['notes']=''; out['labeler']=''; out['label_time']=''; out.to_csv('data/derived/ground_truth_200_labeling_sheet.csv', index=False); print('Wrote: data/derived/ground_truth_200_labeling_sheet.csv')"
```

**Output:** `data/derived/ground_truth_200_labeling_sheet.csv`

---

## Running Notebooks (Optional)

To explore the data interactively:
```bash
python -m pip install jupyter
jupyter notebook
```

Navigate to the `notebooks/` directory in the Jupyter interface.

---

## Configuration

Edit `config/config.yaml` to customize:

- **Dataset ID:** Hugging Face dataset (default: `hao-li/AIDev`)
- **Minimum stars:** Repository star threshold (default: 500)
- **Agent list:** Types of coding agents to include
- **Output paths:** Locations for derived data and outputs

---

## Git Tracking Policy

**Generated artifacts are not committed to version control:**

- `data/derived/` — Generated datasets (git-ignored)
- `outputs/` — Generated tables and figures (git-ignored)

**Rationale:**
- Large machine-generated CSVs can trigger GitHub secret scanning (false positives)
- Bloats repository size
- Complicates replication

This repository tracks **code and configuration only**. All results are reproduced locally.

---

## Citation

If you use this replication package, please cite:
```bibtex
@article{hindi2026codingagents,
  title     = {Coding Agents in the Wild: Failure Modes and Rejection Patterns 
               of AI-Generated Pull Requests},
  author    = {Hindi, Mahd and Mahmood, Yasir and Mohammed, Linda and 
               Bouktif, Salah and Mediani, Mohamed},
  journal   = {IEEE Access},
  year      = {2026},
  note      = {Replication package: https://github.com/mahdhindi/coding-agents-wild}
}
```

Please also cite the **AIDev dataset** according to its Hugging Face page and associated publications.

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Contact

For questions or issues regarding this replication package:

**Mahd Hindi**  
📧 mahmoud.alhindi@gmail.com