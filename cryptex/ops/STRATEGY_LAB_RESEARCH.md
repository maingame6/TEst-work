# CRYPTEX independent hourly strategy lab

**PAPER-ONLY RESEARCH.** This is isolated from the original $210 experiment,
21 agents and the five-minute GitHub writer. No external account access,
private exchange credentials, live orders or automatic strategy promotion.

## Frozen research registry

- 28 distinct signal families, fixed lookback windows 8/16/32 observed hours:
  **84 registered variants** over twelve Kraken USD pairs.
- **47 computed causal indicators/features**: SMA, EMA, RSI, ATR, Bollinger,
  MACD, ROC, rolling VWAP, OBV, MFI, CCI, CMF, stochastic, Williams %R,
  Aroon, ADX **proxy**, Ulcer, TRIX, range, volume, volatility and others.
- One preset 24-hour observed hold. Entries are *hypothetical* at a later
  completed hourly close. The current forming Kraken candle is excluded.
  Historical prices only warm up indicators, and never generate earlier
  simulated trades. Missing hours censor pending/active hypotheses.
- Estimated taker fee 0.8% per side, modelled slippage 0.25% per side,
  slippage stress 0.5% per side. A completed candle is not an executable quote.
- No automatic promotion. Frozen held-out period starts 10 Nov 2026 00:00 UTC;
  minimum 30 days and 60 genuine forward outcomes per candidate are
  *review prerequisites*, not a proof of profit.

The hourly free GitHub Actions workflow operates independently and commits
only to the `cryptex-factor-research` branch, never to the paper trading
journal. Native cron is best effort. No hypothetical fills are invented for
skipped intervals. All results, including failures, are published.

## Evidence output

- `cryptex/strategy-lab/data/strategy_lab_state.json`: recorded outcomes,
  censored samples and all per-candidate pending/active state.
- `cryptex/strategy-lab/data/strategy_lab_report.json`: full candidate scores.
- `cryptex/strategy-lab/data/strategy_lab_report.md`: readable scorecard.

**The purpose is to falsify weak trading ideas**, not pretend that correlated
indicator combinations establish a positive expectancy.

## Remaining gaps ranked for profit and resilience

1. Long-term uninterrupted five-minute and hourly collection, single-writer
   failover evidence (current bounded fallback ends 10 November).
2. Time-consistent orderbook depth, bid/ask, true venue fees and market
   impact at the proposed order size.
3. Pre-registered matched benchmarks and multiple-testing correction
   (cluster bootstrap, deflated Sharpe), with untouched held-out markets/dates.
4. More than 30 days of genuine observed hours, stable symbol membership,
   delistings and data provenance; do not infer live opportunities from
   backfilled candles.
5. Further 4-hour/daily signals, minimum notional/precision checks and
   exposure/correlation constraints, after enough data.
6. Independent outage monitoring, durable backup, reproducible restoration,
   no silent account or writer switching.
7. Prove value of correlated reviewers; 640 reviewers are not independent
   models or sources of evidence.

Research:
- https://www.sciencedirect.com/science/article/pii/S1544612325011377
- https://link.springer.com/article/10.1007/s11408-025-00474-9
- https://www.frontiersin.org/journals/blockchain/articles/10.3389/fbloc.2026.1811716/full
- https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7350238

No financial returns are guaranteed. Historical backtests and prospective
paper results can both fail to predict future live trading performance.
