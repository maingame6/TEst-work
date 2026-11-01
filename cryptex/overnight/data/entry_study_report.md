# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1793507700; captured candles: 63.
Missed fills: 0; censored exits: 1.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 0 | 0 | not measured | n/a | 0 | 0 |
| COST_AWARE | 2.172% | 0 | 0 | not measured | n/a | 0 | 0 |
| BALANCED_TEST | 1.200% | 1 | 0 | -2.1575% | -2.6455% | 0 | 0 |
| LOW_HURDLE_CONTROL | 0.500% | 4 | 0 | -2.0465% | -2.5351% | 1 | 1 |

A gate only places a *research candidate*, entered on a later observed candle.
No trade or price is backfilled. No automatic rollout to real or $210 paper strategies.
Six-candle exits are evaluation windows, not validated exit strategies.
