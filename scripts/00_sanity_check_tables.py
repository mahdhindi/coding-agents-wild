import yaml
from utils_hf import read_parquet_hf

REQUIRED_PR_COLS = {
    "id", "repo_id", "created_at", "closed_at", "state", "merged_at", "agent"
}
REQUIRED_REPO_COLS = {
    "id", "full_name", "stars"
}

def main():
    cfg = yaml.safe_load(open("config/config.yaml", "r", encoding="utf-8"))
    dataset_path = cfg["aidev_hf_dataset"]
    tables = cfg["tables"]

    print("=== AIDev sanity check ===")
    print("HF dataset:", dataset_path)

    pr = read_parquet_hf(dataset_path, tables["pull_request"])
    repo = read_parquet_hf(dataset_path, tables["repository"])

    missing_pr = REQUIRED_PR_COLS - set(pr.columns)
    missing_repo = REQUIRED_REPO_COLS - set(repo.columns)

    if missing_pr:
        raise ValueError(f"Missing PR columns: {sorted(missing_pr)}")
    if missing_repo:
        raise ValueError(f"Missing repository columns: {sorted(missing_repo)}")

    print("✅ Schema sanity checks passed.")
    print("PR rows:", len(pr))
    print("Repo rows:", len(repo))
    print("PR columns:", len(pr.columns))
    print("Repo columns:", len(repo.columns))

if __name__ == "__main__":
    main()
