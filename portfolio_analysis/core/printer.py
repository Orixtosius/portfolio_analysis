import matplotlib.pyplot as plt


class ResultPrinter:
    def __call__(self, analysis_result: dict):
        self._plot_efficient_frontier(analysis_result)
        self._print_summary(analysis_result)
    
    def _plot_efficient_frontier(self, analysis_result):
        plt.figure(figsize=(10, 6))
        plt.scatter(
            analysis_result["efficient_frontier"], 
            analysis_result["range"], 
            c=(analysis_result["range"]-0)/analysis_result["efficient_frontier"], marker='x')
        plt.plot(analysis_result["volatility"], analysis_result["return"], 'r*', markersize=15)
        plt.title('Efficient Frontier')
        plt.xlabel('Volatility (Risk)')
        plt.ylabel('Expected Return')
        plt.show()

    def _print_summary(self, analysis_result):
        print(f"Portfolio Distribution: {analysis_result["portfolio_distribution"]}")
        print(f"Expected Portfolio Return: {analysis_result["return"]}")
        print(f"Portfolio Volatility (Risk): {analysis_result["volatility"]}")
        print(f"Sharpe Ratio: {analysis_result["sharpe_ratio"]}")