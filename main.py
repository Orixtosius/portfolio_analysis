from portfolio_analysis.utils import read_csv

config = {
    "filepath_or_buffer": "data/historical_data.csv"
}
df = read_csv(config)
print(df)