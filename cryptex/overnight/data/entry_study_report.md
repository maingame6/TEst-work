# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1794401100; captured candles: 2643.
Missed fills: 1; censored exits: 7.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 7 | 0 | -2.4898% | -2.9761% | 1 | 1 |
| COST_AWARE | 2.172% | 10 | 0 | -2.8163% | -3.3010% | 1 | 1 |
| BALANCED_TEST | 1.200% | 78 | 0 | -2.3989% | -2.8857% | 22 | 1 |
| LOW_HURDLE_CONTROL | 0.500% | 370 | 1 | -2.2385% | -2.7261% | 136 | 1 |

## V4 gate diagnostics (from instrumentation onward; never reconstructed)
| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 13 | 24569 | 18819 | 8 | 6 | -2.4669% | 16.209% |
| COST_AWARE | 16 | 24564 | 18557 | 11 | 9 | -2.8373% | 24.894% |
| BALANCED_TEST | 119 | 24386 | 18557 | 78 | 56 | -2.3638% | 84.991% |
| LOW_HURDLE_CONTROL | 703 | 22694 | 18251 | 366 | 281 | -2.2291% | 99.977% |

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
| LOW_HURDLE_CONTROL | 4h | 139 | 23 | -2.344% | -0.181% |
| LOW_HURDLE_CONTROL | 24h | 18 | 2 | -5.120% | -2.534% |

A gate only places a *research candidate*, entered on a later observed candle.
No trade or price is backfilled. No automatic rollout to real or $210 paper strategies.
Six-candle exits are evaluation windows, not validated exit strategies.
