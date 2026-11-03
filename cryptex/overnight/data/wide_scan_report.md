# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-11-03T17:49:09.205784+00:00; scanning cycles: 34.
Discovered: 4224 distinct venue/pair listings.
Selected in scan batches: **4224**.
Checked against exchange metadata: **4223**.
Real 5m OHLCV requests attempted: **4223**.
Validated recent closed-candle histories: **3808**.
Venue/pairs producing historical strategy samples: **226**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1201 | 1201 | 1198 | 3 |
| coinbase | 865 | 865 | 455 | 411 |
| bitstamp | 234 | 234 | 234 | 0 |
| okx | 1039 | 1039 | 1039 | 0 |
| kucoin | 885 | 885 | 882 | 3 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 372 | 25 | 114 | -2.53860% |
| cost_aware_momentum | 80 | 13 | 14 | -2.59767% |
| breakout | 432 | 24 | 137 | -2.36408% |
| dip_recovery | 85 | 11 | 39 | -1.77801% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
