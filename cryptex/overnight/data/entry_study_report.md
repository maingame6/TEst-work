# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1795896000; captured candles: 6660.
Missed fills: 120; censored exits: 50.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 31 | 2 | -1.9572% | -2.4462% | 12 | 0 |
| COST_AWARE | 2.172% | 38 | 2 | -2.0981% | -2.5863% | 13 | 0 |
| BALANCED_TEST | 1.200% | 188 | 4 | -2.1613% | -2.6493% | 73 | 0 |
| LOW_HURDLE_CONTROL | 0.500% | 926 | 11 | -2.1112% | -2.5995% | 391 | 0 |

## V4 gate diagnostics (from instrumentation onward; never reconstructed)
| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 121 | 64496 | 49199 | 35 | 30 | -1.9349% | 45.935% |
| COST_AWARE | 141 | 64469 | 48494 | 45 | 37 | -2.0838% | 55.450% |
| BALANCED_TEST | 486 | 63800 | 48494 | 221 | 166 | -2.1180% | 98.370% |
| LOW_HURDLE_CONTROL | 2130 | 58955 | 47742 | 1036 | 837 | -2.0946% | 100.000% |

## Fixed-duration counterfactual research (30m versus 4h and 24h)
Only exact same-signal pairs are eligible; heldout begins at the frozen +72h timestamp.
Trading costs and slippage are charged at both endpoints for each hypothetical exit.
Gaps censor long holds. Figures below are not independent across correlated symbols.

| Gate | Hold | Matched (all) | Independent heldout | Heldout avg net | Versus paired 30m |
|---|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 4h | 19 | 9 | -2.248% | +0.191% |
| V4_TAKER_STRICT | 24h | 13 | 4 | -3.038% | -0.457% |
| COST_AWARE | 4h | 21 | 9 | -1.883% | +0.266% |
| COST_AWARE | 24h | 14 | 4 | -3.038% | -0.457% |
| BALANCED_TEST | 4h | 112 | 32 | -1.751% | +0.244% |
| BALANCED_TEST | 24h | 44 | 7 | -2.794% | -1.037% |
| LOW_HURDLE_CONTROL | 4h | 405 | 67 | -2.224% | -0.057% |
| LOW_HURDLE_CONTROL | 24h | 112 | 10 | -2.554% | -0.332% |

A gate only places a *research candidate*, entered on a later observed candle.
No trade or price is backfilled. No automatic rollout to real or $210 paper strategies.
Six-candle exits are evaluation windows, not validated exit strategies.
