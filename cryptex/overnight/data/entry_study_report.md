# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1795243200; captured candles: 4908.
Missed fills: 114; censored exits: 50.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 17 | 0 | -2.2359% | -2.7235% | 7 | 0 |
| COST_AWARE | 2.172% | 23 | 0 | -2.4907% | -2.9771% | 7 | 0 |
| BALANCED_TEST | 1.200% | 142 | 1 | -2.3535% | -2.8405% | 44 | 3 |
| LOW_HURDLE_CONTROL | 0.500% | 706 | 2 | -2.1854% | -2.6733% | 278 | 5 |

## V4 gate diagnostics (from instrumentation onward; never reconstructed)
| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 48 | 48822 | 37154 | 26 | 16 | -2.2115% | 31.975% |
| COST_AWARE | 60 | 48804 | 36618 | 35 | 22 | -2.4845% | 44.089% |
| BALANCED_TEST | 316 | 48290 | 36618 | 180 | 120 | -2.3288% | 96.621% |
| LOW_HURDLE_CONTROL | 1601 | 44431 | 36037 | 815 | 617 | -2.1735% | 100.000% |

## Fixed-duration counterfactual research (30m versus 4h and 24h)
Only exact same-signal pairs are eligible; heldout begins at the frozen +72h timestamp.
Trading costs and slippage are charged at both endpoints for each hypothetical exit.
Gaps censor long holds. Figures below are not independent across correlated symbols.

| Gate | Hold | Matched (all) | Independent heldout | Heldout avg net | Versus paired 30m |
|---|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 4h | 5 | 4 | -1.152% | +1.165% |
| V4_TAKER_STRICT | 24h | 1 | 1 | -2.441% | -0.027% |
| COST_AWARE | 4h | 6 | 4 | -0.847% | +1.412% |
| COST_AWARE | 24h | 1 | 1 | -2.441% | -0.027% |
| BALANCED_TEST | 4h | 75 | 22 | -1.865% | +0.283% |
| BALANCED_TEST | 24h | 19 | 3 | -2.551% | -0.287% |
| LOW_HURDLE_CONTROL | 4h | 264 | 42 | -2.244% | -0.005% |
| LOW_HURDLE_CONTROL | 24h | 51 | 5 | -4.723% | -2.458% |

A gate only places a *research candidate*, entered on a later observed candle.
No trade or price is backfilled. No automatic rollout to real or $210 paper strategies.
Six-candle exits are evaluation windows, not validated exit strategies.
