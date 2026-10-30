# CRYPTEX paper-trading results — automated review

**SIMULATED TRADING ONLY: no actual orders, earnings or exchange balances.**

Generated: 2026-10-30T22:26:39.958421+00:00
Data status: HEALTHY: paper trading on completed Kraken candles
Paper equity: USD 99.75; initial USD 100.00; change USD -0.25.
Closed trades: 8; wins 0; losses/breakevens 8.

## Specialist research teams

10 parent traders; 64 deterministic, correlated indicator-voters per parent = 640 transparent subagent evaluations per valid candle.
The specialist parameter sweeps do **not** mean 640 independent AI models or additional market feeds.
Votes may disagree; all votes are archived at `data/subagent_decisions.csv`. Parent fill results still come from `data/trades.csv`.

| Parent | Decision | Symbol | Favourable votes | Cautious votes | Vetoes |
| --- | --- | --- | ---: | ---: | ---: |
| GAMBLER | SELL | BTC | 8 | 16 | 0 |
| HOUSE | HOLD | ETH | 26 | 6 | 0 |
| SPY | HOLD | SOL | 19 | 5 | 0 |
| MEME HUNTER | HOLD | PEPE | 6 | 35 | 0 |
| BREAKOUT | SELL | SOL | 19 | 5 | 0 |
| CONTRARIAN | HOLD | XRP | 12 | 7 | 0 |
| ROTATOR | HOLD | ADA | 10 | 19 | 1 |
| VORTEX | HOLD | ETH | 5 | 27 | 0 |
| FRACTAL | SELL | BTC | 8 | 16 | 0 |
| SHOCKWAVE | HOLD | PEPE | 6 | 35 | 0 |

## Bot performance

| Bot | Closed | Wins | Losses | Win rate | Realized net USD | Next allocation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| GAMBLER | 1 | 0 | 1 | 0.0% | -0.0089 | 1.00x |
| HOUSE | 1 | 0 | 1 | 0.0% | -0.0085 | 1.00x |
| SPY | 1 | 0 | 1 | 0.0% | -0.0173 | 1.00x |
| MEME HUNTER | 1 | 0 | 1 | 0.0% | -0.0075 | 1.00x |
| BREAKOUT | 1 | 0 | 1 | 0.0% | -0.0538 | 1.00x |
| CONTRARIAN | 1 | 0 | 1 | 0.0% | -0.0071 | 1.00x |
| ROTATOR | 0 | 0 | 0 | — | +0.0000 | 1.00x |
| VORTEX | 0 | 0 | 0 | — | +0.0000 | 1.00x |
| FRACTAL | 1 | 0 | 1 | 0.0% | -0.0078 | 1.00x |
| SHOCKWAVE | 1 | 0 | 1 | 0.0% | -0.0075 | 1.00x |

## Where paper trades lost money

- **Exploratory 15-minute observation complete (next-bar fill)**: 6 exits; net USD -0.0577
- **RSI normalized**: 1 exits; net USD -0.0071
- **Breakout failed**: 1 exits; net USD -0.0538

## Where paper trades made money

No completed evidence yet.

## How to interpret the results

A win rate alone is not a trading edge. We must examine risk-adjusted out-of-sample returns, sample size, market regime, costs, feed freshness and rejected decisions.
Position size decreases after at least 20 closed paper trades if expectancy is weak; this is bounded adaptive sizing, not a trained self-improving prediction model.
Scheduled sampling can miss interim price moves and delays stop triggers. Backtesting and paper trading are not proof of real profitability.
Latest unavailable Kraken pairs: none reported
