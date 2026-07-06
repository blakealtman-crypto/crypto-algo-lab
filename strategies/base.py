"""Base class every strategy implements. Keep strategies stateless and vectorized
where possible so the backtester can run them fast over full history."""
from abc import ABC, abstractmethod
import pandas as pd


class Strategy(ABC):
    """A strategy turns OHLCV data into a position signal per bar.

    Signal convention: 1 = long, -1 = short, 0 = flat.
    Override `generate_signals` to implement your logic.
    """

    @abstractmethod
    def generate_signals(self, df: pd.DataFrame) -> pd.Series:
        """Return a Series of signals (1/0/-1), same index as df."""
        raise NotImplementedError
