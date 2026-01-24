import os
import yaml
import pandas as pd

def main():
    cfg = yaml.safe_load(open("config/config.yaml", "r", encoding="utf-8"))
    derived_dir = cfg["paths"]["derived_dir"]
    os.makedirs(derived_dir, exist_ok=True)

    comments_path = os.path.join(derived_dir, "aidev_pop_ge500_pr_review_comments_with_task_type.csv")
    pr_path = os.path.join(derived_dir, "aidev_pop_ge500_agent_prs.csv")

    if not os.path.exists(comments_path):
        raise FileNotFoundError(f"Missing {comments_path}. Run script 02 first.")
    if not os.path.exists(pr_path):
        raise FileNotFoundError(f"Missing {pr_path}. Run script 01 first.")

    print("=== Build PR-level commented RAPRs dataset ===")
    print("Reading:", comments_path)
    dfc = pd.read_csv(comments_path, low_memory=False)

    # Required keys
    for col in ["full_name", "number"]:
        if col not in dfc.columns:
            raise ValueError(f"Comments CSV missing '{col}'. Columns: {list(dfc.columns)}")

    dfc["full_name"] = dfc["full_name"].astype(str)
    dfc["number"] = pd.to_numeric(dfc["number"], errors="coerce")
    dfc = dfc.dropna(subset=["number"])
    dfc["number"] = dfc["number"].astype("int64")

    # Build per-PR aggregates from comment-level
    per_pr = (
        dfc.groupby(["full_name", "number"], as_index=False)
           .agg(
               n_comments=("body", "count") if "body" in dfc.columns else ("full_name", "count"),
               n_unique_commenters=("user", "nunique") if "user" in dfc.columns else ("full_name", "count"),
               first_comment_at=("created_at", "min") if "created_at" in dfc.columns else ("full_name", "count"),
               last_comment_at=("created_at", "max") if "created_at" in dfc.columns else ("full_name", "count"),
               task_type_majority=("task_type", lambda s: s.value_counts().index[0]) if "task_type" in dfc.columns else ("full_name", "count"),
           )
    )

    # Merge PR-level metadata from Script 01 output
    print("Reading:", pr_path)
    pr = pd.read_csv(pr_path, low_memory=False)

    if "full_name" not in pr.columns or "number" not in pr.columns:
        raise ValueError(f"PR CSV missing full_name/number. Columns: {list(pr.columns)}")

    pr["full_name"] = pr["full_name"].astype(str)
    pr["number"] = pd.to_numeric(pr["number"], errors="coerce")
    pr = pr.dropna(subset=["number"])
    pr["number"] = pr["number"].astype("int64")

    # Keep only rejected PRs
    if "pr_outcome" in pr.columns:
        pr = pr.loc[pr["pr_outcome"] == "REJECTED"].copy()

    out = per_pr.merge(pr, on=["full_name", "number"], how="left", suffixes=("", "_pr"))

    out_path = os.path.join(derived_dir, "aidev_pop_ge500_commented_raprs_pr_level.csv")
    out.to_csv(out_path, index=False)

    print("✅ Wrote:", out_path)
    print("Rows (unique commented RAPRs):", len(out))
    print("Top task types:\n", out["task_type_majority"].value_counts(dropna=False).head(15) if "task_type_majority" in out.columns else "n/a")

if __name__ == "__main__":
    main()
