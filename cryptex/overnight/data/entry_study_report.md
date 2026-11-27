# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1795741200; captured candles: 6144.
Missed fills: 120; censored exits: 50.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 30 | 2 | -1.9267% | -2.4159% | 12 | 0 |
| COST_AWARE | 2.172% | 37 | 2 | -2.0772% | -2.5655% | 13 | 0 |
| BALANCED_TEST | 1.200% | 182 | 4 | -2.1821% | -2.6700% | 68 | 0 |
| LOW_HURDLE_CONTROL | 0.500% | 879 | 11 | -2.1148% | -2.6030% | 369 | 2 |

## V4 gate diagnostics (from instrumentation onward; never reconstructed)
| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 119 | 60158 | 45870 | 34 | 29 | -1.9026% | 45.080% |
| COST_AWARE | 139 | 60131 | 45215 | 44 | 36 | -2.0619% | 54.746% |
| BALANCED_TEST | 474 | 59488 | 45215 | 215 | 160 | -2.1400% | 98.212% |
| LOW_HURDLE_CONTROL | 2029 | 54866 | 44512 | 991 | 790 | -2.0976% | 100.000% |

## Fixed-duration counterfactual research (30m versus 4h and 24h)
Only exact same-signal pairs are eligible; heldout begins at the frozen +72h timestamp.
Trading costs and slippage are charged at both endpoints for each hypothetical exit.
Gaps censor long holds. Figures below are not independent across correlated symbols.

| Gate | Hold | Matched (all) | Independent heldout | Heldout avg net | Versus paired 30m |
|---|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 4h | 18 | 8 | -2.227% | +0.157% |
| V4_TAKER_STRICT | 24h | 12 | 3 | -2.861% | -0.377% |
| COST_AWARE | 4h | 20 | 8 | -1.817% | +0.242% |
| COST_AWARE | 24h | 13 | 3 | -2.861% | -0.377% |
| BALANCED_TEST | 4h | 106 | 30 | -1.759% | +0.239% |
| BALANCED_TEST | 24h | 39 | 6 | -2.724% | -0.804% |
| LOW_HURDLE_CONTROL | 4h | 375 | 60 | -2.143% | +0.043% |
| LOW_HURDLE_CONTROL | 24h | 95 | 8 | -3.142% | -0.892% |

A gate only places a *research candidate*, entered on a later observed candle.
No trade or price is backfilled. No automatic rollout to real or $210 paper strategies.
Six-candle exits are evaluation windows, not validated exit strategies.
