from typing import Literal
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np
import scipy.optimize as sco


class SharpeRatioAnalyser(BaseEstimator, TransformerMixin):

    def __init__(self, method: str = "SLSQP", risk_free_rate: float = 0) -> None:
        self.method = method
        self.risk_free_rate = risk_free_rate

    def fit(self, X: pd.DataFrame, y=None):
        returns = np.log(X / X.shift(1)).dropna()
        self.mean_returns = returns.mean()
        self.cov_matrix = returns.cov()
        self.columns = [c.replace("Close_", "") for c in X.columns]
        return self
    
    def _get_portfolio_performance(self, weights):
        returns = np.sum(weights * self.mean_returns)
        volatility = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix, weights)))
        return returns, volatility
    
    def _set_common_properties(self):
        num_assets = len(self.mean_returns)
        cons = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        bounds = tuple((0, 1) for _ in range(num_assets))
        return num_assets, cons, bounds
    
    def _optimize_sharpe_ratio(self):
        num_assets, cons, bounds = self._set_common_properties()
        result = sco.minimize(
            fun=self._calculate_neg_sharpe_ration, 
            x0=num_assets * [1. / num_assets,],
            method='SLSQP', 
            bounds=bounds, 
            constraints=(cons))
        return result
    
    def _calculate_neg_sharpe_ration(self, weights):
        returns, volatility = self._get_portfolio_performance(weights)
        return - (returns - self.risk_free_rate) / volatility
    
    def _calculate_portfolio_variance(self, weights):
        return self._get_portfolio_performance(weights)[1]
    
    def _calculate_efficient_frontier(self, returns_range):
        num_assets, cons, bounds = self._set_common_properties()
        efficients = []
        for ret in returns_range:
            constraints = (cons, {'type': 'eq', 'fun': lambda x: self._get_portfolio_performance(x)[0] - ret})
            result = sco.minimize(
                fun=self._calculate_portfolio_variance, 
                x0=num_assets * [1. / num_assets,], 
                method='SLSQP', 
                bounds=bounds, 
                constraints=constraints)
            efficients.append(result['fun'])
        return efficients

    def transform(self, X, y=None) -> dict:
        optimal_portfolio = self._optimize_sharpe_ratio()
        optimal_weights = optimal_portfolio['x']
        portfolio_return, portfolio_volatility = self._get_portfolio_performance(optimal_weights)
        sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_volatility
        returns_range = np.linspace(self.mean_returns.min(), self.mean_returns.max(), 100)
        efficient_frontier = self._calculate_efficient_frontier(returns_range)
        result = {
            "portfolio_distribution": {c: w for c, w in zip(self.columns, optimal_weights)},
            "return": portfolio_return,
            "volatility": portfolio_volatility,
            "sharpe_ratio": sharpe_ratio,
            "efficient_frontier": efficient_frontier,
            "range": returns_range
        }
        return result
    
    def set_output(self, *, transform: None | Literal['default'] | Literal['pandas'] = "pandas") -> BaseEstimator:
        return super().set_output(transform=transform)