# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1795449900; captured candles: 5597.
Missed fills: 114; censored exits: 50.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 30 | 2 | -1.9267% | -2.4159% | 12 | 0 |
| COST_AWARE | 2.172% | 37 | 2 | -2.0772% | -2.5655% | 13 | 0 |
| BALANCED_TEST | 1.200% | 179 | 4 | -2.1973% | -2.6851% | 65 | 0 |
| LOW_HURDLE_CONTROL | 0.500% | 811 | 11 | -2.1165% | -2.6047% | 333 | 0 |

## V4 gate diagnostics (from instrumentation onward; never reconstructed)
| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 119 | 54914 | 41864 | 34 | 29 | -1.9026% | 45.080% |
| COST_AWARE | 139 | 54887 | 41264 | 44 | 36 | -2.0619% | 54.746% |
| BALANCED_TEST | 470 | 54253 | 41264 | 212 | 157 | -2.1566% | 98.166% |
| LOW_HURDLE_CONTROL | 1929 | 49978 | 40616 | 916 | 722 | -2.0979% | 100.000% |

## Fixed-duration counterfactual research (30m versus 4h and 24h)
Only exact same-signal pairs are eligible; heldout begins at the frozen +72h timestamp.
Trading costs and slippage are charged at both endpoints for each hypothetical exit.
Gaps censor long holds. Figures below are not independent across correlated symbols.

| Gate | Hold | Matched (all) | Independent heldout | Heldout avg net | Versus paired 30m |
|---|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 4h | 13 | 7 | -1.801% | +0.735% |
| V4_TAKER_STRICT | 24h | 6 | 2 | -1.803% | +0.817% |
| COST_AWARE | 4h | 15 | 7 | -1.332% | +0.832% |
| COST_AWARE | 24h | 7 | 2 | -1.803% | +0.817% |
| BALANCED_TEST | 4h | 99 | 27 | -1.711% | +0.391% |
| BALANCED_TEST | 24h | 33 | 5 | -1.740% | +0.299% |
| LOW_HURDLE_CONTROL | 4h | 322 | 52 | -1.979% | +0.209% |
| LOW_HURDLE_CONTROL | 24h | 81 | 7 | -3.079% | -0.760% |

A gate only places a *research candidate*, entered on a later observed candle.
No trade or price is backfilled. No automatic rollout to real or $210 paper strategies.
Six-candle exits are evaluation windows, not validated exit strategies.
