# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1794394800; captured candles: 2622.
Missed fills: 1; censored exits: 7.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 6 | 0 | -2.2836% | -2.7709% | 1 | 0 |
| COST_AWARE | 2.172% | 9 | 0 | -2.7150% | -3.2003% | 1 | 0 |
| BALANCED_TEST | 1.200% | 76 | 0 | -2.3868% | -2.8737% | 22 | 1 |
| LOW_HURDLE_CONTROL | 0.500% | 367 | 1 | -2.2385% | -2.7261% | 135 | 2 |

## V4 gate diagnostics (from instrumentation onward; never reconstructed)
| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 8 | 24384 | 18675 | 6 | 5 | -2.2149% | 12.965% |
| COST_AWARE | 11 | 24379 | 18415 | 9 | 8 | -2.7260% | 21.986% |
| BALANCED_TEST | 113 | 24203 | 18415 | 76 | 54 | -2.3455% | 84.095% |
| LOW_HURDLE_CONTROL | 694 | 22521 | 18111 | 362 | 278 | -2.2291% | 99.976% |

## Fixed-duration counterfactual research (30m versus 4h and 24h)
Only exact same-signal pairs are eligible; heldout begins at the frozen +72h timestamp.
Trading costs and slippage are charged at both endpoints for each hypothetical exit.
Gaps censor long holds. Figures below are not independent across correlated symbols.

| Gate | Hold | Matched (all) | Independent heldout | Heldout avg net | Versus paired 30m |
|---|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 4h | 2 | 2 | -0.868% | +0.694% |
| V4_TAKER_STRICT | 24h | 0 | 0 | n/a | n/a |
| COST_AWARE | 4h | 3 | 2 | -0.585% | +1.525% |
| COST_AWARE | 24h | 0 | 0 | n/a | n/a |
| BALANCED_TEST | 4h | 41 | 12 | -1.449% | +0.428% |
| BALANCED_TEST | 24h | 4 | 1 | -0.463% | +1.241% |
| LOW_HURDLE_CONTROL | 4h | 133 | 23 | -2.344% | -0.181% |
| LOW_HURDLE_CONTROL | 24h | 18 | 2 | -5.120% | -2.534% |

A gate only places a *research candidate*, entered on a later observed candle.
No trade or price is backfilled. No automatic rollout to real or $210 paper strategies.
Six-candle exits are evaluation windows, not validated exit strategies.
