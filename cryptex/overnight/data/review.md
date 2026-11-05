# CRYPTEX paper-trading results — automated review

**SIMULATED TRADING ONLY: no actual orders, earnings or exchange balances.**

Generated: 2026-11-05T06:11:35.393928+00:00
Data status: HEALTHY: paper trading on completed Kraken candles
Paper equity: USD 97.04; initial USD 100.00; change USD -2.96.
Closed trades: 59; wins 7; losses/breakevens 52.

## Specialist research teams

10 parent traders; 64 deterministic, correlated indicator-voters per parent = 640 transparent subagent evaluations per valid candle.
The specialist parameter sweeps do **not** mean 640 independent AI models or additional market feeds.
Votes may disagree; all votes are archived at `data/subagent_decisions.csv`. Parent fill results still come from `data/trades.csv`.

| Parent | Decision | Symbol | Favourable votes | Cautious votes | Vetoes |
| --- | --- | --- | ---: | ---: | ---: |
| GAMBLER | HOLD | BTC | 4 | 17 | 0 |
| HOUSE | HOLD | BTC | 18 | 3 | 0 |
| SPY | HOLD | SOL | 6 | 22 | 1 |
| MEME HUNTER | HOLD | DOGE | 8 | 20 | 0 |
| BREAKOUT | HOLD | BTC | 4 | 17 | 0 |
| CONTRARIAN | HOLD | BTC | 18 | 3 | 0 |
| ROTATOR | HOLD | BTC | 4 | 17 | 0 |
| VORTEX | SELL | ETH | 6 | 19 | 0 |
| FRACTAL | HOLD | SOL | 6 | 22 | 1 |
| SHOCKWAVE | HOLD | DOGE | 8 | 20 | 0 |

## Bot performance

| Bot | Closed | Wins | Losses | Win rate | Realized net USD | Next allocation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| GAMBLER | 3 | 0 | 3 | 0.0% | -0.1021 | 1.00x |
| HOUSE | 6 | 0 | 6 | 0.0% | -0.1206 | 1.00x |
| SPY | 5 | 1 | 4 | 20.0% | -0.0486 | 1.00x |
| MEME HUNTER | 4 | 2 | 2 | 50.0% | -0.0057 | 1.00x |
| BREAKOUT | 4 | 0 | 4 | 0.0% | -0.1994 | 1.00x |
| CONTRARIAN | 6 | 0 | 6 | 0.0% | -0.0463 | 1.00x |
| ROTATOR | 1 | 0 | 1 | 0.0% | -0.1467 | 1.00x |
| VORTEX | 16 | 1 | 15 | 6.2% | -1.9747 | 1.00x |
| FRACTAL | 9 | 1 | 8 | 11.1% | -0.4258 | 1.00x |
| SHOCKWAVE | 5 | 2 | 3 | 40.0% | -0.0131 | 1.00x |

## Where paper trades lost money

- **Exploratory 15-minute observation complete (next-bar fill)**: 18 exits; net USD -0.1765
- **PILOT V1 trend turned down; next-candle simulated exit**: 13 exits; net USD -2.2110
- **RSI normalized**: 4 exits; net USD -0.0356
- **Time-based exit**: 4 exits; net USD -0.3833
- **Breakout failed**: 3 exits; net USD -0.1827
- **PILOT V1 fixed holding window reached; next-candle simulated exit**: 3 exits; net USD -0.3749
- **Timescales disagree**: 2 exits; net USD -0.0146
- **Range normalized**: 2 exits; net USD -0.0870
- **Trend failure**: 1 exits; net USD -0.0072
- **Volume faded**: 1 exits; net USD -0.0095
- **Shockwave ended**: 1 exits; net USD -0.0095

## Where paper trades made money

- **Exploratory 15-minute observation complete (next-bar fill)**: 5 exits; net USD +0.0132
- **PILOT V1 fixed holding window reached; next-candle simulated exit**: 1 exits; net USD +0.0087
- **PILOT V1 trend turned down; next-candle simulated exit**: 1 exits; net USD +0.3868

## How to interpret the results

A win rate alone is not a trading edge. We must examine risk-adjusted out-of-sample returns, sample size, market regime, costs, feed freshness and rejected decisions.
Position size decreases after at least 20 closed paper trades if expectancy is weak; this is bounded adaptive sizing, not a trained self-improving prediction model.
Scheduled sampling can miss interim price moves and delays stop triggers. Backtesting and paper trading are not proof of real profitability.
Latest unavailable Kraken pairs: none reported
