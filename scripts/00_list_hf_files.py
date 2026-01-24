from huggingface_hub import list_repo_files

DATASET = "hao-li/AIDev"

def main():
    files = list_repo_files(DATASET, repo_type="dataset")
    # Print only parquet-ish files to keep output readable
    for f in files:
        if f.endswith(".parquet") or "parquet" in f.lower() or "review" in f.lower() or "comment" in f.lower():
            print(f)

if __name__ == "__main__":
    main()
