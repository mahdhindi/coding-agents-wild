import os
import re
import yaml
import pandas as pd

TRIVIAL_PATTERNS = [
    r"^\s*$",
    r"^\s*(lgtm|looks good to me)\s*[.!]?\s*$",
    r"^\s*(thanks|thank you)\s*[.!]?\s*$",
    r"^\s*(done|fixed|resolved)\s*[.!]?\s*$",
    r"^\s*(\+1|👍)\s*$",
]

def is_substantive(text: str) -> bool:
    if text is None:
        return False
    t = str(text).strip()
    if not t:
        return False
    low = t.lower()
    for p in TRIVIAL_PATTERNS:
        if re.match(p, low):
            return False
    # Too short is usually not useful as a "blocking reason"
    if len(t) < 20:
        return False
    return True

def pick_final_substantive(group: pd.DataFrame, body_col: str, time_col: str) -> pd.Series:
    # group already sorted by time
    # Walk backwards and pick last substantive comment
    for i in range(len(group) - 1, -1, -1):
        row = group.iloc[i]
        if is_substantive(row.get(body_col, "")):
            return row
    # fallback: last row even if trivial (rare)
    return group.iloc[-1]

def main():
    cfg = yaml.safe_load(open("config/config.yaml", "r", encoding="utf-8"))
    derived_dir = cfg["paths"]["derived_dir"]
    os.makedirs(derived_dir, exist_ok=True)

    in_path = os.path.join(derived_dir, "ground_truth_200_review_comments.csv")
    if not os.path.exists(in_path):
        raise FileNotFoundError(f"Missing {in_path}. Run script 06 first.")

    df = pd.read_csv(in_path, low_memory=False)

    # Keys
    for c in ["full_name", "number"]:
        if c not in df.columns:
            raise ValueError(f"Missing '{c}' in {in_path}. Columns: {list(df.columns)}")

    # Choose the best available timestamp column
    time_col = None
    for cand in ["created_at_comment", "created_at", "updated_at", "updated_at_comment"]:
        if cand in df.columns:
            time_col = cand
            break
    if time_col is None:
        raise ValueError(
            "No timestamp column found. Need one of: created_at_comment, created_at, updated_at, updated_at_comment"
        )

    # Choose body column
    body_col = None
    for cand in ["body_comment", "body", "comment_body"]:
        if cand in df.columns:
            body_col = cand
            break
    if body_col is None:
        raise ValueError(f"No comment body column found. Columns: {list(df.columns)}")

    # Normalize
    df["full_name"] = df["full_name"].astype(str)
    df["number"] = pd.to_numeric(df["number"], errors="coerce").dropna().astype("int64")
    df[time_col] = pd.to_datetime(df[time_col], errors="coerce")

    # Sort and pick final substantive per PR
    df = df.sort_values(["full_name", "number", time_col])

    picked_rows = []
    for (repo, num), g in df.groupby(["full_name", "number"], sort=False):
        g = g.dropna(subset=[time_col])
        if len(g) == 0:
            continue
        picked = pick_final_substantive(g, body_col=body_col, time_col=time_col)
        picked_rows.append(picked)

    out = pd.DataFrame(picked_rows).copy()

    # Keep a clean minimal view for labeling
    keep_cols = []
    for c in ["full_name", "number", "agent_type", "task_type", time_col, body_col, "path", "diff_hunk", "position"]:
        if c in out.columns:
            keep_cols.append(c)

    out_min = out[keep_cols].copy() if keep_cols else out.copy()
    out_min = out_min.rename(columns={body_col: "final_blocking_comment", time_col: "final_comment_time"})

    out_path = os.path.join(derived_dir, "ground_truth_200_final_blocking_comment.csv")
    out_min.to_csv(out_path, index=False)

    print("✅ Wrote:", out_path)
    print("Rows (PRs):", len(out_min))
    print("Example rows:")
    print(out_min.head(3).to_string(index=False))

if __name__ == "__main__":
    main()
