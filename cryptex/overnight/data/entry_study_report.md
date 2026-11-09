# CRYPTEX — prospective entry threshold research

**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**

Last observed closed candle: 1794228900; captured candles: 2318.
Missed fills: 0; censored exits: 2.

Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.

| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 2.322% | 3 | 0 | -2.6106% | -3.0963% | 0 | 1 |
| COST_AWARE | 2.172% | 5 | 0 | -3.2329% | -3.7155% | 0 | 1 |
| BALANCED_TEST | 1.200% | 66 | 0 | -2.3906% | -2.8774% | 19 | 1 |
| LOW_HURDLE_CONTROL | 0.500% | 282 | 1 | -2.2332% | -2.7209% | 103 | 4 |

## V4 gate diagnostics (from instrumentation onward; never reconstructed)
| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |
|---|---:|---:|---:|---:|---:|---:|---:|
| V4_TAKER_STRICT | 5 | 21243 | 16263 | 4 | 2 | -2.6024% | 7.630% |
| COST_AWARE | 7 | 21239 | 16043 | 6 | 4 | -3.3844% | 15.167% |
| BALANCED_TEST | 96 | 21089 | 16043 | 64 | 44 | -2.3418% | 79.792% |
| LOW_HURDLE_CONTROL | 548 | 19735 | 15796 | 275 | 193 | -2.2172% | 99.830% |

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
| BALANCED_TEST | 4h | 36 | 10 | -1.716% | +0.213% |
| BALANCED_TEST | 24h | 4 | 1 | -0.463% | +1.241% |
| LOW_HURDLE_CONTROL | 4h | 115 | 20 | -2.279% | -0.071% |
| LOW_HURDLE_CONTROL | 24h | 17 | 2 | -5.120% | -2.534% |

A gate only places a *research candidate*, entered on a later observed candle.
No trade or price is backfilled. No automatic rollout to real or $210 paper strategies.
Six-candle exits are evaluation windows, not validated exit strategies.
