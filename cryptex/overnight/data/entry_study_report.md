# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1795265400; captured candles: 4982.
Missed fills: 114; censored exits: 50.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 22 | 0 | -2.2675% | -2.7549% | 8 | 0 |
| COST_AWARE | 2.172% | 28 | 0 | -2.4700% | -2.9564% | 8 | 0 |
| BALANCED_TEST | 1.200% | 155 | 1 | -2.2991% | -2.7864% | 52 | 0 |
| LOW_HURDLE_CONTROL | 0.500% | 732 | 7 | -2.1529% | -2.6409% | 289 | 5 |

## V4 gate diagnostics (from instrumentation onward; never reconstructed)
| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 62 | 49686 | 37862 | 26 | 21 | -2.2503% | 39.679% |
| COST_AWARE | 74 | 49667 | 37319 | 35 | 27 | -2.4642% | 50.422% |
| BALANCED_TEST | 345 | 49122 | 37319 | 188 | 133 | -2.2679% | 97.299% |
| LOW_HURDLE_CONTROL | 1672 | 45160 | 36728 | 841 | 643 | -2.1369% | 100.000% |

## Fixed-duration counterfactual research (30m versus 4h and 24h)
Only exact same-signal pairs are eligible; heldout begins at the frozen +72h timestamp.
Trading costs and slippage are charged at both endpoints for each hypothetical exit.
Gaps censor long holds. Figures below are not independent across correlated symbols.

| Gate | Hold | Matched (all) | Independent heldout | Heldout avg net | Versus paired 30m |
|---|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 4h | 10 | 5 | -1.454% | +0.964% |
| V4_TAKER_STRICT | 24h | 1 | 1 | -2.441% | -0.027% |
| COST_AWARE | 4h | 11 | 5 | -1.210% | +1.162% |
| COST_AWARE | 24h | 1 | 1 | -2.441% | -0.027% |
| BALANCED_TEST | 4h | 80 | 23 | -1.807% | +0.286% |
| BALANCED_TEST | 24h | 19 | 3 | -2.551% | -0.287% |
| LOW_HURDLE_CONTROL | 4h | 278 | 44 | -2.138% | +0.109% |
| LOW_HURDLE_CONTROL | 24h | 54 | 5 | -4.723% | -2.458% |

A gate only places a *research candidate*, entered on a later observed candle.
No trade or price is backfilled. No automatic rollout to real or $210 paper strategies.
Six-candle exits are evaluation windows, not validated exit strategies.
