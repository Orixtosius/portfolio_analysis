from context import *
from sklearn.pipeline import Pipeline
from portfolio_analysis.core.anaylsis.sharpe_ratio import SharpeRatioAnalyser

class TestAnalyser(unittest.TestCase):


    def test_calculate_mean_and_cov(self):
        columns = ["Close_AAPL", "Close_XXX", "Close_YYY"]
        input_data = pd.DataFrame(data=[
            [27.33, 26.51, 26.80],
            [26.56, 26.56, 26.93],
            [26.59, 26.56, 26.93],
        ], columns=columns)
        steps = [("analyser", SharpeRatioAnalyser())]
        p = Pipeline(steps=steps)
        result = p.fit_transform(input_data)
        self.assertIsInstance(result, dict)