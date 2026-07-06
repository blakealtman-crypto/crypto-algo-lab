"""
Pull historical OHLCV candles from an exchange using ccxt (public market data,
no API key required) and save to a local CSV for backtesting.

Usage:
    python fetch_data.py --symbol BTC/USDT --timeframe 1h --limit 1000
"""
import argparse
import ccxt
import pandas as pd


def fetch_ohlcv(exchange_id="binance", symbol="BTC/USDT", timeframe="1h", limit=1000):
    exchange_class = getattr(ccxt, exchange_id)
    exchange = exchange_class({"enableRateLimit": True})
    raw = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(raw, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)
    return df


def main():
    parser = argparse.ArgumentParser(description="Fetch historical crypto OHLCV data")
    parser.add_argument("--exchange", default="binance")
    parser.add_argument("--symbol", default="BTC/USDT")
    parser.add_argument("--timeframe", default="1h")
    parser.add_argument("--limit", type=int, default=1000)
    parser.add_argument("--out", default=None, help="Output CSV path")
    args = parser.parse_args()

    df = fetch_ohlcv(args.exchange, args.symbol, args.timeframe, args.limit)
    out_path = args.out or f"data/{args.symbol.replace('/', '')}_{args.timeframe}.csv"
    df.to_csv(out_path)
    print(f"Saved {len(df)} candles to {out_path}")


if __name__ == "__main__":
    main()
