from datetime import date
import time
from context import *
from portfolio_analysis.core.data_reading import DataReader

class TestAnalyser(unittest.TestCase):

    def setUp(self) -> None:
        self.reader = DataReader()

    def test_read_single_ticker(self):
        config = {
            "tickers": ["AMD"],
            "start": int(time.mktime(date(2023, 9, 1).timetuple())),
            "end": int(time.mktime(date(2024, 9, 1).timetuple())),
            "interval": "1d",
        }
        df = self.reader(config)
        self.assertIsInstance(df, pd.DataFrame)

    def test_read_multiple_ticker(self):
        config = {
            "tickers": ["AMD", "TSLA"],
            "start": int(time.mktime(date(2023, 9, 1).timetuple())),
            "end": int(time.mktime(date(2024, 9, 1).timetuple())),
            "interval": "1d",
        }
        df = self.reader(config)
        self.assertIsInstance(df, pd.DataFrame)