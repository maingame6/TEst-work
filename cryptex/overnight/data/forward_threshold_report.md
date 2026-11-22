# Frozen prospective book-momentum thresholds

**NO TRADES, NO CHANGES to the $210 accounts or existing V4 strategy.**
These four rules use a new **15-minute snapshot** signal, not the original 5m V4 feature.
Frozen at 2026-11-01T19:30:00+00:00

| Candidate | Move threshold | Completed hypotheses | Mean base-cost net | Stress-cost net | Promotable |
|---|---:|---:|---:|---:|---|
| STRICT_232BPS | 2.322% | 15 | -2.88682% | -3.37119% | No |
| COST_AWARE_217BPS | 2.172% | 27 | -2.33469% | -2.8218% | No |
| BALANCED_120BPS | 1.2% | 107 | -2.22819% | -2.71584% | No |
| CONTROL_50BPS | 0.5% | 794 | -1.92561% | -2.41477% | No |

Censored entries: 19
Censored exits: 31
Gaps: 390
Consecutive observed market-pair intervals: 23520 of 23910 observed transitions. These are NOT missing five-minute Kraken candles.

Cash benchmark: zero assumed. Matched buy/hold and statistically robust comparison NOT YET verified.
Fees are published-spot-tier or labeled assumptions; actual fills unverified.
Snapshots cannot establish actual fills or exchange account profitability.
