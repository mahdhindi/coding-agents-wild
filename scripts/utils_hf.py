import pandas as pd

def read_parquet_hf(dataset_path: str, table_name: str) -> pd.DataFrame:
    """
    Read a Parquet table from Hugging Face using pandas.
    Expected URI format: hf://datasets/<dataset_path>/<table_name>

    Note: If the dataset stores files in subfolders, adjust the URI here ONCE,
    and all scripts will work.
    """
    uri = f"hf://datasets/{dataset_path}/{table_name}"
    return pd.read_parquet(uri)
