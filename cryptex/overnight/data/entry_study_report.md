# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1795803900; captured candles: 6353.
Missed fills: 120; censored exits: 50.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 31 | 2 | -1.9572% | -2.4462% | 12 | 0 |
| COST_AWARE | 2.172% | 38 | 2 | -2.0981% | -2.5863% | 13 | 0 |
| BALANCED_TEST | 1.200% | 187 | 4 | -2.1610% | -2.6489% | 73 | 1 |
| LOW_HURDLE_CONTROL | 0.500% | 914 | 11 | -2.1097% | -2.5979% | 387 | 5 |

## V4 gate diagnostics (from instrumentation onward; never reconstructed)
| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 121 | 62338 | 47513 | 35 | 30 | -1.9349% | 45.935% |
| COST_AWARE | 141 | 62311 | 46834 | 45 | 37 | -2.0838% | 55.450% |
| BALANCED_TEST | 486 | 61642 | 46834 | 221 | 165 | -2.1173% | 98.333% |
| LOW_HURDLE_CONTROL | 2122 | 56821 | 46104 | 1029 | 825 | -2.0926% | 100.000% |

## Fixed-duration counterfactual research (30m versus 4h and 24h)
Only exact same-signal pairs are eligible; heldout begins at the frozen +72h timestamp.
Trading costs and slippage are charged at both endpoints for each hypothetical exit.
Gaps censor long holds. Figures below are not independent across correlated symbols.

| Gate | Hold | Matched (all) | Independent heldout | Heldout avg net | Versus paired 30m |
|---|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 4h | 19 | 9 | -2.248% | +0.191% |
| V4_TAKER_STRICT | 24h | 12 | 3 | -2.861% | -0.377% |
| COST_AWARE | 4h | 21 | 9 | -1.883% | +0.266% |
| COST_AWARE | 24h | 13 | 3 | -2.861% | -0.377% |
| BALANCED_TEST | 4h | 111 | 31 | -1.735% | +0.253% |
| BALANCED_TEST | 24h | 40 | 7 | -2.794% | -1.037% |
| LOW_HURDLE_CONTROL | 4h | 391 | 63 | -2.182% | -0.002% |
| LOW_HURDLE_CONTROL | 24h | 102 | 9 | -2.742% | -0.502% |

A gate only places a *research candidate*, entered on a later observed candle.
No trade or price is backfilled. No automatic rollout to real or $210 paper strategies.
Six-candle exits are evaluation windows, not validated exit strategies.
