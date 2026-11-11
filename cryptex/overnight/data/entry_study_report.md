# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1794408300; captured candles: 2667.
Missed fills: 1; censored exits: 7.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 8 | 0 | -2.2682% | -2.7556% | 2 | 0 |
| COST_AWARE | 2.172% | 11 | 0 | -2.6254% | -3.1111% | 2 | 0 |
| BALANCED_TEST | 1.200% | 81 | 0 | -2.3864% | -2.8733% | 23 | 0 |
| LOW_HURDLE_CONTROL | 0.500% | 380 | 1 | -2.2290% | -2.7166% | 142 | 2 |

## V4 gate diagnostics (from instrumentation onward; never reconstructed)
| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 13 | 24786 | 18977 | 8 | 7 | -2.2170% | 16.810% |
| COST_AWARE | 16 | 24781 | 18712 | 11 | 10 | -2.6253% | 25.433% |
| BALANCED_TEST | 122 | 24600 | 18712 | 80 | 59 | -2.3485% | 85.903% |
| LOW_HURDLE_CONTROL | 719 | 22879 | 18403 | 376 | 291 | -2.2170% | 99.981% |

## Fixed-duration counterfactual research (30m versus 4h and 24h)
Only exact same-signal pairs are eligible; heldout begins at the frozen +72h timestamp.
Trading costs and slippage are charged at both endpoints for each hypothetical exit.
Gaps censor long holds. Figures below are not independent across correlated symbols.

| Gate | Hold | Matched (all) | Independent heldout | Heldout avg net | Versus paired 30m |
|---|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 4h | 2 | 2 | -0.868% | +0.694% |
| V4_TAKER_STRICT | 24h | 0 | 0 | n/a | n/a |
| COST_AWARE | 4h | 4 | 3 | -1.164% | +1.043% |
| COST_AWARE | 24h | 0 | 0 | n/a | n/a |
| BALANCED_TEST | 4h | 43 | 13 | -1.516% | +0.402% |
| BALANCED_TEST | 24h | 4 | 1 | -0.463% | +1.241% |
| LOW_HURDLE_CONTROL | 4h | 143 | 24 | -2.271% | -0.165% |
| LOW_HURDLE_CONTROL | 24h | 18 | 2 | -5.120% | -2.534% |

A gate only places a *research candidate*, entered on a later observed candle.
No trade or price is backfilled. No automatic rollout to real or $210 paper strategies.
Six-candle exits are evaluation windows, not validated exit strategies.
