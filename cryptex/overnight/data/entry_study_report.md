# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1794183600; captured candles: 2167.
Missed fills: 0; censored exits: 2.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 2 | 0 | -2.4964% | -2.9827% | 0 | 0 |
| COST_AWARE | 2.172% | 4 | 0 | -3.3314% | -3.8135% | 0 | 0 |
| BALANCED_TEST | 1.200% | 57 | 0 | -2.4851% | -2.9715% | 15 | 0 |
| LOW_HURDLE_CONTROL | 0.500% | 249 | 1 | -2.2611% | -2.7486% | 88 | 1 |

## V4 gate diagnostics (from instrumentation onward; never reconstructed)
| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2 | 19654 | 15038 | 2 | 1 | -2.3659% | 4.931% |
| COST_AWARE | 4 | 19650 | 14839 | 4 | 3 | -3.5662% | 12.688% |
| BALANCED_TEST | 84 | 19520 | 14839 | 54 | 35 | -2.4832% | 76.215% |
| LOW_HURDLE_CONTROL | 483 | 18351 | 14609 | 240 | 160 | -2.2573% | 99.665% |

## Fixed-duration counterfactual research (30m versus 4h and 24h)
Only exact same-signal pairs are eligible; heldout begins at the frozen +72h timestamp.
Trading costs and slippage are charged at both endpoints for each hypothetical exit.
Gaps censor long holds. Figures below are not independent across correlated symbols.

| Gate | Hold | Matched (all) | Independent heldout | Heldout avg net | Versus paired 30m |
|---|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 4h | 0 | 0 | n/a | n/a |
| V4_TAKER_STRICT | 24h | 0 | 0 | n/a | n/a |
| COST_AWARE | 4h | 0 | 0 | n/a | n/a |
| COST_AWARE | 24h | 0 | 0 | n/a | n/a |
| BALANCED_TEST | 4h | 26 | 8 | -2.040% | -0.145% |
| BALANCED_TEST | 24h | 3 | 0 | n/a | n/a |
| LOW_HURDLE_CONTROL | 4h | 95 | 17 | -2.276% | -0.059% |
| LOW_HURDLE_CONTROL | 24h | 13 | 1 | -3.758% | -0.959% |

A gate only places a *research candidate*, entered on a later observed candle.
No trade or price is backfilled. No automatic rollout to real or $210 paper strategies.
Six-candle exits are evaluation windows, not validated exit strategies.
