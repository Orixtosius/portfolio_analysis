import pandas as pd


class DataReader:

    def _read_from_yahoo(self, config: dict) -> pd.DataFrame:
        tickers = config["tickers"]
        start = config["start"]
        end = config["end"]
        interval = config["interval"]
        base_link = "https://query1.finance.yahoo.com/v7/finance/download/"
        end_link = "&events=history&includeAdjustedClose=true"
        df_list = [
            self._read_from_csv(f"{base_link}{ticker}?period1={start}&period2={end}&interval={interval}{end_link}")
            for ticker in tickers
        ]
        return pd.concat(df_list, axis=0)

    def _read_from_csv(self, source: str) -> pd.DataFrame:
        return pd.read_csv(source)
    
    def __call__(self, source: str | dict) -> pd.DataFrame:
        """Factory method for reading"""
        if isinstance(source, str):
            return self._read_from_csv(source)
        elif isinstance(source, dict):
            return self._read_from_yahoo(source)
        else:
            raise ValueError(f"Given source type: {type(source)} is not recognized.")