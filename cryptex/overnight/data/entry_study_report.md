# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1793776500; captured candles: 954.
Missed fills: 0; censored exits: 1.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 1 | 0 | -2.6269% | -3.1126% | 0 | 0 |
| COST_AWARE | 2.172% | 1 | 0 | -2.6269% | -3.1126% | 0 | 0 |
| BALANCED_TEST | 1.200% | 32 | 0 | -2.5135% | -2.9998% | 8 | 0 |
| LOW_HURDLE_CONTROL | 0.500% | 118 | 1 | -2.2888% | -2.7762% | 40 | 1 |

## V4 gate diagnostics (from instrumentation onward; never reconstructed)
| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 1 | 8515 | 6496 | 1 | 0 | n/a | 2.627% |
| COST_AWARE | 1 | 8514 | 6399 | 1 | 0 | n/a | 2.627% |
| BALANCED_TEST | 39 | 8459 | 6399 | 30 | 10 | -2.5694% | 55.758% |
| LOW_HURDLE_CONTROL | 241 | 7934 | 6292 | 109 | 29 | -2.3526% | 93.510% |

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
| BALANCED_TEST | 4h | 10 | 1 | -2.492% | +0.452% |
| BALANCED_TEST | 24h | 3 | 0 | n/a | n/a |
| LOW_HURDLE_CONTROL | 4h | 29 | 1 | -0.561% | +1.501% |
| LOW_HURDLE_CONTROL | 24h | 6 | 0 | n/a | n/a |

A gate only places a *research candidate*, entered on a later observed candle.
No trade or price is backfilled. No automatic rollout to real or $210 paper strategies.
Six-candle exits are evaluation windows, not validated exit strategies.
