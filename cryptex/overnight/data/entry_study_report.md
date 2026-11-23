# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1795443300; captured candles: 5575.
Missed fills: 114; censored exits: 50.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 25 | 0 | -2.2976% | -2.7849% | 9 | 5 |
| COST_AWARE | 2.172% | 32 | 0 | -2.3904% | -2.8773% | 10 | 5 |
| BALANCED_TEST | 1.200% | 174 | 2 | -2.2584% | -2.7459% | 62 | 5 |
| LOW_HURDLE_CONTROL | 0.500% | 798 | 9 | -2.1200% | -2.6082% | 330 | 5 |

## V4 gate diagnostics (from instrumentation onward; never reconstructed)
| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 112 | 54523 | 41522 | 34 | 24 | -2.2839% | 44.128% |
| COST_AWARE | 132 | 54497 | 40926 | 44 | 31 | -2.3828% | 53.961% |
| BALANCED_TEST | 458 | 53884 | 40926 | 212 | 152 | -2.2251% | 98.134% |
| LOW_HURDLE_CONTROL | 1903 | 49645 | 40283 | 907 | 709 | -2.1014% | 100.000% |

## Fixed-duration counterfactual research (30m versus 4h and 24h)
Only exact same-signal pairs are eligible; heldout begins at the frozen +72h timestamp.
Trading costs and slippage are charged at both endpoints for each hypothetical exit.
Gaps censor long holds. Figures below are not independent across correlated symbols.

| Gate | Hold | Matched (all) | Independent heldout | Heldout avg net | Versus paired 30m |
|---|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 4h | 13 | 7 | -1.801% | +0.735% |
| V4_TAKER_STRICT | 24h | 6 | 2 | -1.803% | +0.817% |
| COST_AWARE | 4h | 15 | 7 | -1.332% | +0.832% |
| COST_AWARE | 24h | 7 | 2 | -1.803% | +0.817% |
| BALANCED_TEST | 4h | 99 | 27 | -1.711% | +0.391% |
| BALANCED_TEST | 24h | 33 | 5 | -1.740% | +0.299% |
| LOW_HURDLE_CONTROL | 4h | 322 | 52 | -1.979% | +0.209% |
| LOW_HURDLE_CONTROL | 24h | 78 | 7 | -3.079% | -0.760% |

A gate only places a *research candidate*, entered on a later observed candle.
No trade or price is backfilled. No automatic rollout to real or $210 paper strategies.
Six-candle exits are evaluation windows, not validated exit strategies.
