# CRYPTEX: independent hourly factor lab

The existing 21-wallet $210 PAPER_ONLY competition is unchanged. This study has
no order API, private exchange key access, portfolio balancing or capability to
promote candidates into the production five-minute engine.

- 28 predeclared rule families x 3 fixed lookback windows (8/16/32 completed
  hourly bars) = 84 strategy candidates, evaluated independently across
  12 Kraken spot pairs. 84 are not 84 proven profitable strategies.
- 47 causal indicator fields: EMA/SMA, RSI, ATR, MACD, VWAP, MFI, CMF,
  OBV, Donchian, Bollinger, Keltner, stochastic, Williams %R, choppiness,
  Aroon, volatility. ADX proxy is not canonical Wilder ADX.
- Signals use fully completed hourly Kraken OHLCV. A signal cannot enter until
  the next genuinely observed hourly close; estimated closes are not fills.
- Hypothetical holding period is 24 consecutive observed hours; missing hours
  censor the outcome. No interpolation, no backdating.
- Assumed taker fee 0.8% per side; hypothetical slippage 0.25% per side,
  stress slippage 0.5% per side. No claim of actual exchange-account fees.
- Frozen holdout starts November 10, 2026 UTC. Minimum *review* threshold:
  30 observed days and 60 closes per candidate, not statistical proof.
- All strategies have eligible_to_promote = false. Independent analysis must
  include multiple-testing corrections, blocked confidence intervals, regime
  checks, and cost-matched buy-and-hold/cash comparisons.
- No look-ahead, retroactive signal injection or automatic optimisation.
- No unproved profit or real-money execution claims.

## Optional standalone execution
    python -m unittest discover -s cryptex/ops/tests -p test_strategy_lab.py -v
    python cryptex/ops/strategy_lab.py --data ./cryptex-factor-lab-data

Files output ONLY to nominated separate research folder:
strategy_lab_state.json, strategy_lab_report.json, strategy_lab_report.md.

## Remaining high-impact research gaps
1. Reliable always-on data collection independent of best-effort GitHub cron.
2. Actual executable bid/ask, depth and minimum-size trade simulation.
3. More than 30 days of genuinely forward-collected, held-out results.
4. Statistical corrections for correlated signals and many candidate tests.
5. Realistic lower-cost execution, where legitimately available, and longer holds.
6. Persistent immutable market data and complete reproducible research artifacts.
7. Independent recovery, monitoring, and writer-fence verification.
