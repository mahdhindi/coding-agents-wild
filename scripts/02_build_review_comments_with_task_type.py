import os
import yaml
import pandas as pd
from utils_hf import read_parquet_hf
from task_type_rules import infer_task_type

def main():
    cfg = yaml.safe_load(open("config/config.yaml", "r", encoding="utf-8"))
    ds = cfg["aidev_hf_dataset"]
    t = cfg["tables"]
    derived_dir = cfg["paths"]["derived_dir"]
    os.makedirs(derived_dir, exist_ok=True)

    pr_path = os.path.join(derived_dir, "aidev_pop_ge500_agent_prs.csv")
    if not os.path.exists(pr_path):
        raise FileNotFoundError(f"Missing {pr_path}. Run script 01 first.")

    print("=== Build review comments dataset + task_type ===")
    print("HF dataset:", ds)
    print("Loading PR-level CSV:", pr_path)

    pr = pd.read_csv(pr_path, low_memory=False)

    # Keep rejected PRs (RAPRs)
    rapr = pr.loc[pr["pr_outcome"] == "REJECTED"].copy()
    if "id_pr" not in rapr.columns:
    	raise ValueError("PR CSV missing 'id_pr'. Re-run script 01 after patching it to keep dataset PR id.")

    rapr_ids = set(pd.to_numeric(rapr["id_pr"], errors="coerce").dropna().astype("int64"))

    print("Rejected APRs (RAPRs):", len(rapr), "Unique PR IDs:", len(rapr_ids))

    # Load review comments table
    comments = read_parquet_hf(ds, t["review_comments"]).copy()

    # Try to find PR id column in comments
    pr_id_candidates = ["id_pr", "pr_id", "pull_request_id", "id"]
    pr_id_col = None
    for c in pr_id_candidates:
        if c in comments.columns:
            pr_id_col = c
            break
    if pr_id_col is None:
        raise ValueError(f"Cannot find PR id column in review comments table. "
                         f"Tried {pr_id_candidates}. Available columns: {list(comments.columns)}")

    # If the comments table has its own id column, we also want comment id
    # We'll keep all columns and rename safely later.
    # Filter to comments on rejected PRs only
    comments[pr_id_col] = pd.to_numeric(comments[pr_id_col], errors="coerce")
    comments = comments.loc[comments[pr_id_col].isin(rapr_ids)].copy()
    print("Review comments on RAPRs:", len(comments))

    # Merge PR-level metadata into each comment row
    # Ensure PR id key is named id_pr for consistency
    comments = comments.rename(columns={pr_id_col: "id_pr"})
    rapr_small = rapr.copy()
    rapr_small["id_pr"] = rapr_small["id"].astype("int64")

    merged = comments.merge(
        rapr_small,
        on="id_pr",
        how="left",
        suffixes=("_comment", "_pr")
    )

    # Derive task_type from PR title
    title_col = "title"
    if title_col in merged.columns:
        merged["task_type"] = merged[title_col].apply(infer_task_type)
    else:
        merged["task_type"] = "unknown"

    out_path = os.path.join(derived_dir, "aidev_pop_ge500_pr_review_comments_with_task_type.csv")
    merged.to_csv(out_path, index=False)
    print("✅ Wrote:", out_path)
    print("Rows:", len(merged), "Cols:", len(merged.columns))
    if "task_type" in merged.columns:
        print("Task type counts:\n", merged["task_type"].value_counts(dropna=False).head(20))

if __name__ == "__main__":
    main()
