# Five-exchange PROSPECTIVE shadow experiment

**No real exchange orders. Not included in $210 paper wallet.**

This is NOT every-five-minute cross-exchange execution.

Markets with genuine post-deployment observations: 418
Distinct forward observations: 1472
Completed hypothetical round trips: 2
Censored entries: 6; censored exits: 0

Cash reference: 0%; fee-adjusted buy/hold markets: 23; mean after costs: -9.3498%.
Buy/hold holding periods differ and cannot establish strategy superiority.

| Exchange | Markets observed | Forward observations | Completed simulations |
|---|---:|---:|---:|
| kraken | 23 | 323 | 2 |
| coinbase | 233 | 437 | 0 |
| bitstamp | 9 | 259 | 0 |
| okx | 18 | 168 | 0 |
| kucoin | 135 | 285 | 0 |

| Prespecified gate | Completed | After-cost wins | Mean after costs | Stress mean | Max unit-stake DD |
|---|---:|---:|---:|---:|---:|
| STRICT_COST | 0 | 0 | n/a | n/a | 0.000% |
| LOW_HURDLE_CONTROL | 2 | 0 | -2.1148% | -2.6030% | 4.185% |

**Held-out evaluation**: boundary fixed at earliest truly observed forward candle plus 72h (no retrospective tuning).
| Gate | Held-out closes | Held-out mean net |
|---|---:|---:|
| STRICT_COST | 0 | n/a |
| LOW_HURDLE_CONTROL | 2 | -2.1148% |

Live orderbook snapshots and user-specific fee tiers are NOT proven. Repeated markets and venues share correlated outcomes. No missing signals or delayed fills are backfilled.
