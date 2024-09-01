from context import *
from sklearn.pipeline import Pipeline
from portfolio_analysis.core.transformer.long_term_stock_wise import LongTermStockWiseTransformer
from pandas.testing import assert_frame_equal

class TestLTStockTransformer(unittest.TestCase):
    def setUp(self) -> None:
        self.columns = ["Date", "Ticker", "Open", "High", "Low", "Close", "AdjClose", "Volume"]
        self.expected_columns = ["Close_AAPL", "Close_XXX", "Close_YYY"]

    def set_up_equal_size_data(self):
        data = pd.DataFrame(data=[
            ["2015-01-02", "AAPL", 27.84, 27.86, 26.83,	27.33, 24.35, 212818400],
            ["2015-01-05", "AAPL", 27.07, 27.16, 26.35,	26.56, 23.60, 257142000],
            ["2015-01-02", "XXX", 26.63, 26.85, 26.15,	26.56, 23.62, 263188400],
            ["2015-01-05", "XXX", 26.56, 26.85, 26.15,	26.56, 23.62, 263188400],
            ["2015-01-02", "YYY", 26.79, 27.04, 26.67,	26.80, 24.03, 160423600],
            ["2015-01-05", "YYY", 26.93, 27.04, 26.67,	26.93, 24.03, 160423600],
        ], columns=self.columns)
        
        data['Date'] = pd.to_datetime(data['Date'])

        expected = pd.DataFrame(data=[
            [27.33, 26.56, 26.80],
            [26.56, 26.56, 26.93],
        ], columns=self.expected_columns)
        
        return data, expected
    
    def set_up_inequal_size_data(self):
        data = pd.DataFrame(data=[
            ["2015-01-02", "AAPL", 27.84, 27.86, 26.83,	27.33, 24.35, 212818400],
            ["2015-01-05", "AAPL", 27.07, 27.16, 26.35,	26.56, 23.60, 257142000],
            ["2015-01-06", "AAPL", 27.08, 27.17, 26.37,	26.59, 23.61, 257142000],
            ["2015-01-02", "XXX", 26.63, 26.85, 26.15,	26.51, 23.62, 263188400],
            ["2015-01-05", "XXX", 26.56, 26.85, 26.15,	26.56, 23.62, 263188400],
            ["2015-01-02", "YYY", 26.79, 27.04, 26.67,	26.80, 24.03, 160423600],
            ["2015-01-05", "YYY", 26.93, 27.04, 26.67,	26.93, 24.03, 160423600],
        ], columns=self.columns)
        
        data['Date'] = pd.to_datetime(data['Date'])

        expected = pd.DataFrame(data=[
            [27.33, 26.51, 26.80],
            [26.56, 26.56, 26.93],
            [26.59, 26.56, 26.93],
        ], columns=self.expected_columns)
        
        return data, expected

    def set_up_pipeline(self, data):
        steps = [("t1", LongTermStockWiseTransformer("Ticker", "Close"))]
        p = Pipeline(steps=steps)
        return p.fit_transform(data)
    
    def test_equal_size_stocks(self):
        data, expected = self.set_up_equal_size_data()
        transformed_data = self.set_up_pipeline(data)
        assert_frame_equal(transformed_data, expected)

    def test_inequal_size_stocks(self):
        data, expected = self.set_up_inequal_size_data()
        transformed_data = self.set_up_pipeline(data)
        assert_frame_equal(transformed_data, expected)