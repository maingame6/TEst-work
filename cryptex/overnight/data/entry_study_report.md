# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1795028400; captured candles: 4192.
Missed fills: 114; censored exits: 50.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 17 | 0 | -2.2359% | -2.7235% | 7 | 0 |
| COST_AWARE | 2.172% | 23 | 0 | -2.4907% | -2.9771% | 7 | 0 |
| BALANCED_TEST | 1.200% | 125 | 1 | -2.3698% | -2.8567% | 39 | 0 |
| LOW_HURDLE_CONTROL | 0.500% | 570 | 2 | -2.1998% | -2.6876% | 218 | 3 |

## V4 gate diagnostics (from instrumentation onward; never reconstructed)
| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 39 | 40870 | 31262 | 21 | 16 | -2.2115% | 31.975% |
| COST_AWARE | 51 | 40853 | 30839 | 30 | 22 | -2.4845% | 44.089% |
| BALANCED_TEST | 271 | 40432 | 30839 | 158 | 103 | -2.3445% | 95.038% |
| LOW_HURDLE_CONTROL | 1324 | 37348 | 30360 | 677 | 481 | -2.1872% | 100.000% |

## Fixed-duration counterfactual research (30m versus 4h and 24h)
Only exact same-signal pairs are eligible; heldout begins at the frozen +72h timestamp.
Trading costs and slippage are charged at both endpoints for each hypothetical exit.
Gaps censor long holds. Figures below are not independent across correlated symbols.

| Gate | Hold | Matched (all) | Independent heldout | Heldout avg net | Versus paired 30m |
|---|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 4h | 5 | 4 | -1.152% | +1.165% |
| V4_TAKER_STRICT | 24h | 0 | 0 | n/a | n/a |
| COST_AWARE | 4h | 6 | 4 | -0.847% | +1.412% |
| COST_AWARE | 24h | 0 | 0 | n/a | n/a |
| BALANCED_TEST | 4h | 56 | 16 | -1.206% | +0.781% |
| BALANCED_TEST | 24h | 4 | 1 | -0.463% | +1.241% |
| LOW_HURDLE_CONTROL | 4h | 178 | 31 | -2.098% | +0.112% |
| LOW_HURDLE_CONTROL | 24h | 18 | 2 | -5.120% | -2.534% |

A gate only places a *research candidate*, entered on a later observed candle.
No trade or price is backfilled. No automatic rollout to real or $210 paper strategies.
Six-candle exits are evaluation windows, not validated exit strategies.
