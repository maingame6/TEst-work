# CRYPTEX paper-trading results — automated review

**SIMULATED TRADING ONLY: no actual orders, earnings or exchange balances.**

Generated: 2026-10-30T23:12:31.758155+00:00
Data status: HEALTHY: paper trading on completed Kraken candles
Paper equity: USD 99.74; initial USD 100.00; change USD -0.26.
Closed trades: 21; wins 5; losses/breakevens 16.

## Specialist research teams

10 parent traders; 64 deterministic, correlated indicator-voters per parent = 640 transparent subagent evaluations per valid candle.
The specialist parameter sweeps do **not** mean 640 independent AI models or additional market feeds.
Votes may disagree; all votes are archived at `data/subagent_decisions.csv`. Parent fill results still come from `data/trades.csv`.

| Parent | Decision | Symbol | Favourable votes | Cautious votes | Vetoes |
| --- | --- | --- | ---: | ---: | ---: |
| GAMBLER | HOLD | SOL | 29 | 2 | 0 |
| HOUSE | SELL | ETH | 9 | 16 | 0 |
| SPY | SELL | PEPE | 43 | 3 | 0 |
| MEME HUNTER | SELL | PEPE | 43 | 3 | 0 |
| BREAKOUT | HOLD | SOL | 29 | 2 | 0 |
| CONTRARIAN | SELL | XRP | 4 | 21 | 0 |
| ROTATOR | HOLD | ADA | 23 | 6 | 2 |
| VORTEX | HOLD | ETH | 14 | 11 | 0 |
| FRACTAL | HOLD | PEPE | 43 | 3 | 0 |
| SHOCKWAVE | SELL | PEPE | 43 | 3 | 0 |

## Bot performance

| Bot | Closed | Wins | Losses | Win rate | Realized net USD | Next allocation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| GAMBLER | 2 | 0 | 2 | 0.0% | -0.0162 | 1.00x |
| HOUSE | 3 | 0 | 3 | 0.0% | -0.0234 | 1.00x |
| SPY | 3 | 1 | 2 | 33.3% | -0.0208 | 1.00x |
| MEME HUNTER | 3 | 2 | 1 | 66.7% | -0.0012 | 1.00x |
| BREAKOUT | 1 | 0 | 1 | 0.0% | -0.0538 | 1.00x |
| CONTRARIAN | 3 | 0 | 3 | 0.0% | -0.0244 | 1.00x |
| ROTATOR | 0 | 0 | 0 | — | +0.0000 | 1.00x |
| VORTEX | 0 | 0 | 0 | — | +0.0000 | 1.00x |
| FRACTAL | 3 | 0 | 3 | 0.0% | -0.0224 | 1.00x |
| SHOCKWAVE | 3 | 2 | 1 | 66.7% | -0.0012 | 1.00x |

## Where paper trades lost money

- **Exploratory 15-minute observation complete (next-bar fill)**: 10 exits; net USD -0.0836
- **RSI normalized**: 2 exits; net USD -0.0174
- **Timescales disagree**: 2 exits; net USD -0.0146
- **Breakout failed**: 1 exits; net USD -0.0538
- **Trend failure**: 1 exits; net USD -0.0072

## Where paper trades made money

- **Exploratory 15-minute observation complete (next-bar fill)**: 5 exits; net USD +0.0132

## How to interpret the results

A win rate alone is not a trading edge. We must examine risk-adjusted out-of-sample returns, sample size, market regime, costs, feed freshness and rejected decisions.
Position size decreases after at least 20 closed paper trades if expectancy is weak; this is bounded adaptive sizing, not a trained self-improving prediction model.
Scheduled sampling can miss interim price moves and delays stop triggers. Backtesting and paper trading are not proof of real profitability.
Latest unavailable Kraken pairs: none reported
