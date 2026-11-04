# Five-exchange PROSPECTIVE shadow experiment

**No real exchange orders. Not included in $210 paper wallet.**

This is NOT every-five-minute cross-exchange execution.

Markets with genuine post-deployment observations: 269
Distinct forward observations: 580
Completed hypothetical round trips: 0
Censored entries: 0; censored exits: 0

Cash reference: 0%; fee-adjusted buy/hold markets: 22; mean after costs: -3.96922%.
Buy/hold holding periods differ and cannot establish strategy superiority.

| Exchange | Markets observed | Forward observations | Completed simulations |
|---|---:|---:|---:|
| kraken | 19 | 109 | 0 |
| coinbase | 112 | 168 | 0 |
| bitstamp | 6 | 81 | 0 |
| okx | 3 | 48 | 0 |
| kucoin | 129 | 174 | 0 |

| Prespecified gate | Completed | After-cost wins | Mean after costs | Stress mean | Max unit-stake DD |
|---|---:|---:|---:|---:|---:|
| STRICT_COST | 0 | 0 | n/a | n/a | 0.000% |
| LOW_HURDLE_CONTROL | 0 | 0 | n/a | n/a | 0.000% |

**Held-out evaluation**: boundary fixed at earliest truly observed forward candle plus 72h (no retrospective tuning).
| Gate | Held-out closes | Held-out mean net |
|---|---:|---:|
| STRICT_COST | 0 | n/a |
| LOW_HURDLE_CONTROL | 0 | n/a |

Live orderbook snapshots and user-specific fee tiers are NOT proven. Repeated markets and venues share correlated outcomes. No missing signals or delayed fills are backfilled.
