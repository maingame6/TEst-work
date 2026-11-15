# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1794704100; captured candles: 3494.
Missed fills: 23; censored exits: 36.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 11 | 0 | -2.5603% | -3.0463% | 2 | 0 |
| COST_AWARE | 2.172% | 17 | 0 | -2.7905% | -3.2754% | 2 | 0 |
| BALANCED_TEST | 1.200% | 107 | 0 | -2.4115% | -2.8982% | 31 | 0 |
| LOW_HURDLE_CONTROL | 0.500% | 497 | 1 | -2.2422% | -2.7298% | 175 | 0 |

## V4 gate diagnostics (from instrumentation onward; never reconstructed)
| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 19 | 34449 | 26366 | 13 | 10 | -2.5536% | 24.871% |
| COST_AWARE | 29 | 34435 | 26004 | 20 | 16 | -2.8008% | 38.250% |
| BALANCED_TEST | 199 | 34106 | 26004 | 118 | 85 | -2.3916% | 92.689% |
| LOW_HURDLE_CONTROL | 1035 | 31621 | 25597 | 524 | 408 | -2.2365% | 99.999% |

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
