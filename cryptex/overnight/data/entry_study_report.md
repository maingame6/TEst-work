# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1793638200; captured candles: 494.
Missed fills: 0; censored exits: 1.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 0 | 0 | not measured | n/a | 0 | 1 |
| COST_AWARE | 2.172% | 0 | 0 | not measured | n/a | 0 | 1 |
| BALANCED_TEST | 1.200% | 8 | 0 | -2.5381% | -3.0242% | 2 | 1 |
| LOW_HURDLE_CONTROL | 0.500% | 44 | 1 | -2.2325% | -2.7201% | 15 | 1 |

## V4 gate diagnostics (from instrumentation onward; never reconstructed)
| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 1 | 3406 | 2570 | 1 | 0 | n/a | 0.000% |
| COST_AWARE | 1 | 3406 | 2536 | 1 | 0 | n/a | 0.000% |
| BALANCED_TEST | 7 | 3398 | 2536 | 6 | 0 | n/a | 18.603% |
| LOW_HURDLE_CONTROL | 74 | 3266 | 2501 | 33 | 0 | n/a | 63.003% |

A gate only places a *research candidate*, entered on a later observed candle.
No trade or price is backfilled. No automatic rollout to real or $210 paper strategies.
Six-candle exits are evaluation windows, not validated exit strategies.
