# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1795747200; captured candles: 6164.
Missed fills: 120; censored exits: 50.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 30 | 2 | -1.9267% | -2.4159% | 12 | 1 |
| COST_AWARE | 2.172% | 37 | 2 | -2.0772% | -2.5655% | 13 | 1 |
| BALANCED_TEST | 1.200% | 187 | 4 | -2.1610% | -2.6489% | 73 | 0 |
| LOW_HURDLE_CONTROL | 0.500% | 886 | 11 | -2.1106% | -2.5989% | 375 | 0 |

## V4 gate diagnostics (from instrumentation onward; never reconstructed)
| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 121 | 60340 | 45987 | 35 | 29 | -1.9026% | 45.080% |
| COST_AWARE | 141 | 60313 | 45330 | 45 | 36 | -2.0619% | 54.746% |
| BALANCED_TEST | 485 | 59660 | 45330 | 220 | 165 | -2.1173% | 98.333% |
| LOW_HURDLE_CONTROL | 2068 | 54992 | 44626 | 996 | 797 | -2.0930% | 100.000% |

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
