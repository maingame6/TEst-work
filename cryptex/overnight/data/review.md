# CRYPTEX paper-trading results — automated review

**SIMULATED TRADING ONLY: no actual orders, earnings or exchange balances.**

Generated: 2026-10-30T22:47:05.690299+00:00
Data status: HEALTHY: paper trading on completed Kraken candles
Paper equity: USD 99.71; initial USD 100.00; change USD -0.29.
Closed trades: 15; wins 2; losses/breakevens 13.

## Specialist research teams

10 parent traders; 64 deterministic, correlated indicator-voters per parent = 640 transparent subagent evaluations per valid candle.
The specialist parameter sweeps do **not** mean 640 independent AI models or additional market feeds.
Votes may disagree; all votes are archived at `data/subagent_decisions.csv`. Parent fill results still come from `data/trades.csv`.

| Parent | Decision | Symbol | Favourable votes | Cautious votes | Vetoes |
| --- | --- | --- | ---: | ---: | ---: |
| GAMBLER | HOLD | SOL | 21 | 8 | 0 |
| HOUSE | BUY | ETH | 19 | 7 | 0 |
| SPY | BUY | PEPE | 25 | 14 | 0 |
| MEME HUNTER | BUY | PEPE | 25 | 14 | 0 |
| BREAKOUT | HOLD | SOL | 21 | 8 | 0 |
| CONTRARIAN | BUY | BTC | 4 | 20 | 0 |
| ROTATOR | HOLD | ADA | 22 | 5 | 0 |
| VORTEX | HOLD | ETH | 5 | 21 | 0 |
| FRACTAL | HOLD | PEPE | 25 | 14 | 0 |
| SHOCKWAVE | BUY | PEPE | 25 | 14 | 0 |

## Bot performance

| Bot | Closed | Wins | Losses | Win rate | Realized net USD | Next allocation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| GAMBLER | 2 | 0 | 2 | 0.0% | -0.0162 | 1.00x |
| HOUSE | 2 | 0 | 2 | 0.0% | -0.0154 | 1.00x |
| SPY | 2 | 0 | 2 | 0.0% | -0.0213 | 1.00x |
| MEME HUNTER | 2 | 1 | 1 | 50.0% | -0.0017 | 1.00x |
| BREAKOUT | 1 | 0 | 1 | 0.0% | -0.0538 | 1.00x |
| CONTRARIAN | 2 | 0 | 2 | 0.0% | -0.0141 | 1.00x |
| ROTATOR | 0 | 0 | 0 | — | +0.0000 | 1.00x |
| VORTEX | 0 | 0 | 0 | — | +0.0000 | 1.00x |
| FRACTAL | 2 | 0 | 2 | 0.0% | -0.0150 | 1.00x |
| SHOCKWAVE | 2 | 1 | 1 | 50.0% | -0.0017 | 1.00x |

## Where paper trades lost money

- **Exploratory 15-minute observation complete (next-bar fill)**: 9 exits; net USD -0.0756
- **RSI normalized**: 1 exits; net USD -0.0071
- **Breakout failed**: 1 exits; net USD -0.0538
- **Trend failure**: 1 exits; net USD -0.0072
- **Timescales disagree**: 1 exits; net USD -0.0072

## Where paper trades made money

- **Exploratory 15-minute observation complete (next-bar fill)**: 2 exits; net USD +0.0116

## How to interpret the results

A win rate alone is not a trading edge. We must examine risk-adjusted out-of-sample returns, sample size, market regime, costs, feed freshness and rejected decisions.
Position size decreases after at least 20 closed paper trades if expectancy is weak; this is bounded adaptive sizing, not a trained self-improving prediction model.
Scheduled sampling can miss interim price moves and delays stop triggers. Backtesting and paper trading are not proof of real profitability.
Latest unavailable Kraken pairs: none reported
