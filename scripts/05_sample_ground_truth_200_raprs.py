import os
import yaml
import pandas as pd

SEED = 2025  # fixed seed for reproducibility

def stratified_sample(df: pd.DataFrame, group_col: str, n_total: int, seed: int) -> pd.DataFrame:
    """
    Proportional stratified sampling by group_col.
    Guarantees sum to n_total by distributing rounding remainder by largest fractional parts.
    """
    counts = df[group_col].value_counts(dropna=False)
    props = counts / len(df)
    raw_targets = props * n_total

    base = raw_targets.apply(lambda x: int(x))  # floor
    remainder = n_total - base.sum()

    # distribute remainder by largest fractional parts
    frac = (raw_targets - base).sort_values(ascending=False)
    for g in frac.index[:remainder]:
        base.loc[g] += 1

    # sample per group
    parts = []
    for g, k in base.items():
        gdf = df[df[group_col] == g]
        if k == 0:
            continue
        if len(gdf) < k:
            raise ValueError(f"Group {g} has only {len(gdf)} rows, cannot sample {k}.")
        parts.append(gdf.sample(n=k, random_state=seed))
    out = pd.concat(parts, ignore_index=True)

    # shuffle for nicer viewing
    out = out.sample(frac=1.0, random_state=seed).reset_index(drop=True)
    return out

def main():
    cfg = yaml.safe_load(open("config/config.yaml", "r", encoding="utf-8"))
    derived_dir = cfg["paths"]["derived_dir"]
    os.makedirs(derived_dir, exist_ok=True)

    in_path = os.path.join(derived_dir, "aidev_pop_ge500_commented_raprs_pr_level.csv")
    if not os.path.exists(in_path):
        raise FileNotFoundError(f"Missing {in_path}. Run script 03 first.")

    df = pd.read_csv(in_path, low_memory=False)

    # Expect agent column in PR metadata (from script 01 merge)
    # In your PR CSV, agent column appears as 'agent_type'
    if "agent_type" not in df.columns:
        raise ValueError(f"Missing 'agent_type' in {in_path}. Columns: {list(df.columns)}")

    # Basic cleaning
    df["agent_type"] = df["agent_type"].astype(str)

    # Sample 200 PRs
    gt = stratified_sample(df, group_col="agent_type", n_total=200, seed=SEED)

    # Minimal manifest columns (stable identifiers)
    keep_cols = []
    for c in ["full_name", "number", "repo_id", "html_url", "repo_url", "agent_type", "created_at", "closed_at", "title", "body"]:
        if c in gt.columns:
            keep_cols.append(c)

    # Always keep the main join keys
    for c in ["full_name", "number", "agent_type"]:
        if c not in keep_cols and c in gt.columns:
            keep_cols.append(c)

    gt_out = gt[keep_cols].copy() if keep_cols else gt.copy()

    out_path = os.path.join(derived_dir, "ground_truth_200_commented_raprs_pr_level.csv")
    gt_out.to_csv(out_path, index=False)

    # Save counts + seed for replication
    manifest_path = os.path.join(derived_dir, "ground_truth_200_manifest.txt")
    counts = gt_out["agent_type"].value_counts().to_string()

    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write("Ground-truth sampling manifest\n")
        f.write(f"Seed: {SEED}\n")
        f.write("Source: aidev_pop_ge500_commented_raprs_pr_level.csv\n")
        f.write("Stratified by: agent_type (proportional)\n\n")
        f.write("Counts per agent:\n")
        f.write(counts + "\n")

    print("✅ Wrote:", out_path)
    print("✅ Wrote:", manifest_path)
    print("\nCounts per agent:\n", gt_out["agent_type"].value_counts())

if __name__ == "__main__":
    main()
