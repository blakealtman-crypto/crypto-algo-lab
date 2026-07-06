"""Minimal vectorized backtester: applies a strategy's signals to price data
and computes returns, equity curve, and basic performance stats.

This is deliberately simple (no slippage/fees modeling by default) — a starting
point to build realism into as you go, not a production trading engine.
"""
import pandas as pd
import numpy as np
from strategies.base import Strategy


class Backtester:
    def __init__(self, fee_bps: float = 0.0):
        """fee_bps: round-trip fee in basis points, applied on position changes."""
        self.fee_bps = fee_bps

    def run(self, df: pd.DataFrame, strategy: Strategy) -> dict:
        signals = strategy.generate_signals(df)
        returns = df["close"].pct_change().fillna(0)

        # shift signal by 1 bar to avoid lookahead bias (you trade on next bar's open)
        positions = signals.shift(1).fillna(0)
        strategy_returns = positions * returns

        # apply fee on position changes
        position_changes = positions.diff().abs().fillna(0)
        fees = position_changes * (self.fee_bps / 10000)
        strategy_returns = strategy_returns - fees

        equity_curve = (1 + strategy_returns).cumprod()

        stats = self._compute_stats(strategy_returns, equity_curve)
        return {
            "equity_curve": equity_curve,
            "returns": strategy_returns,
            "positions": positions,
            "stats": stats,
        }

    @staticmethod
    def _compute_stats(returns: pd.Series, equity_curve: pd.Series) -> dict:
        total_return = equity_curve.iloc[-1] - 1 if len(equity_curve) else 0
        n = len(returns)
        ann_factor = 365 * 24  # assumes hourly bars; adjust for your timeframe
        vol = returns.std() * np.sqrt(ann_factor) if n > 1 else 0
        sharpe = (returns.mean() * ann_factor) / vol if vol > 0 else 0
        running_max = equity_curve.cummax()
        drawdown = (equity_curve / running_max) - 1
        max_drawdown = drawdown.min() if len(drawdown) else 0

        return {
            "total_return_pct": round(total_return * 100, 2),
            "annualized_sharpe": round(sharpe, 2),
            "max_drawdown_pct": round(max_drawdown * 100, 2),
            "num_bars": n,
        }
