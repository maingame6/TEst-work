# CRYPTEX: independent free historical market-data research

**Prepared 9 November 2026. PAPER ONLY. No trading, no strategy promotion, no new infrastructure.**

This branch is an additive read-only reference-data experiment. It does not alter the $210 / 21-agent simulated accounts, Kraken forward signals, five-minute scheduler, GitHub writer authority, keys, CSGORisky, or the other research branches.

## Public GitHub sources researched

| Project | What it offers | CRYPTEX decision |
| --- | --- | --- |
| [binance/binance-public-data](https://github.com/binance/binance-public-data) | Official downloadable, checksummed monthly and daily OHLCV/trades. Spot timestamps switch to **microseconds** from 1 January 2025. | **Added** a checksum-verified, historical spot monthly 5m/1h importer and offline replay. |
| [ccxt/ccxt](https://github.com/ccxt/ccxt) | Public OHLCV, pair metadata and order-book APIs across many exchanges. | Already used in the separate five-exchange scanner; do not mistake a market catalogue for acquired trade history. |
| [coinmetrics/data](https://github.com/coinmetrics/data) | Daily-updated free community on-chain CSV data. | Research candidate only. Its **CC BY-NC 4.0** licence and daily frequency need review before any use in commercial or 5m signals. |
| [bmoscon/cryptofeed](https://github.com/bmoscon/cryptofeed) | Normalized live order-book and trade events with venue/receipt timestamps. | Research candidate only. Current code has AGPL obligations and continuous-feed operational cost; not deployed. |
| [freqtrade/freqtrade](https://github.com/freqtrade/freqtrade) | Lookahead and recursive-indicator checks for backtesting. | Adopt causality tests, not its GPL code. Completed bars only; never move signals back in time. |

## Added in this update

- **historical_archive.py** downloads one manually selected, fully completed public Binance spot archive and official SHA-256 checksum. It verifies exact archive naming, member paths, timestamp resolution, OHLC validity, chronology and gaps. It preserves quote currency, e.g. BTCUSDT is not Kraken BTC/USD.
- **historical_replay.py** runs **three fixed reference rules** on the final 30% of that historical month. Signals use earlier complete candles, entry and exit use subsequent complete-candle proxies, and missing intervals censor outcomes. It compares hypothetical after-cost returns and stressed slippage against cash and a same-symbol buy-and-hold reference when continuous.
- Research-only cost counterfactual: **0.8% assumed fee per side** and **0.25% / 0.50% assumed slippage per side**. These are NOT actual Binance account fees or executable fills.
- Regression tests are standalone Python stdlib, with deliberate checksum tampering, time-unit changes, duplicates, invalid OHLC, gaps and non-paper input.
- The new Actions workflow is **manual-only**, read-only, no secrets, no cron, no trading credentials, no commits to data branches, and uploads reference data and diagnostics as a 14-day artifact.

### Run only after reviewing and merging the PR

In GitHub Actions, select **CRYPTEX - independent historical reference data (PAPER ONLY)**, then Run workflow. Example inputs: symbol **BTCUSDT**, interval **5m**, month **2026-10**. The public archive must already exist, and the month must have fully ended. If unavailable or corrupt, the workflow FAILS rather than inventing returns.

Local test and run commands:

    python3 -m unittest discover -s cryptex/ops/tests -p 'test_historical_*.py' -v
    python3 cryptex/ops/historical_archive.py --symbol BTCUSDT --interval 5m --month 2026-10 --out /tmp/cryptex-history
    python3 cryptex/ops/historical_replay.py --reference /tmp/cryptex-history

For reproducible offline import, give historical_archive.py BOTH --archive and --checksum paths from the official archive.

The output artifact contains **historical_reference.csv**, **historical_reference.json**, and **historical_replay.json**. Neither historical data nor replay outcomes are written into the prospective CRYPTEX paper ledger.

## Measured gaps and safe next priorities

At **2026-11-09 12:27 UTC**, the genuine main five-minute record had **2,311/2,462** expected candles, **151 missing**, **93.867% coverage**, and **$200.746259** virtual portfolio equity from $210 start. The separate 84-variant hourly lab had **312 observed and 1,560 missing symbol-hours**, and **zero completed hypothetical outcomes**. These are DISTINCT populations.

Historical archive rows **never count** as recovered prospective observations, previously censored hourly samples, forward paper fills or restored coverage. An old backtest cannot repair an outage or prove executable performance.

Next engineering priorities: raise genuine five-minute and hourly collection reliability; audit single-writer/fallback behavior before its planned cutoff; collect bid/ask depths and verified applicable costs; test many independently frozen periods and regimes without cherry-picking; compare outcomes to matched cash/buy-hold with uncertainty and multiple-testing penalties. A fresh held-out forward sample still needs at least 99% recorded coverage and 30 clean completions per original strategy, with no automatic promotion. Any promising backtest remains **NOT PROVEN** until these conditions are met.
