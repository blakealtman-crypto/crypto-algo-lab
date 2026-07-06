"""
CLI entry point: load data, run a strategy through the backtester, print stats.

Usage:
    python fetch_data.py --symbol BTC/USDT --timeframe 1h --limit 1000
    python run_backtest.py --data data/BTCUSDT_1h.csv --fast 20 --slow 50
"""
import argparse
import pandas as pd
from strategies.sma_crossover import SmaCrossover
from backtester import Backtester


def main():
    parser = argparse.ArgumentParser(description="Run a backtest on historical OHLCV data")
    parser.add_argument("--data", required=True, help="Path to CSV from fetch_data.py")
    parser.add_argument("--fast", type=int, default=20, help="Fast SMA window")
    parser.add_argument("--slow", type=int, default=50, help="Slow SMA window")
    parser.add_argument("--fee-bps", type=float, default=5.0, help="Round-trip fee in bps")
    args = parser.parse_args()

    df = pd.read_csv(args.data, index_col=0, parse_dates=True)
    strategy = SmaCrossover(fast_window=args.fast, slow_window=args.slow)
    bt = Backtester(fee_bps=args.fee_bps)
    result = bt.run(df, strategy)

    print("\n--- Backtest Results ---")
    for k, v in result["stats"].items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
