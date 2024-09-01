from portfolio_analysis.utils import read_csv
from sklearn.pipeline import Pipeline
from portfolio_analysis.core.anaylsis.sharpe_ratio import SharpeRatioAnalyser as SRA
from portfolio_analysis.core.transformer.long_term_stock_wise import LongTermStockWiseTransformer as LTS
from portfolio_analysis.core.printer import ResultPrinter


class PipelineManager:

    def __call__(self, config: dict) -> None:
        df = read_csv(config["data_source"])
        steps = [
            ("lts_transformer", LTS(**config["transformer"])),
            ("sra_analyser", SRA()),
        ]
        pipeline = Pipeline(steps=steps)
        analysis = pipeline.fit_transform(df)
        ResultPrinter()(analysis)