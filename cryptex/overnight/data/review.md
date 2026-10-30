# CRYPTEX paper-trading results — automated review

**SIMULATED TRADING ONLY: no actual orders, earnings or exchange balances.**

Generated: 2026-10-30T23:25:35.897508+00:00
Data status: HEALTHY: paper trading on completed Kraken candles
Paper equity: USD 99.66; initial USD 100.00; change USD -0.34.
Closed trades: 24; wins 5; losses/breakevens 19.

## Specialist research teams

10 parent traders; 64 deterministic, correlated indicator-voters per parent = 640 transparent subagent evaluations per valid candle.
The specialist parameter sweeps do **not** mean 640 independent AI models or additional market feeds.
Votes may disagree; all votes are archived at `data/subagent_decisions.csv`. Parent fill results still come from `data/trades.csv`.

| Parent | Decision | Symbol | Favourable votes | Cautious votes | Vetoes |
| --- | --- | --- | ---: | ---: | ---: |
| GAMBLER | HOLD | SOL | 19 | 3 | 0 |
| HOUSE | SELL | SOL | 5 | 17 | 0 |
| SPY | SELL | PEPE | 20 | 16 | 0 |
| MEME HUNTER | HOLD | PEPE | 20 | 16 | 0 |
| BREAKOUT | SELL | SOL | 19 | 3 | 0 |
| CONTRARIAN | BUY | XRP | 7 | 14 | 0 |
| ROTATOR | HOLD | ADA | 16 | 9 | 1 |
| VORTEX | HOLD | ETH | 16 | 6 | 0 |
| FRACTAL | SELL | PEPE | 20 | 16 | 0 |
| SHOCKWAVE | SELL | PEPE | 20 | 16 | 0 |

## Bot performance

| Bot | Closed | Wins | Losses | Win rate | Realized net USD | Next allocation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| GAMBLER | 2 | 0 | 2 | 0.0% | -0.0162 | 1.00x |
| HOUSE | 3 | 0 | 3 | 0.0% | -0.0234 | 1.00x |
| SPY | 3 | 1 | 2 | 33.3% | -0.0208 | 1.00x |
| MEME HUNTER | 3 | 2 | 1 | 66.7% | -0.0012 | 1.00x |
| BREAKOUT | 2 | 0 | 2 | 0.0% | -0.1166 | 1.00x |
| CONTRARIAN | 4 | 0 | 4 | 0.0% | -0.0351 | 1.00x |
| ROTATOR | 0 | 0 | 0 | — | +0.0000 | 1.00x |
| VORTEX | 0 | 0 | 0 | — | +0.0000 | 1.00x |
| FRACTAL | 4 | 0 | 4 | 0.0% | -0.0429 | 1.00x |
| SHOCKWAVE | 3 | 2 | 1 | 66.7% | -0.0012 | 1.00x |

## Where paper trades lost money

- **Exploratory 15-minute observation complete (next-bar fill)**: 11 exits; net USD -0.1040
- **RSI normalized**: 3 exits; net USD -0.0281
- **Breakout failed**: 2 exits; net USD -0.1166
- **Timescales disagree**: 2 exits; net USD -0.0146
- **Trend failure**: 1 exits; net USD -0.0072

## Where paper trades made money

- **Exploratory 15-minute observation complete (next-bar fill)**: 5 exits; net USD +0.0132

## How to interpret the results

A win rate alone is not a trading edge. We must examine risk-adjusted out-of-sample returns, sample size, market regime, costs, feed freshness and rejected decisions.
Position size decreases after at least 20 closed paper trades if expectancy is weak; this is bounded adaptive sizing, not a trained self-improving prediction model.
Scheduled sampling can miss interim price moves and delays stop triggers. Backtesting and paper trading are not proof of real profitability.
Latest unavailable Kraken pairs: none reported
