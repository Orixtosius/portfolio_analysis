import time
from datetime import date
from portfolio_analysis.pipeline_management import PipelineManager



if __name__ == "__main__":
    config = {
#        "data_source": "data/historical_data.csv",
        "data_source":{
            "tickers": ["AMD", "TSLA"],
            "start": int(time.mktime(date(2023, 9, 1).timetuple())),
            "end": int(time.mktime(date(2024, 9, 1).timetuple())),
            "interval": "1d",
        },
        "transformer": {"stock_column": "Ticker", "price_column": "Close"}       
    }   
    manager = PipelineManager()
    manager(config)