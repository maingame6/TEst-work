# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1795491000; captured candles: 5734.
Missed fills: 114; censored exits: 50.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 30 | 2 | -1.9267% | -2.4159% | 12 | 0 |
| COST_AWARE | 2.172% | 37 | 2 | -2.0772% | -2.5655% | 13 | 0 |
| BALANCED_TEST | 1.200% | 179 | 4 | -2.1973% | -2.6851% | 65 | 0 |
| LOW_HURDLE_CONTROL | 0.500% | 828 | 11 | -2.1221% | -2.6103% | 336 | 3 |

## V4 gate diagnostics (from instrumentation onward; never reconstructed)
| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 119 | 56396 | 42995 | 34 | 29 | -1.9026% | 45.080% |
| COST_AWARE | 139 | 56369 | 42376 | 44 | 36 | -2.0619% | 54.746% |
| BALANCED_TEST | 470 | 55733 | 42376 | 212 | 157 | -2.1566% | 98.166% |
| LOW_HURDLE_CONTROL | 1952 | 51338 | 41709 | 936 | 739 | -2.1045% | 100.000% |

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
| BALANCED_TEST | 4h | 104 | 28 | -1.836% | +0.238% |
| BALANCED_TEST | 24h | 34 | 5 | -1.740% | +0.299% |
| LOW_HURDLE_CONTROL | 4h | 342 | 54 | -2.082% | +0.092% |
| LOW_HURDLE_CONTROL | 24h | 82 | 7 | -3.079% | -0.760% |

A gate only places a *research candidate*, entered on a later observed candle.
No trade or price is backfilled. No automatic rollout to real or $210 paper strategies.
Six-candle exits are evaluation windows, not validated exit strategies.
