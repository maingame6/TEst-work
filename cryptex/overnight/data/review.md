# CRYPTEX paper-trading results — automated review

**SIMULATED TRADING ONLY: no actual orders, earnings or exchange balances.**

Generated: 2026-10-30T21:39:59.257133+00:00
Data status: HEALTHY: paper trading on completed Kraken candles
Paper equity: USD 99.88; initial USD 100.00; change USD -0.12.
Closed trades: 0; wins 0; losses/breakevens 0.

## Specialist research teams

10 parent traders; 64 deterministic, correlated indicator-voters per parent = 640 transparent subagent evaluations per valid candle.
The specialist parameter sweeps do **not** mean 640 independent AI models or additional market feeds.
Votes may disagree; all votes are archived at `data/subagent_decisions.csv`. Parent fill results still come from `data/trades.csv`.

| Parent | Decision | Symbol | Favourable votes | Cautious votes | Vetoes |
| --- | --- | --- | ---: | ---: | ---: |
| GAMBLER | HOLD | ETH | 16 | 6 | 0 |
| HOUSE | HOLD | BTC | 15 | 8 | 1 |
| SPY | HOLD | PEPE | 12 | 26 | 1 |
| MEME HUNTER | HOLD | WIF | 31 | 13 | 1 |
| BREAKOUT | HOLD | SOL | 30 | 0 | 0 |
| CONTRARIAN | SELL | XRP | 10 | 12 | 0 |
| ROTATOR | HOLD | ADA | 29 | 2 | 0 |
| VORTEX | HOLD | ETH | 16 | 6 | 0 |
| FRACTAL | HOLD | ADA | 29 | 2 | 0 |
| SHOCKWAVE | HOLD | WIF | 31 | 13 | 1 |

## Bot performance

| Bot | Closed | Wins | Losses | Win rate | Realized net USD | Next allocation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| GAMBLER | 0 | 0 | 0 | — | +0.0000 | 1.00x |
| HOUSE | 0 | 0 | 0 | — | +0.0000 | 1.00x |
| SPY | 0 | 0 | 0 | — | +0.0000 | 1.00x |
| MEME HUNTER | 0 | 0 | 0 | — | +0.0000 | 1.00x |
| BREAKOUT | 0 | 0 | 0 | — | +0.0000 | 1.00x |
| CONTRARIAN | 0 | 0 | 0 | — | +0.0000 | 1.00x |
| ROTATOR | 0 | 0 | 0 | — | +0.0000 | 1.00x |
| VORTEX | 0 | 0 | 0 | — | +0.0000 | 1.00x |
| FRACTAL | 0 | 0 | 0 | — | +0.0000 | 1.00x |
| SHOCKWAVE | 0 | 0 | 0 | — | +0.0000 | 1.00x |

## Where paper trades lost money

No completed evidence yet.

## Where paper trades made money

No completed evidence yet.

## How to interpret the results

A win rate alone is not a trading edge. We must examine risk-adjusted out-of-sample returns, sample size, market regime, costs, feed freshness and rejected decisions.
Position size decreases after at least 20 closed paper trades if expectancy is weak; this is bounded adaptive sizing, not a trained self-improving prediction model.
Scheduled sampling can miss interim price moves and delays stop triggers. Backtesting and paper trading are not proof of real profitability.
Latest unavailable Kraken pairs: none reported
