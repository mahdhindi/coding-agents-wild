import os
import yaml
import numpy as np
import pandas as pd
from utils_hf import read_parquet_hf

AGENT_COL_CANDIDATES = ["agent", "agent_type"]
REPO_ID_COL = "repo_id"

def derive_outcome(df: pd.DataFrame) -> pd.Series:
    # MERGED if merged_at exists, REJECTED if closed and not merged, else OPEN
    merged = df["merged_at"].notna()
    closed = df["state"].astype(str).str.lower().eq("closed")
    outcome = np.where(merged, "MERGED", np.where(closed, "REJECTED", "OPEN"))
    return pd.Series(outcome, index=df.index, name="pr_outcome")

def to_datetime_safe(s: pd.Series) -> pd.Series:
    return pd.to_datetime(s, errors="coerce", utc=True)

def main():
    cfg = yaml.safe_load(open("config/config.yaml", "r", encoding="utf-8"))
    ds = cfg["aidev_hf_dataset"]
    t = cfg["tables"]
    min_stars = int(cfg["min_stars"])
    agents = set(cfg["agents"])
    derived_dir = cfg["paths"]["derived_dir"]
    os.makedirs(derived_dir, exist_ok=True)

    print("=== Build AIDev-POP Agent PRs (>=500 stars) ===")
    print("HF dataset:", ds)
    print("MIN_STARS:", min_stars)
    print("Agents:", sorted(list(agents)))

    # Load core tables
    pr = read_parquet_hf(ds, t["pull_request"])
    # Preserve dataset PR id if present (helps join with comments)
    if "id" in pr.columns:
    	pr = pr.rename(columns={"id": "id_pr"})

    repo = read_parquet_hf(ds, t["repository"])
    

    # Identify agent column
    agent_col = None
    for c in AGENT_COL_CANDIDATES:
        if c in pr.columns:
            agent_col = c
            break
    if agent_col is None:
        raise ValueError(f"Could not find agent column. Tried: {AGENT_COL_CANDIDATES}. "
                         f"Available columns: {list(pr.columns)}")

    # Filter popular repos
    if "stars" not in repo.columns:
        raise ValueError("Repository table missing 'stars' column.")
    popular_repo = repo.loc[repo["stars"] >= min_stars, ["id", "full_name", "stars"]].copy()
    popular_repo_ids = set(popular_repo["id"].astype("int64"))

    print("Popular repos:", len(popular_repo))

    # Filter PRs to popular repos (AIDev-POP)
    pr = pr.loc[pr[REPO_ID_COL].isin(popular_repo_ids)].copy()
    print("PRs in popular repos:", len(pr))

    # Standardize agent column -> agent_type and filter to target agents
    pr["agent_type"] = pr[agent_col].astype(str)
    pr = pr.loc[pr["agent_type"].isin(agents)].copy()
    print("Agent PRs (target agents):", len(pr))

    # Parse timestamps
    for col in ["created_at", "closed_at", "merged_at"]:
        if col in pr.columns:
            pr[col] = to_datetime_safe(pr[col])

    # Turnaround time (hours)
    pr["turnaround_time_hours"] = (pr["closed_at"] - pr["created_at"]).dt.total_seconds() / 3600.0

    # Outcome
    pr["pr_outcome"] = derive_outcome(pr)

    # Attach repo metadata
    # PR table uses repo_id; repository table uses id
    pr = pr.merge(popular_repo, left_on="repo_id", right_on="id", how="left", suffixes=("", "_repo"))
    # Avoid confusion: keep repo id as repo_id, drop duplicate "id" from repo table
    if "id_repo" in pr.columns:
        pr = pr.drop(columns=["id_repo"], errors="ignore")
    pr = pr.drop(columns=["id"], errors="ignore")  # repo id column from repo table merge

    # Reorder key columns first (keep the rest)
    key_cols = [
    "id_pr", "repo_id", "full_name", "stars",
    "number",
    "agent_type",
    "created_at", "closed_at", "merged_at",
    "turnaround_time_hours",
    "state", "pr_outcome",
    "title", "body"]

    existing_key_cols = [c for c in key_cols if c in pr.columns]
    remaining_cols = [c for c in pr.columns if c not in existing_key_cols]
    pr = pr[existing_key_cols + remaining_cols]

    out_path = os.path.join(derived_dir, "aidev_pop_ge500_agent_prs.csv")
    pr.to_csv(out_path, index=False)
    print("✅ Wrote:", out_path)
    print("Rows:", len(pr), "Cols:", len(pr.columns))
    print("Outcome counts:\n", pr["pr_outcome"].value_counts(dropna=False))
    print("Agent counts:\n", pr["agent_type"].value_counts(dropna=False))

if __name__ == "__main__":
    main()
