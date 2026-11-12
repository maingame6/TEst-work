# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1794524100; captured candles: 3011.
Missed fills: 1; censored exits: 14.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 8 | 0 | -2.2682% | -2.7556% | 2 | 0 |
| COST_AWARE | 2.172% | 12 | 0 | -2.6187% | -3.1044% | 2 | 0 |
| BALANCED_TEST | 1.200% | 94 | 0 | -2.4206% | -2.9072% | 27 | 0 |
| LOW_HURDLE_CONTROL | 0.500% | 438 | 1 | -2.2290% | -2.7167% | 163 | 0 |

## V4 gate diagnostics (from instrumentation onward; never reconstructed)
| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 13 | 28709 | 22002 | 8 | 7 | -2.2170% | 16.810% |
| COST_AWARE | 18 | 28702 | 21686 | 12 | 11 | -2.6180% | 27.331% |
| BALANCED_TEST | 149 | 28480 | 21686 | 98 | 72 | -2.3999% | 90.040% |
| LOW_HURDLE_CONTROL | 849 | 26449 | 21343 | 433 | 349 | -2.2191% | 99.995% |

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
