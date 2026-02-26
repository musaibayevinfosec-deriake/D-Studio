import pandas as pd

def read_csv(path: str) -> pd.DataFrame:
    # dtype=str -> cleaning üçün rahat (sonradan cast edərsən)
    return pd.read_csv(path, dtype=str, keep_default_na=False)

def write_csv(df: pd.DataFrame, path: str) -> None:
    df.to_csv(path, index=False, encoding="utf-8")
