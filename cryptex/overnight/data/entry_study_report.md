# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1794344700; captured candles: 2457.
Missed fills: 1; censored exits: 5.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 5 | 0 | -2.1383% | -2.6264% | 1 | 0 |
| COST_AWARE | 2.172% | 7 | 0 | -2.7177% | -3.2029% | 1 | 0 |
| BALANCED_TEST | 1.200% | 72 | 0 | -2.3764% | -2.8633% | 21 | 0 |
| LOW_HURDLE_CONTROL | 0.500% | 325 | 1 | -2.2288% | -2.7165% | 118 | 3 |

## V4 gate diagnostics (from instrumentation onward; never reconstructed)
| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 7 | 22893 | 17519 | 5 | 4 | -2.0161% | 10.264% |
| COST_AWARE | 9 | 22889 | 17278 | 7 | 6 | -2.7329% | 17.586% |
| BALANCED_TEST | 105 | 22724 | 17278 | 70 | 50 | -2.3272% | 82.345% |
| LOW_HURDLE_CONTROL | 630 | 21203 | 16997 | 321 | 236 | -2.2140% | 99.935% |

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
| BALANCED_TEST | 4h | 39 | 11 | -1.332% | +0.448% |
| BALANCED_TEST | 24h | 4 | 1 | -0.463% | +1.241% |
| LOW_HURDLE_CONTROL | 4h | 123 | 21 | -2.211% | -0.077% |
| LOW_HURDLE_CONTROL | 24h | 18 | 2 | -5.120% | -2.534% |

A gate only places a *research candidate*, entered on a later observed candle.
No trade or price is backfilled. No automatic rollout to real or $210 paper strategies.
Six-candle exits are evaluation windows, not validated exit strategies.
