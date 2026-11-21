# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1795253700; captured candles: 4943.
Missed fills: 114; censored exits: 50.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 22 | 0 | -2.2675% | -2.7549% | 8 | 0 |
| COST_AWARE | 2.172% | 28 | 0 | -2.4700% | -2.9564% | 8 | 0 |
| BALANCED_TEST | 1.200% | 150 | 1 | -2.3028% | -2.7901% | 50 | 0 |
| LOW_HURDLE_CONTROL | 0.500% | 723 | 7 | -2.1548% | -2.6428% | 283 | 1 |

## V4 gate diagnostics (from instrumentation onward; never reconstructed)
| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 62 | 49261 | 37536 | 26 | 21 | -2.2503% | 39.679% |
| COST_AWARE | 74 | 49242 | 36995 | 35 | 27 | -2.4642% | 50.422% |
| BALANCED_TEST | 336 | 48707 | 36995 | 183 | 128 | -2.2710% | 96.983% |
| LOW_HURDLE_CONTROL | 1638 | 44808 | 36409 | 828 | 634 | -2.1389% | 100.000% |

## Fixed-duration counterfactual research (30m versus 4h and 24h)
Only exact same-signal pairs are eligible; heldout begins at the frozen +72h timestamp.
Trading costs and slippage are charged at both endpoints for each hypothetical exit.
Gaps censor long holds. Figures below are not independent across correlated symbols.

| Gate | Hold | Matched (all) | Independent heldout | Heldout avg net | Versus paired 30m |
|---|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 4h | 5 | 4 | -1.152% | +1.165% |
| V4_TAKER_STRICT | 24h | 1 | 1 | -2.441% | -0.027% |
| COST_AWARE | 4h | 6 | 4 | -0.847% | +1.412% |
| COST_AWARE | 24h | 1 | 1 | -2.441% | -0.027% |
| BALANCED_TEST | 4h | 75 | 22 | -1.865% | +0.283% |
| BALANCED_TEST | 24h | 19 | 3 | -2.551% | -0.287% |
| LOW_HURDLE_CONTROL | 4h | 272 | 43 | -2.211% | +0.039% |
| LOW_HURDLE_CONTROL | 24h | 52 | 5 | -4.723% | -2.458% |

A gate only places a *research candidate*, entered on a later observed candle.
No trade or price is backfilled. No automatic rollout to real or $210 paper strategies.
Six-candle exits are evaluation windows, not validated exit strategies.
