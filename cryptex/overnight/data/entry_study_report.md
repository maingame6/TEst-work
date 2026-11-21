# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1795246500; captured candles: 4919.
Missed fills: 114; censored exits: 50.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 22 | 0 | -2.2675% | -2.7549% | 8 | 0 |
| COST_AWARE | 2.172% | 28 | 0 | -2.4700% | -2.9564% | 8 | 0 |
| BALANCED_TEST | 1.200% | 147 | 1 | -2.3284% | -2.8156% | 47 | 0 |
| LOW_HURDLE_CONTROL | 0.500% | 716 | 7 | -2.1604% | -2.6484% | 278 | 0 |

## V4 gate diagnostics (from instrumentation onward; never reconstructed)
| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 62 | 48974 | 37299 | 26 | 21 | -2.2503% | 39.679% |
| COST_AWARE | 74 | 48955 | 36762 | 35 | 27 | -2.4642% | 50.422% |
| BALANCED_TEST | 333 | 48424 | 36762 | 180 | 125 | -2.3003% | 96.886% |
| LOW_HURDLE_CONTROL | 1620 | 44558 | 36178 | 820 | 627 | -2.1451% | 100.000% |

## Fixed-duration counterfactual research (30m versus 4h and 24h)
Only exact same-signal pairs are eligible; heldout begins at the frozen +72h timestamp.
Trading costs and slippage are charged at both endpoints for each hypothetical exit.
Gaps censor long holds. Figures below are not independent across correlated symbols.

| Gate | Hold | Matched (all) | Independent heldout | Heldout avg net | Versus paired 30m |
|---|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 4h | 5 | 4 | -1.152% | +1.165% |
| V4_TAKER_STRICT | 24h | 1 | 1 | -2.441% | -0.027% |
| COST_AWARE | 4h | 6 | 4 | -0.847% | +1.412% |
| COST_AWARE | 24h | 1 | 1 | -2.441% | -0.027% |
| BALANCED_TEST | 4h | 75 | 22 | -1.865% | +0.283% |
| BALANCED_TEST | 24h | 19 | 3 | -2.551% | -0.287% |
| LOW_HURDLE_CONTROL | 4h | 264 | 42 | -2.244% | -0.005% |
| LOW_HURDLE_CONTROL | 24h | 52 | 5 | -4.723% | -2.458% |

A gate only places a *research candidate*, entered on a later observed candle.
No trade or price is backfilled. No automatic rollout to real or $210 paper strategies.
Six-candle exits are evaluation windows, not validated exit strategies.
