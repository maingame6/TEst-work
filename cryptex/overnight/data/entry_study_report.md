# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1795269900; captured candles: 4997.
Missed fills: 114; censored exits: 50.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 23 | 0 | -2.3189% | -2.8061% | 8 | 1 |
| COST_AWARE | 2.172% | 29 | 0 | -2.4219% | -2.9086% | 9 | 2 |
| BALANCED_TEST | 1.200% | 157 | 2 | -2.2740% | -2.7614% | 53 | 4 |
| LOW_HURDLE_CONTROL | 0.500% | 742 | 9 | -2.1328% | -2.6209% | 297 | 5 |

## V4 gate diagnostics (from instrumentation onward; never reconstructed)
| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 64 | 49892 | 37994 | 28 | 22 | -2.3049% | 41.760% |
| COST_AWARE | 78 | 49871 | 37447 | 38 | 28 | -2.4146% | 50.955% |
| BALANCED_TEST | 373 | 49295 | 37447 | 194 | 135 | -2.2391% | 97.317% |
| LOW_HURDLE_CONTROL | 1717 | 45287 | 36855 | 851 | 653 | -2.1144% | 100.000% |

## Fixed-duration counterfactual research (30m versus 4h and 24h)
Only exact same-signal pairs are eligible; heldout begins at the frozen +72h timestamp.
Trading costs and slippage are charged at both endpoints for each hypothetical exit.
Gaps censor long holds. Figures below are not independent across correlated symbols.

| Gate | Hold | Matched (all) | Independent heldout | Heldout avg net | Versus paired 30m |
|---|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 4h | 10 | 5 | -1.454% | +0.964% |
| V4_TAKER_STRICT | 24h | 1 | 1 | -2.441% | -0.027% |
| COST_AWARE | 4h | 11 | 5 | -1.210% | +1.162% |
| COST_AWARE | 24h | 1 | 1 | -2.441% | -0.027% |
| BALANCED_TEST | 4h | 80 | 23 | -1.807% | +0.286% |
| BALANCED_TEST | 24h | 19 | 3 | -2.551% | -0.287% |
| LOW_HURDLE_CONTROL | 4h | 280 | 44 | -2.138% | +0.109% |
| LOW_HURDLE_CONTROL | 24h | 54 | 5 | -4.723% | -2.458% |

A gate only places a *research candidate*, entered on a later observed candle.
No trade or price is backfilled. No automatic rollout to real or $210 paper strategies.
Six-candle exits are evaluation windows, not validated exit strategies.
