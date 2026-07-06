# crypto-algo-lab

A backtesting framework and strategy playground for systematic crypto trading — built to actually run, not just look good in a repo list.

**Status: early-stage / learning-in-public.** This is a research and experimentation tool, not a live trading system, and nothing here is financial advice.

## What's in here

- `fetch_data.py` — pulls historical OHLCV candles from any exchange via [ccxt](https://github.com/ccxt/ccxt) (public data, no API key needed)
- `strategies/` — strategy interface (`base.py`) + an example moving-average crossover strategy (`sma_crossover.py`)
- `backtester.py` — vectorized backtest engine: no-lookahead signal shifting, fee modeling, equity curve, Sharpe, max drawdown
- `run_backtest.py` — CLI to run a strategy against fetched data and print results
- `tests/` — sanity tests on the backtest math itself (lookahead bias, fee handling, compounding)

## Quickstart

```bash
pip install -r requirements.txt

# Pull ~1000 hourly BTC/USDT candles from Binance (public data)
python fetch_data.py --symbol BTC/USDT --timeframe 1h --limit 1000

# Backtest the example SMA crossover strategy against it
python run_backtest.py --data data/BTCUSDT_1h.csv --fast 20 --slow 50
```

## Run tests

```bash
pytest tests/
```

## Adding your own strategy

1. Subclass `Strategy` in `strategies/`, implement `generate_signals(df) -> pd.Series` (1 = long, 0 = flat, -1 = short)
2. Point `run_backtest.py` at your new strategy class
3. Iterate on parameters, timeframes, and symbols

## Design notes / honesty check

- Signals are shifted by one bar to avoid lookahead bias — you're trading on the *next* bar after a signal fires, not the same one
- Fees are modeled as a flat bps cost per position change; slippage is **not** modeled yet
- The included SMA crossover strategy is a template, not something to trade with real capital
- No live execution/order placement here — this is backtest-only, on purpose, until there's a strategy worth the risk

## Roadmap ideas

- [ ] Walk-forward / out-of-sample testing to avoid overfitting to backtest data
- [ ] Slippage modeling
- [ ] Multi-asset portfolio backtesting
- [ ] Parameter optimization with proper train/test splits (not just curve-fitting)
- [ ] Paper-trading mode before any real execution
