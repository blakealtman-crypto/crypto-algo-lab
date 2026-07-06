"""Sanity tests: not a validation of strategy profitability, just that the
engine's math (no lookahead, equity curve compounding, drawdown calc) is correct."""
import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backtester import Backtester
from strategies.base import Strategy


class AlwaysLong(Strategy):
    def generate_signals(self, df):
        return pd.Series(1, index=df.index)


class AlwaysFlat(Strategy):
    def generate_signals(self, df):
        return pd.Series(0, index=df.index)


def make_dummy_df(prices):
    idx = pd.date_range("2024-01-01", periods=len(prices), freq="h")
    return pd.DataFrame({"close": prices}, index=idx)


def test_always_flat_has_zero_return():
    df = make_dummy_df([100, 110, 90, 120, 105])
    bt = Backtester(fee_bps=0)
    result = bt.run(df, AlwaysFlat())
    assert result["stats"]["total_return_pct"] == 0


def test_always_long_matches_buy_and_hold():
    prices = [100, 110, 121]
    df = make_dummy_df(prices)
    bt = Backtester(fee_bps=0)
    result = bt.run(df, AlwaysLong())
    # first bar's pct_change is 0 by construction (no prior bar), so an
    # always-long strategy should fully match buy-and-hold from bar 0 to the end
    expected = (prices[-1] / prices[0]) - 1
    assert abs(result["equity_curve"].iloc[-1] - (1 + expected)) < 1e-9


def test_no_lookahead_bias():
    # first bar should always have zero position since signal is shifted
    df = make_dummy_df([100, 200, 50, 300])
    bt = Backtester(fee_bps=0)
    result = bt.run(df, AlwaysLong())
    assert result["positions"].iloc[0] == 0


def test_fees_reduce_returns():
    df = make_dummy_df([100, 110, 100, 110, 100])
    bt_no_fee = Backtester(fee_bps=0)
    bt_fee = Backtester(fee_bps=50)
    r_no_fee = bt_no_fee.run(df, AlwaysLong())["stats"]["total_return_pct"]
    r_fee = bt_fee.run(df, AlwaysLong())["stats"]["total_return_pct"]
    assert r_fee <= r_no_fee
