# coding-agents-failure-modes
Replication package for: Coding Agents in the Wild: Failure Modes and Rejection Patterns of AI-Generated Pull Requests
# Coding Agents in the Wild: Failure Modes and Rejection Patterns

Replication package for the paper:

**"Coding Agents in the Wild: Failure Modes and Rejection Patterns of AI-Generated Pull Requests"**

Mahd Hindi, Yasir Mahmood, Linda Mohammed, Salah Bouktif, Mohammed Mediani

Published in IEEE Access, 2026.

## Overview

This repository contains the code and data used to analyze agent-generated 
pull requests (APRs) in popular GitHub repositories using the AIDev-POP dataset.

## Repository Structure

- `notebooks/` - Jupyter/Colab notebooks for data analysis
- `data/` - Processed datasets (or instructions to obtain them)
- `scripts/` - Python scripts for data processing
- `results/` - Generated figures and tables

## Requirements

- Python 3.8+
- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn

Install dependencies:
```bash
pip install pandas numpy scikit-learn matplotlib seaborn
```

## Data

The analysis uses the AIDev dataset available on Hugging Face:
https://huggingface.co/datasets/[dataset-path]

## Usage

1. Open `notebooks/AIDev_POP.ipynb` in Google Colab or Jupyter
2. Follow the cells sequentially to reproduce the analysis

## Citation

If you use this code, please cite:
```bibtex
@article{hindi2026coding,
  title={Coding Agents in the Wild: Failure Modes and Rejection Patterns of AI-Generated Pull Requests},
  author={Hindi, Mahd and Mahmood, Yasir and Mohammed, Linda and Bouktif, Salah and Mediani, Mohammed},
  journal={IEEE Access},
  year={2026},
  publisher={IEEE}
}
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions, contact: [your email or advisor's email]
