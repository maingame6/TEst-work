# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1793627100; captured candles: 459.
Missed fills: 0; censored exits: 1.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 0 | 0 | not measured | n/a | 0 | 0 |
| COST_AWARE | 2.172% | 0 | 0 | not measured | n/a | 0 | 0 |
| BALANCED_TEST | 1.200% | 6 | 0 | -2.3283% | -2.8155% | 2 | 2 |
| LOW_HURDLE_CONTROL | 0.500% | 39 | 1 | -2.1183% | -2.6065% | 15 | 5 |

## V4 gate diagnostics (from instrumentation onward; never reconstructed)
| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 0 | 2969 | 2236 | 0 | 0 | n/a | 0.000% |
| COST_AWARE | 0 | 2969 | 2203 | 0 | 0 | n/a | 0.000% |
| BALANCED_TEST | 6 | 2961 | 2203 | 5 | 0 | n/a | 13.188% |
| LOW_HURDLE_CONTROL | 72 | 2836 | 2171 | 32 | 0 | n/a | 56.641% |

A gate only places a *research candidate*, entered on a later observed candle.
No trade or price is backfilled. No automatic rollout to real or $210 paper strategies.
Six-candle exits are evaluation windows, not validated exit strategies.
