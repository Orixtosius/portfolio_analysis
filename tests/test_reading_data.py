from context import *
from portfolio_analysis.utils import read_csv


class TestReader(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def test_read_csv(self):
        config = {
            "filepath_or_buffer": "data/historical_data.csv"
        }
        df = read_csv(config)
        self.assertIsInstance(df, pd.DataFrame)