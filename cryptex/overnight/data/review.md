# CRYPTEX paper-trading results — automated review

**SIMULATED TRADING ONLY: no actual orders, earnings or exchange balances.**

Generated: 2026-11-22T00:00:40.995077+00:00
Data status: HEALTHY: paper trading on completed Kraken candles
Paper equity: USD 84.81; initial USD 100.00; change USD -15.19.
Closed trades: 136; wins 7; losses/breakevens 129.

## Specialist research teams

10 parent traders; 64 deterministic, correlated indicator-voters per parent = 640 transparent subagent evaluations per valid candle.
The specialist parameter sweeps do **not** mean 640 independent AI models or additional market feeds.
Votes may disagree; all votes are archived at `data/subagent_decisions.csv`. Parent fill results still come from `data/trades.csv`.

| Parent | Decision | Symbol | Favourable votes | Cautious votes | Vetoes |
| --- | --- | --- | ---: | ---: | ---: |
| GAMBLER | HOLD | BTC | 10 | 11 | 0 |
| HOUSE | HOLD | BTC | 10 | 11 | 0 |
| SPY | HOLD | SOL | 16 | 6 | 0 |
| MEME HUNTER | HOLD | DOGE | 19 | 5 | 0 |
| BREAKOUT | HOLD | BTC | 10 | 11 | 0 |
| CONTRARIAN | HOLD | BTC | 10 | 11 | 0 |
| ROTATOR | HOLD | BTC | 10 | 11 | 0 |
| VORTEX | HOLD | BTC | 10 | 11 | 0 |
| FRACTAL | HOLD | BTC | 10 | 11 | 0 |
| SHOCKWAVE | HOLD | DOGE | 19 | 5 | 0 |

## Bot performance

| Bot | Closed | Wins | Losses | Win rate | Realized net USD | Next allocation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| GAMBLER | 5 | 0 | 5 | 0.0% | -0.5215 | 1.00x |
| HOUSE | 10 | 0 | 10 | 0.0% | -0.5537 | 1.00x |
| SPY | 7 | 1 | 6 | 14.3% | -0.5041 | 1.00x |
| MEME HUNTER | 6 | 2 | 4 | 33.3% | -0.3414 | 1.00x |
| BREAKOUT | 7 | 0 | 7 | 0.0% | -0.8432 | 1.00x |
| CONTRARIAN | 11 | 0 | 11 | 0.0% | -0.8912 | 1.00x |
| ROTATOR | 9 | 0 | 9 | 0.0% | -3.3339 | 1.00x |
| VORTEX | 48 | 1 | 47 | 2.1% | -5.0301 | 0.50x |
| FRACTAL | 25 | 1 | 24 | 4.0% | -3.5208 | 0.50x |
| SHOCKWAVE | 8 | 2 | 6 | 25.0% | -0.0490 | 1.00x |

## Where paper trades lost money

- **PILOT V1 trend turned down; next-candle simulated exit**: 45 exits; net USD -5.2664
- **PILOT V1 fixed holding window reached; next-candle simulated exit**: 22 exits; net USD -3.7552
- **Exploratory 15-minute observation complete (next-bar fill)**: 21 exits; net USD -0.2123
- **RSI normalized**: 9 exits; net USD -0.8805
- **Breakout failed**: 6 exits; net USD -0.8265
- **Range normalized**: 6 exits; net USD -0.5201
- **Time-based exit**: 5 exits; net USD -0.5343
- **PILOT V1 observed 6% stop; next-candle simulated exit**: 5 exits; net USD -2.9019
- **Trend failure**: 3 exits; net USD -0.4266
- **Volume faded**: 3 exits; net USD -0.4650
- **Timescales disagree**: 2 exits; net USD -0.0146
- **Shockwave ended**: 1 exits; net USD -0.0095
- **Meme reversal**: 1 exits; net USD -0.1847

## Where paper trades made money

- **Exploratory 15-minute observation complete (next-bar fill)**: 5 exits; net USD +0.0132
- **PILOT V1 fixed holding window reached; next-candle simulated exit**: 1 exits; net USD +0.0087
- **PILOT V1 trend turned down; next-candle simulated exit**: 1 exits; net USD +0.3868

## How to interpret the results

A win rate alone is not a trading edge. We must examine risk-adjusted out-of-sample returns, sample size, market regime, costs, feed freshness and rejected decisions.
Position size decreases after at least 20 closed paper trades if expectancy is weak; this is bounded adaptive sizing, not a trained self-improving prediction model.
Scheduled sampling can miss interim price moves and delays stop triggers. Backtesting and paper trading are not proof of real profitability.
Latest unavailable Kraken pairs: none reported
