"""Example strategy: simple moving average crossover.

Long when fast SMA > slow SMA, flat otherwise. This is intentionally simple —
it's a template to replace with your own logic, not a strategy to trade live.
"""
import pandas as pd
from strategies.base import Strategy


class SmaCrossover(Strategy):
    def __init__(self, fast_window: int = 20, slow_window: int = 50):
        self.fast_window = fast_window
        self.slow_window = slow_window

    def generate_signals(self, df: pd.DataFrame) -> pd.Series:
        fast = df["close"].rolling(self.fast_window).mean()
        slow = df["close"].rolling(self.slow_window).mean()
        signal = (fast > slow).astype(int)
        return signal.fillna(0)
