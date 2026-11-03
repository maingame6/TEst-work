# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1793728800; captured candles: 795.
Missed fills: 0; censored exits: 1.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 1 | 0 | -2.6269% | -3.1126% | 0 | 0 |
| COST_AWARE | 2.172% | 1 | 0 | -2.6269% | -3.1126% | 0 | 0 |
| BALANCED_TEST | 1.200% | 21 | 0 | -2.4646% | -2.9511% | 6 | 0 |
| LOW_HURDLE_CONTROL | 0.500% | 86 | 1 | -2.2759% | -2.7633% | 29 | 0 |

## V4 gate diagnostics (from instrumentation onward; never reconstructed)
| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 1 | 6688 | 5114 | 1 | 0 | n/a | 2.627% |
| COST_AWARE | 1 | 6688 | 5034 | 1 | 0 | n/a | 2.627% |
| BALANCED_TEST | 22 | 6661 | 5034 | 18 | 0 | n/a | 40.830% |
| LOW_HURDLE_CONTROL | 171 | 6311 | 4949 | 75 | 0 | n/a | 86.220% |

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
| BALANCED_TEST | 4h | 8 | 0 | n/a | n/a |
| BALANCED_TEST | 24h | 0 | 0 | n/a | n/a |
| LOW_HURDLE_CONTROL | 4h | 19 | 0 | n/a | n/a |
| LOW_HURDLE_CONTROL | 24h | 0 | 0 | n/a | n/a |

A gate only places a *research candidate*, entered on a later observed candle.
No trade or price is backfilled. No automatic rollout to real or $210 paper strategies.
Six-candle exits are evaluation windows, not validated exit strategies.
