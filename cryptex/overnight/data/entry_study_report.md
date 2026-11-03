# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1793746200; captured candles: 853.
Missed fills: 0; censored exits: 1.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 1 | 0 | -2.6269% | -3.1126% | 0 | 0 |
| COST_AWARE | 2.172% | 1 | 0 | -2.6269% | -3.1126% | 0 | 0 |
| BALANCED_TEST | 1.200% | 22 | 0 | -2.4882% | -2.9745% | 6 | 0 |
| LOW_HURDLE_CONTROL | 0.500% | 89 | 1 | -2.2681% | -2.7555% | 31 | 0 |

## V4 gate diagnostics (from instrumentation onward; never reconstructed)
| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 1 | 7210 | 5517 | 1 | 0 | n/a | 2.627% |
| COST_AWARE | 1 | 7210 | 5433 | 1 | 0 | n/a | 2.627% |
| BALANCED_TEST | 23 | 7182 | 5433 | 19 | 0 | n/a | 42.595% |
| LOW_HURDLE_CONTROL | 175 | 6825 | 5339 | 77 | 0 | n/a | 87.049% |

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
| BALANCED_TEST | 4h | 9 | 0 | n/a | n/a |
| BALANCED_TEST | 24h | 2 | 0 | n/a | n/a |
| LOW_HURDLE_CONTROL | 4h | 22 | 0 | n/a | n/a |
| LOW_HURDLE_CONTROL | 24h | 6 | 0 | n/a | n/a |

A gate only places a *research candidate*, entered on a later observed candle.
No trade or price is backfilled. No automatic rollout to real or $210 paper strategies.
Six-candle exits are evaluation windows, not validated exit strategies.
