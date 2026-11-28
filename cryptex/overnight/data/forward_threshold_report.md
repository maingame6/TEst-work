# Frozen prospective book-momentum thresholds

**NO TRADES, NO CHANGES to the $210 accounts or existing V4 strategy.**
These four rules use a new **15-minute snapshot** signal, not the original 5m V4 feature.
Frozen at 2026-11-01T19:30:00+00:00

| Candidate | Move threshold | Completed hypotheses | Mean base-cost net | Stress-cost net | Promotable |
|---|---:|---:|---:|---:|---|
| STRICT_232BPS | 2.322% | 29 | -2.94744% | -3.4315% | No |
| COST_AWARE_217BPS | 2.172% | 41 | -2.5661% | -3.05206% | No |
| BALANCED_120BPS | 1.2% | 124 | -2.33376% | -2.82088% | No |
| CONTROL_50BPS | 0.5% | 981 | -1.99375% | -2.48257% | No |

Censored entries: 20
Censored exits: 38
Gaps: 420
Consecutive observed market-pair intervals: 30030 of 30450 observed transitions. These are NOT missing five-minute Kraken candles.

Cash benchmark: zero assumed. Matched buy/hold and statistically robust comparison NOT YET verified.
Fees are published-spot-tier or labeled assumptions; actual fills unverified.
Snapshots cannot establish actual fills or exchange account profitability.
