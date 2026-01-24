import os
import yaml
import pandas as pd

def main():
    cfg = yaml.safe_load(open("config/config.yaml", "r", encoding="utf-8"))
    derived_dir = cfg["paths"]["derived_dir"]
    os.makedirs(derived_dir, exist_ok=True)

    sample_path = os.path.join(derived_dir, "ground_truth_200_commented_raprs_pr_level.csv")
    comments_path = os.path.join(derived_dir, "aidev_pop_ge500_pr_review_comments_with_task_type.csv")

    if not os.path.exists(sample_path):
        raise FileNotFoundError(f"Missing {sample_path}. Run script 05 first.")
    if not os.path.exists(comments_path):
        raise FileNotFoundError(f"Missing {comments_path}. Run script 02 first.")

    print("=== Export review comments for ground-truth 200 PRs ===")
    print("Sample:", sample_path)
    print("Comments:", comments_path)

    sample = pd.read_csv(sample_path, low_memory=False)
    comments = pd.read_csv(comments_path, low_memory=False)

    # Required join keys
    for col in ["full_name", "number"]:
        if col not in sample.columns:
            raise ValueError(f"Sample missing '{col}'. Columns: {list(sample.columns)}")
        if col not in comments.columns:
            raise ValueError(f"Comments missing '{col}'. Columns: {list(comments.columns)}")

    # Normalize types
    sample["full_name"] = sample["full_name"].astype(str)
    comments["full_name"] = comments["full_name"].astype(str)

    sample["number"] = pd.to_numeric(sample["number"], errors="coerce")
    comments["number"] = pd.to_numeric(comments["number"], errors="coerce")
    sample = sample.dropna(subset=["number"])
    comments = comments.dropna(subset=["number"])
    sample["number"] = sample["number"].astype("int64")
    comments["number"] = comments["number"].astype("int64")

    keys = sample[["full_name", "number"]].drop_duplicates()

    # Filter comments down to only those PRs
    gt_comments = comments.merge(keys, on=["full_name", "number"], how="inner")

    # Optional: sort chronologically if timestamps exist
    if "created_at_comment" in gt_comments.columns:
        gt_comments = gt_comments.sort_values(["full_name", "number", "created_at_comment"])
    elif "created_at" in gt_comments.columns:
        gt_comments = gt_comments.sort_values(["full_name", "number", "created_at"])

    out_path = os.path.join(derived_dir, "ground_truth_200_review_comments.csv")
    gt_comments.to_csv(out_path, index=False)

    print("✅ Wrote:", out_path)
    print("Rows (comments):", len(gt_comments))
    print("Unique PRs:", gt_comments[["full_name", "number"]].drop_duplicates().shape[0])

    # quick check of comment volume distribution
    per_pr = gt_comments.groupby(["full_name", "number"]).size()
    print("\nComment count per PR (summary):")
    print(per_pr.describe())

if __name__ == "__main__":
    main()
