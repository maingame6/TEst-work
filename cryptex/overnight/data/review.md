# CRYPTEX paper-trading results — automated review

**SIMULATED TRADING ONLY: no actual orders, earnings or exchange balances.**

Generated: 2026-11-06T07:26:15.487601+00:00
Data status: HEALTHY: paper trading on completed Kraken candles
Paper equity: USD 94.38; initial USD 100.00; change USD -5.62.
Closed trades: 70; wins 7; losses/breakevens 63.

## Specialist research teams

10 parent traders; 64 deterministic, correlated indicator-voters per parent = 640 transparent subagent evaluations per valid candle.
The specialist parameter sweeps do **not** mean 640 independent AI models or additional market feeds.
Votes may disagree; all votes are archived at `data/subagent_decisions.csv`. Parent fill results still come from `data/trades.csv`.

| Parent | Decision | Symbol | Favourable votes | Cautious votes | Vetoes |
| --- | --- | --- | ---: | ---: | ---: |
| GAMBLER | HOLD | BTC | 5 | 20 | 0 |
| HOUSE | HOLD | BTC | 19 | 6 | 0 |
| SPY | HOLD | SOL | 15 | 9 | 0 |
| MEME HUNTER | HOLD | DOGE | 10 | 20 | 0 |
| BREAKOUT | HOLD | BTC | 5 | 20 | 0 |
| CONTRARIAN | HOLD | BTC | 19 | 6 | 0 |
| ROTATOR | HOLD | BTC | 5 | 20 | 0 |
| VORTEX | HOLD | ETH | 7 | 24 | 0 |
| FRACTAL | HOLD | SOL | 15 | 9 | 0 |
| SHOCKWAVE | HOLD | DOGE | 10 | 20 | 0 |

## Bot performance

| Bot | Closed | Wins | Losses | Win rate | Realized net USD | Next allocation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| GAMBLER | 3 | 0 | 3 | 0.0% | -0.1021 | 1.00x |
| HOUSE | 6 | 0 | 6 | 0.0% | -0.1206 | 1.00x |
| SPY | 5 | 1 | 4 | 20.0% | -0.0486 | 1.00x |
| MEME HUNTER | 4 | 2 | 2 | 50.0% | -0.0057 | 1.00x |
| BREAKOUT | 4 | 0 | 4 | 0.0% | -0.1994 | 1.00x |
| CONTRARIAN | 7 | 0 | 7 | 0.0% | -0.3125 | 1.00x |
| ROTATOR | 2 | 0 | 2 | 0.0% | -0.4172 | 1.00x |
| VORTEX | 22 | 1 | 21 | 4.5% | -2.8829 | 0.50x |
| FRACTAL | 12 | 1 | 11 | 8.3% | -1.2427 | 1.00x |
| SHOCKWAVE | 5 | 2 | 3 | 40.0% | -0.0131 | 1.00x |

## Where paper trades lost money

- **PILOT V1 trend turned down; next-candle simulated exit**: 19 exits; net USD -3.1191
- **Exploratory 15-minute observation complete (next-bar fill)**: 18 exits; net USD -0.1765
- **PILOT V1 fixed holding window reached; next-candle simulated exit**: 6 exits; net USD -0.9151
- **RSI normalized**: 5 exits; net USD -0.3018
- **Time-based exit**: 4 exits; net USD -0.3833
- **Breakout failed**: 3 exits; net USD -0.1827
- **Timescales disagree**: 2 exits; net USD -0.0146
- **Range normalized**: 2 exits; net USD -0.0870
- **Trend failure**: 1 exits; net USD -0.0072
- **Volume faded**: 1 exits; net USD -0.0095
- **Shockwave ended**: 1 exits; net USD -0.0095
- **PILOT V1 observed 6% stop; next-candle simulated exit**: 1 exits; net USD -0.5472

## Where paper trades made money

- **Exploratory 15-minute observation complete (next-bar fill)**: 5 exits; net USD +0.0132
- **PILOT V1 fixed holding window reached; next-candle simulated exit**: 1 exits; net USD +0.0087
- **PILOT V1 trend turned down; next-candle simulated exit**: 1 exits; net USD +0.3868

## How to interpret the results

A win rate alone is not a trading edge. We must examine risk-adjusted out-of-sample returns, sample size, market regime, costs, feed freshness and rejected decisions.
Position size decreases after at least 20 closed paper trades if expectancy is weak; this is bounded adaptive sizing, not a trained self-improving prediction model.
Scheduled sampling can miss interim price moves and delays stop triggers. Backtesting and paper trading are not proof of real profitability.
Latest unavailable Kraken pairs: none reported
