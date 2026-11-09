# CRYPTEX paper-trading results — automated review

**SIMULATED TRADING ONLY: no actual orders, earnings or exchange balances.**

Generated: 2026-11-09T12:07:59.577464+00:00
Data status: HEALTHY: paper trading on completed Kraken candles
Paper equity: USD 91.09; initial USD 100.00; change USD -8.91.
Closed trades: 101; wins 7; losses/breakevens 94.

## Specialist research teams

10 parent traders; 64 deterministic, correlated indicator-voters per parent = 640 transparent subagent evaluations per valid candle.
The specialist parameter sweeps do **not** mean 640 independent AI models or additional market feeds.
Votes may disagree; all votes are archived at `data/subagent_decisions.csv`. Parent fill results still come from `data/trades.csv`.

| Parent | Decision | Symbol | Favourable votes | Cautious votes | Vetoes |
| --- | --- | --- | ---: | ---: | ---: |
| GAMBLER | HOLD | BTC | 24 | 3 | 0 |
| HOUSE | HOLD | BTC | 10 | 17 | 0 |
| SPY | HOLD | SOL | 25 | 8 | 0 |
| MEME HUNTER | HOLD | DOGE | 28 | 6 | 0 |
| BREAKOUT | HOLD | BTC | 24 | 3 | 0 |
| CONTRARIAN | HOLD | BTC | 10 | 17 | 0 |
| ROTATOR | HOLD | BTC | 24 | 3 | 0 |
| VORTEX | HOLD | ETH | 22 | 9 | 0 |
| FRACTAL | HOLD | SOL | 25 | 8 | 0 |
| SHOCKWAVE | HOLD | DOGE | 28 | 6 | 0 |

## Bot performance

| Bot | Closed | Wins | Losses | Win rate | Realized net USD | Next allocation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| GAMBLER | 3 | 0 | 3 | 0.0% | -0.1021 | 1.00x |
| HOUSE | 8 | 0 | 8 | 0.0% | -0.2712 | 1.00x |
| SPY | 5 | 1 | 4 | 20.0% | -0.0486 | 1.00x |
| MEME HUNTER | 4 | 2 | 2 | 50.0% | -0.0057 | 1.00x |
| BREAKOUT | 4 | 0 | 4 | 0.0% | -0.1994 | 1.00x |
| CONTRARIAN | 9 | 0 | 9 | 0.0% | -0.5319 | 1.00x |
| ROTATOR | 3 | 0 | 3 | 0.0% | -0.5873 | 1.00x |
| VORTEX | 43 | 1 | 42 | 2.3% | -4.5881 | 0.50x |
| FRACTAL | 17 | 1 | 16 | 5.9% | -2.1251 | 1.00x |
| SHOCKWAVE | 5 | 2 | 3 | 40.0% | -0.0131 | 1.00x |

## Where paper trades lost money

- **PILOT V1 trend turned down; next-candle simulated exit**: 40 exits; net USD -4.8243
- **Exploratory 15-minute observation complete (next-bar fill)**: 18 exits; net USD -0.1765
- **PILOT V1 fixed holding window reached; next-candle simulated exit**: 12 exits; net USD -1.9677
- **RSI normalized**: 7 exits; net USD -0.5212
- **Range normalized**: 4 exits; net USD -0.2376
- **Time-based exit**: 4 exits; net USD -0.3833
- **Breakout failed**: 3 exits; net USD -0.1827
- **Timescales disagree**: 2 exits; net USD -0.0146
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
