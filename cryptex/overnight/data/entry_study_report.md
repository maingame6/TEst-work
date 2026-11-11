# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1794364200; captured candles: 2520.
Missed fills: 1; censored exits: 7.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 6 | 0 | -2.2836% | -2.7709% | 1 | 0 |
| COST_AWARE | 2.172% | 8 | 0 | -2.7542% | -3.2393% | 1 | 0 |
| BALANCED_TEST | 1.200% | 74 | 0 | -2.3969% | -2.8837% | 21 | 0 |
| LOW_HURDLE_CONTROL | 0.500% | 341 | 1 | -2.2357% | -2.7233% | 126 | 0 |

## V4 gate diagnostics (from instrumentation onward; never reconstructed)
| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 8 | 23521 | 18008 | 6 | 5 | -2.2149% | 12.965% |
| COST_AWARE | 10 | 23517 | 17763 | 8 | 7 | -2.7724% | 20.067% |
| BALANCED_TEST | 109 | 23347 | 17763 | 73 | 52 | -2.3582% | 83.434% |
| LOW_HURDLE_CONTROL | 653 | 21769 | 17473 | 335 | 252 | -2.2243% | 99.956% |

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
