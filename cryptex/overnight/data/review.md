# CRYPTEX paper-trading results — automated review

**SIMULATED TRADING ONLY: no actual orders, earnings or exchange balances.**

Generated: 2026-10-30T23:30:38.630841+00:00
Data status: HEALTHY: paper trading on completed Kraken candles
Paper equity: USD 99.66; initial USD 100.00; change USD -0.34.
Closed trades: 27; wins 5; losses/breakevens 22.

## Specialist research teams

10 parent traders; 64 deterministic, correlated indicator-voters per parent = 640 transparent subagent evaluations per valid candle.
The specialist parameter sweeps do **not** mean 640 independent AI models or additional market feeds.
Votes may disagree; all votes are archived at `data/subagent_decisions.csv`. Parent fill results still come from `data/trades.csv`.

| Parent | Decision | Symbol | Favourable votes | Cautious votes | Vetoes |
| --- | --- | --- | ---: | ---: | ---: |
| GAMBLER | HOLD | SOL | 26 | 2 | 0 |
| HOUSE | SELL | SOL | 8 | 20 | 0 |
| SPY | SELL | PEPE | 19 | 14 | 0 |
| MEME HUNTER | HOLD | PEPE | 19 | 14 | 0 |
| BREAKOUT | BUY | SOL | 26 | 2 | 0 |
| CONTRARIAN | SELL | XRP | 8 | 19 | 0 |
| ROTATOR | HOLD | ADA | 23 | 6 | 1 |
| VORTEX | HOLD | ETH | 20 | 6 | 1 |
| FRACTAL | BUY | SOL | 26 | 2 | 0 |
| SHOCKWAVE | SELL | PEPE | 19 | 14 | 0 |

## Bot performance

| Bot | Closed | Wins | Losses | Win rate | Realized net USD | Next allocation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| GAMBLER | 2 | 0 | 2 | 0.0% | -0.0162 | 1.00x |
| HOUSE | 4 | 0 | 4 | 0.0% | -0.0310 | 1.00x |
| SPY | 4 | 1 | 3 | 25.0% | -0.0303 | 1.00x |
| MEME HUNTER | 3 | 2 | 1 | 66.7% | -0.0012 | 1.00x |
| BREAKOUT | 2 | 0 | 2 | 0.0% | -0.1166 | 1.00x |
| CONTRARIAN | 4 | 0 | 4 | 0.0% | -0.0351 | 1.00x |
| ROTATOR | 0 | 0 | 0 | — | +0.0000 | 1.00x |
| VORTEX | 0 | 0 | 0 | — | +0.0000 | 1.00x |
| FRACTAL | 4 | 0 | 4 | 0.0% | -0.0429 | 1.00x |
| SHOCKWAVE | 4 | 2 | 2 | 50.0% | -0.0107 | 1.00x |

## Where paper trades lost money

- **Exploratory 15-minute observation complete (next-bar fill)**: 11 exits; net USD -0.1040
- **RSI normalized**: 3 exits; net USD -0.0281
- **Breakout failed**: 2 exits; net USD -0.1166
- **Timescales disagree**: 2 exits; net USD -0.0146
- **Trend failure**: 1 exits; net USD -0.0072
- **Range normalized**: 1 exits; net USD -0.0075
- **Volume faded**: 1 exits; net USD -0.0095
- **Shockwave ended**: 1 exits; net USD -0.0095

## Where paper trades made money

- **Exploratory 15-minute observation complete (next-bar fill)**: 5 exits; net USD +0.0132

## How to interpret the results

A win rate alone is not a trading edge. We must examine risk-adjusted out-of-sample returns, sample size, market regime, costs, feed freshness and rejected decisions.
Position size decreases after at least 20 closed paper trades if expectancy is weak; this is bounded adaptive sizing, not a trained self-improving prediction model.
Scheduled sampling can miss interim price moves and delays stop triggers. Backtesting and paper trading are not proof of real profitability.
Latest unavailable Kraken pairs: none reported
