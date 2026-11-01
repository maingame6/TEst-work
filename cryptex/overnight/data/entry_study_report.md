# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1793537100; captured candles: 161.
Missed fills: 0; censored exits: 1.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 0 | 0 | not measured | n/a | 0 | 0 |
| COST_AWARE | 2.172% | 0 | 0 | not measured | n/a | 0 | 0 |
| BALANCED_TEST | 1.200% | 3 | 0 | -2.1519% | -2.6399% | 1 | 0 |
| LOW_HURDLE_CONTROL | 0.500% | 15 | 1 | -1.9676% | -2.4566% | 5 | 1 |

## V4 gate diagnostics (from instrumentation onward; never reconstructed)
| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 0 | 395 | 301 | 0 | 0 | n/a | 0.000% |
| COST_AWARE | 0 | 395 | 295 | 0 | 0 | n/a | 0.000% |
| BALANCED_TEST | 0 | 395 | 295 | 0 | 0 | n/a | 6.320% |
| LOW_HURDLE_CONTROL | 7 | 383 | 292 | 4 | 0 | n/a | 25.810% |

A gate only places a *research candidate*, entered on a later observed candle.
No trade or price is backfilled. No automatic rollout to real or $210 paper strategies.
Six-candle exits are evaluation windows, not validated exit strategies.
