# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1794216900; captured candles: 2278.
Missed fills: 0; censored exits: 2.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 3 | 0 | -2.6106% | -3.0963% | 0 | 0 |
| COST_AWARE | 2.172% | 5 | 0 | -3.2329% | -3.7155% | 0 | 0 |
| BALANCED_TEST | 1.200% | 63 | 0 | -2.3829% | -2.8698% | 19 | 0 |
| LOW_HURDLE_CONTROL | 0.500% | 275 | 1 | -2.2348% | -2.7225% | 101 | 0 |

## V4 gate diagnostics (from instrumentation onward; never reconstructed)
| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 3 | 20810 | 15928 | 3 | 2 | -2.6024% | 7.630% |
| COST_AWARE | 5 | 20806 | 15714 | 5 | 4 | -3.3844% | 15.167% |
| BALANCED_TEST | 91 | 20659 | 15714 | 60 | 41 | -2.3264% | 78.162% |
| LOW_HURDLE_CONTROL | 522 | 19363 | 15473 | 264 | 186 | -2.2190% | 99.801% |

## Fixed-duration counterfactual research (30m versus 4h and 24h)
Only exact same-signal pairs are eligible; heldout begins at the frozen +72h timestamp.
Trading costs and slippage are charged at both endpoints for each hypothetical exit.
Gaps censor long holds. Figures below are not independent across correlated symbols.

| Gate | Hold | Matched (all) | Independent heldout | Heldout avg net | Versus paired 30m |
|---|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 4h | 1 | 1 | -4.247% | -1.408% |
| V4_TAKER_STRICT | 24h | 0 | 0 | n/a | n/a |
| COST_AWARE | 4h | 2 | 1 | -3.681% | +0.254% |
| COST_AWARE | 24h | 0 | 0 | n/a | n/a |
| BALANCED_TEST | 4h | 33 | 9 | -1.891% | +0.104% |
| BALANCED_TEST | 24h | 3 | 0 | n/a | n/a |
| LOW_HURDLE_CONTROL | 4h | 107 | 19 | -2.346% | -0.105% |
| LOW_HURDLE_CONTROL | 24h | 14 | 2 | -5.120% | -2.534% |

A gate only places a *research candidate*, entered on a later observed candle.
No trade or price is backfilled. No automatic rollout to real or $210 paper strategies.
Six-candle exits are evaluation windows, not validated exit strategies.
