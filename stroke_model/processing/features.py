import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class Mapper(BaseEstimator, TransformerMixin):
    def __init__(self, variables: str, variables_mapping: dict):
        if not isinstance(variables, str):
            raise ValueError("variables must be a string")

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()
        X[self.variables] = X[self.variables].map(self.mapping).astype(int)
        return X



class OutlierHandler(BaseEstimator, TransformerMixin):
    def __init__(self, threshold=3):
        self.threshold = threshold

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        z_scores = np.abs((X - X.mean()) / X.std())
        X_cleaned = X[(z_scores < self.threshold).all(axis=1)]
        return X_cleaned
