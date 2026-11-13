# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1794596100; captured candles: 3235.
Missed fills: 1; censored exits: 30.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 10 | 0 | -2.4230% | -2.9097% | 2 | 0 |
| COST_AWARE | 2.172% | 15 | 0 | -2.7447% | -3.2297% | 2 | 0 |
| BALANCED_TEST | 1.200% | 100 | 0 | -2.3888% | -2.8757% | 31 | 0 |
| LOW_HURDLE_CONTROL | 0.500% | 480 | 1 | -2.2254% | -2.7131% | 174 | 0 |

## V4 gate diagnostics (from instrumentation onward; never reconstructed)
| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 18 | 31470 | 24115 | 12 | 9 | -2.4004% | 21.795% |
| COST_AWARE | 27 | 31458 | 23782 | 18 | 14 | -2.7531% | 34.185% |
| BALANCED_TEST | 185 | 31178 | 23782 | 109 | 78 | -2.3608% | 91.121% |
| LOW_HURDLE_CONTROL | 977 | 28903 | 23412 | 481 | 391 | -2.2157% | 99.998% |

## Fixed-duration counterfactual research (30m versus 4h and 24h)
Only exact same-signal pairs are eligible; heldout begins at the frozen +72h timestamp.
Trading costs and slippage are charged at both endpoints for each hypothetical exit.
Gaps censor long holds. Figures below are not independent across correlated symbols.

| Gate | Hold | Matched (all) | Independent heldout | Heldout avg net | Versus paired 30m |
|---|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 4h | 4 | 3 | -1.570% | +0.714% |
| V4_TAKER_STRICT | 24h | 0 | 0 | n/a | n/a |
| COST_AWARE | 4h | 5 | 3 | -1.164% | +1.043% |
| COST_AWARE | 24h | 0 | 0 | n/a | n/a |
| BALANCED_TEST | 4h | 50 | 15 | -1.459% | +0.537% |
| BALANCED_TEST | 24h | 4 | 1 | -0.463% | +1.241% |
| LOW_HURDLE_CONTROL | 4h | 162 | 27 | -2.329% | -0.140% |
| LOW_HURDLE_CONTROL | 24h | 18 | 2 | -5.120% | -2.534% |

A gate only places a *research candidate*, entered on a later observed candle.
No trade or price is backfilled. No automatic rollout to real or $210 paper strategies.
Six-candle exits are evaluation windows, not validated exit strategies.
