# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1793642400; captured candles: 507.
Missed fills: 0; censored exits: 1.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 1 | 0 | -2.6269% | -3.1126% | 0 | 0 |
| COST_AWARE | 2.172% | 1 | 0 | -2.6269% | -3.1126% | 0 | 0 |
| BALANCED_TEST | 1.200% | 9 | 0 | -2.5479% | -3.0340% | 2 | 0 |
| LOW_HURDLE_CONTROL | 0.500% | 45 | 1 | -2.2412% | -2.7288% | 15 | 0 |

## V4 gate diagnostics (from instrumentation onward; never reconstructed)
| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 1 | 3619 | 2710 | 1 | 0 | n/a | 2.627% |
| COST_AWARE | 1 | 3619 | 2672 | 1 | 0 | n/a | 2.627% |
| BALANCED_TEST | 7 | 3611 | 2672 | 6 | 0 | n/a | 20.741% |
| LOW_HURDLE_CONTROL | 78 | 3461 | 2637 | 37 | 0 | n/a | 63.975% |

A gate only places a *research candidate*, entered on a later observed candle.
No trade or price is backfilled. No automatic rollout to real or $210 paper strategies.
Six-candle exits are evaluation windows, not validated exit strategies.
