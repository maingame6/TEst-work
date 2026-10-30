# CRYPTEX paper-trading results — automated review

**SIMULATED TRADING ONLY: no actual orders, earnings or exchange balances.**

Generated: 2026-10-30T22:16:35.702473+00:00
Data status: HEALTHY: paper trading on completed Kraken candles
Paper equity: USD 99.84; initial USD 100.00; change USD -0.16.
Closed trades: 7; wins 0; losses/breakevens 7.

## Specialist research teams

10 parent traders; 64 deterministic, correlated indicator-voters per parent = 640 transparent subagent evaluations per valid candle.
The specialist parameter sweeps do **not** mean 640 independent AI models or additional market feeds.
Votes may disagree; all votes are archived at `data/subagent_decisions.csv`. Parent fill results still come from `data/trades.csv`.

| Parent | Decision | Symbol | Favourable votes | Cautious votes | Vetoes |
| --- | --- | --- | ---: | ---: | ---: |
| GAMBLER | BUY | BTC | 7 | 10 | 0 |
| HOUSE | BUY | ETH | 12 | 7 | 0 |
| SPY | BUY | SOL | 20 | 5 | 0 |
| MEME HUNTER | BUY | PEPE | 6 | 31 | 0 |
| BREAKOUT | HOLD | SOL | 20 | 5 | 0 |
| CONTRARIAN | BUY | XRP | 9 | 13 | 0 |
| ROTATOR | HOLD | ADA | 21 | 7 | 1 |
| VORTEX | HOLD | ETH | 6 | 13 | 0 |
| FRACTAL | BUY | BTC | 7 | 10 | 0 |
| SHOCKWAVE | BUY | PEPE | 6 | 31 | 0 |

## Bot performance

| Bot | Closed | Wins | Losses | Win rate | Realized net USD | Next allocation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| GAMBLER | 1 | 0 | 1 | 0.0% | -0.0089 | 1.00x |
| HOUSE | 1 | 0 | 1 | 0.0% | -0.0085 | 1.00x |
| SPY | 1 | 0 | 1 | 0.0% | -0.0173 | 1.00x |
| MEME HUNTER | 1 | 0 | 1 | 0.0% | -0.0075 | 1.00x |
| BREAKOUT | 0 | 0 | 0 | — | +0.0000 | 1.00x |
| CONTRARIAN | 1 | 0 | 1 | 0.0% | -0.0071 | 1.00x |
| ROTATOR | 0 | 0 | 0 | — | +0.0000 | 1.00x |
| VORTEX | 0 | 0 | 0 | — | +0.0000 | 1.00x |
| FRACTAL | 1 | 0 | 1 | 0.0% | -0.0078 | 1.00x |
| SHOCKWAVE | 1 | 0 | 1 | 0.0% | -0.0075 | 1.00x |

## Where paper trades lost money

- **Exploratory 15-minute observation complete (next-bar fill)**: 6 exits; net USD -0.0577
- **RSI normalized**: 1 exits; net USD -0.0071

## Where paper trades made money

No completed evidence yet.

## How to interpret the results

A win rate alone is not a trading edge. We must examine risk-adjusted out-of-sample returns, sample size, market regime, costs, feed freshness and rejected decisions.
Position size decreases after at least 20 closed paper trades if expectancy is weak; this is bounded adaptive sizing, not a trained self-improving prediction model.
Scheduled sampling can miss interim price moves and delays stop triggers. Backtesting and paper trading are not proof of real profitability.
Latest unavailable Kraken pairs: none reported
