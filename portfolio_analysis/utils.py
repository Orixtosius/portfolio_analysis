import pandas as pd


def read_csv(config: dict) -> pd.DataFrame:
    df = pd.read_csv(**config)
    return df