# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1793980200; captured candles: 1508.
Missed fills: 0; censored exits: 2.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 2 | 0 | -2.4964% | -2.9827% | 0 | 0 |
| COST_AWARE | 2.172% | 2 | 0 | -2.4964% | -2.9827% | 0 | 0 |
| BALANCED_TEST | 1.200% | 49 | 0 | -2.3854% | -2.8723% | 14 | 0 |
| LOW_HURDLE_CONTROL | 0.500% | 202 | 1 | -2.2446% | -2.7321% | 73 | 1 |

## V4 gate diagnostics (from instrumentation onward; never reconstructed)
| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2 | 14591 | 11128 | 2 | 1 | -2.3659% | 4.931% |
| COST_AWARE | 2 | 14590 | 10981 | 2 | 1 | -2.3659% | 4.931% |
| BALANCED_TEST | 70 | 14495 | 10981 | 46 | 27 | -2.3018% | 69.406% |
| LOW_HURDLE_CONTROL | 395 | 13554 | 10809 | 192 | 113 | -2.2261% | 98.985% |

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
| BALANCED_TEST | 4h | 20 | 6 | -2.191% | -0.346% |
| BALANCED_TEST | 24h | 3 | 0 | n/a | n/a |
| LOW_HURDLE_CONTROL | 4h | 65 | 9 | -1.735% | +0.454% |
| LOW_HURDLE_CONTROL | 24h | 7 | 0 | n/a | n/a |

A gate only places a *research candidate*, entered on a later observed candle.
No trade or price is backfilled. No automatic rollout to real or $210 paper strategies.
Six-candle exits are evaluation windows, not validated exit strategies.
