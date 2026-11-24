# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1795526400; captured candles: 5852.
Missed fills: 114; censored exits: 50.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 30 | 2 | -1.9267% | -2.4159% | 12 | 0 |
| COST_AWARE | 2.172% | 37 | 2 | -2.0772% | -2.5655% | 13 | 0 |
| BALANCED_TEST | 1.200% | 180 | 4 | -2.1911% | -2.6790% | 66 | 0 |
| LOW_HURDLE_CONTROL | 0.500% | 846 | 11 | -2.1237% | -2.6119% | 344 | 0 |

## V4 gate diagnostics (from instrumentation onward; never reconstructed)
| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 119 | 57408 | 43755 | 34 | 29 | -1.9026% | 45.080% |
| COST_AWARE | 139 | 57381 | 43123 | 44 | 36 | -2.0619% | 54.746% |
| BALANCED_TEST | 471 | 56742 | 43123 | 213 | 158 | -2.1498% | 98.166% |
| LOW_HURDLE_CONTROL | 1974 | 52278 | 42451 | 950 | 757 | -2.1067% | 100.000% |

## Fixed-duration counterfactual research (30m versus 4h and 24h)
Only exact same-signal pairs are eligible; heldout begins at the frozen +72h timestamp.
Trading costs and slippage are charged at both endpoints for each hypothetical exit.
Gaps censor long holds. Figures below are not independent across correlated symbols.

| Gate | Hold | Matched (all) | Independent heldout | Heldout avg net | Versus paired 30m |
|---|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 4h | 18 | 8 | -2.227% | +0.157% |
| V4_TAKER_STRICT | 24h | 7 | 3 | -2.861% | -0.377% |
| COST_AWARE | 4h | 20 | 8 | -1.817% | +0.242% |
| COST_AWARE | 24h | 8 | 3 | -2.861% | -0.377% |
| BALANCED_TEST | 4h | 105 | 29 | -1.821% | +0.220% |
| BALANCED_TEST | 24h | 34 | 5 | -1.740% | +0.299% |
| LOW_HURDLE_CONTROL | 4h | 350 | 56 | -2.125% | +0.064% |
| LOW_HURDLE_CONTROL | 24h | 86 | 8 | -3.142% | -0.892% |

A gate only places a *research candidate*, entered on a later observed candle.
No trade or price is backfilled. No automatic rollout to real or $210 paper strategies.
Six-candle exits are evaluation windows, not validated exit strategies.
