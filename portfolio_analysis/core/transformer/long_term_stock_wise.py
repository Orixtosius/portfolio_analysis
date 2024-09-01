from typing import Literal
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd


class LongTermStockWiseTransformer(BaseEstimator, TransformerMixin):

    def __init__(self, stock_column: str, price_column: str) -> None:
        self.stock_column = stock_column
        self.price_column = price_column

    def fit(self, X, y=None):
        X_simple = X[[self.stock_column, self.price_column]]
        X_expanded = pd.DataFrame()
        for stock in X_simple[self.stock_column].unique():
            X_expanded[f'{self.price_column}_{stock}'] = \
                X_simple[X_simple[self.stock_column] == stock][self.price_column].reset_index(drop=True)

        self.X_expanded = X_expanded
        return self

    def transform(self, X, y=None):
        return self.X_expanded
    
    def set_output(self, *, transform: None | Literal['default'] | Literal['pandas'] = "pandas") -> BaseEstimator:
        return super().set_output(transform=transform)