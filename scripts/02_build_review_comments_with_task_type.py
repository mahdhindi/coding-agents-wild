import os
import re
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

    # --- Keep rejected PRs (RAPRs) ---
    if "pr_outcome" not in pr.columns:
        raise ValueError(f"PR CSV missing pr_outcome. Columns: {list(pr.columns)}")
    if "full_name" not in pr.columns or "number" not in pr.columns:
        raise ValueError(f"PR CSV must include full_name and number. Columns: {list(pr.columns)}")

    rapr = pr.loc[pr["pr_outcome"] == "REJECTED"].copy()
    rapr["full_name"] = rapr["full_name"].astype(str)
    rapr["number"] = pd.to_numeric(rapr["number"], errors="coerce")
    rapr = rapr.dropna(subset=["number"])
    rapr["number"] = rapr["number"].astype("int64")

    print("Rejected APRs (RAPRs):", len(rapr))
    rapr_key = rapr[["full_name", "number"]].drop_duplicates()

    # --- Load review comments table ---
    comments = read_parquet_hf(ds, t["review_comments"]).copy()

    if "pull_request_url" not in comments.columns:
        raise ValueError(
            "Expected 'pull_request_url' in comments table.\n"
            f"Available columns: {list(comments.columns)}"
        )

    # --- Extract full_name and number from pull_request_url ---
    # Example: https://api.github.com/repos/OWNER/REPO/pulls/123
    pat = re.compile(r"repos/([^/]+/[^/]+)/pulls/(\d+)")
    extracted = comments["pull_request_url"].astype(str).str.extract(pat)

    comments["full_name"] = extracted[0]
    comments["number"] = pd.to_numeric(extracted[1], errors="coerce")

    comments = comments.dropna(subset=["full_name", "number"])
    comments["full_name"] = comments["full_name"].astype(str)
    comments["number"] = comments["number"].astype("int64")

    # --- Keep only comments on RAPRs ---
    comments = comments.merge(rapr_key, on=["full_name", "number"], how="inner")
    print("Review comments on RAPRs:", len(comments))

    # --- Merge PR-level metadata into each comment row ---
    merged = comments.merge(
        rapr,
        on=["full_name", "number"],
        how="left",
        suffixes=("_comment", "_pr")
    )

    # --- Derive task_type from PR title ---
    if "title" in merged.columns:
        merged["task_type"] = merged["title"].apply(infer_task_type)
    else:
        merged["task_type"] = "unknown"

    out_path = os.path.join(derived_dir, "aidev_pop_ge500_pr_review_comments_with_task_type.csv")
    merged.to_csv(out_path, index=False)

    print("✅ Wrote:", out_path)
    print("Rows:", len(merged), "Cols:", len(merged.columns))
    print("Task type counts:\n", merged["task_type"].value_counts(dropna=False).head(20))


if __name__ == "__main__":
    main()
