# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1795398900; captured candles: 5427.
Missed fills: 114; censored exits: 50.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 24 | 0 | -2.3012% | -2.7885% | 9 | 0 |
| COST_AWARE | 2.172% | 31 | 0 | -2.3962% | -2.8830% | 10 | 0 |
| BALANCED_TEST | 1.200% | 169 | 2 | -2.2653% | -2.7528% | 58 | 0 |
| LOW_HURDLE_CONTROL | 0.500% | 784 | 9 | -2.1275% | -2.6157% | 320 | 0 |

## V4 gate diagnostics (from instrumentation onward; never reconstructed)
| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 64 | 53264 | 40581 | 28 | 23 | -2.2871% | 42.865% |
| COST_AWARE | 78 | 53243 | 40005 | 38 | 30 | -2.3885% | 52.920% |
| BALANCED_TEST | 386 | 52653 | 40005 | 202 | 147 | -2.2320% | 97.934% |
| LOW_HURDLE_CONTROL | 1791 | 48506 | 39374 | 888 | 695 | -2.1096% | 100.000% |

## Fixed-duration counterfactual research (30m versus 4h and 24h)
Only exact same-signal pairs are eligible; heldout begins at the frozen +72h timestamp.
Trading costs and slippage are charged at both endpoints for each hypothetical exit.
Gaps censor long holds. Figures below are not independent across correlated symbols.

| Gate | Hold | Matched (all) | Independent heldout | Heldout avg net | Versus paired 30m |
|---|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 4h | 12 | 6 | -1.673% | +0.917% |
| V4_TAKER_STRICT | 24h | 6 | 2 | -1.803% | +0.817% |
| COST_AWARE | 4h | 14 | 6 | -1.125% | +1.030% |
| COST_AWARE | 24h | 7 | 2 | -1.803% | +0.817% |
| BALANCED_TEST | 4h | 94 | 26 | -1.684% | +0.420% |
| BALANCED_TEST | 24h | 29 | 4 | -2.543% | -0.351% |
| LOW_HURDLE_CONTROL | 4h | 311 | 50 | -2.014% | +0.211% |
| LOW_HURDLE_CONTROL | 24h | 73 | 6 | -4.129% | -1.693% |

A gate only places a *research candidate*, entered on a later observed candle.
No trade or price is backfilled. No automatic rollout to real or $210 paper strategies.
Six-candle exits are evaluation windows, not validated exit strategies.
