from portfolio_analysis.pipeline_management import PipelineManager



if __name__ == "__main__":
    config = {
        "data_source":{"filepath_or_buffer": "data/historical_data.csv"},
        "transformer": {"stock_column": "Ticker", "price_column": "Close"}       
    }   
    manager = PipelineManager()
    manager(config)