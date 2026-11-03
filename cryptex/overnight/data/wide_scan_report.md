# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-11-03T21:55:42.284729+00:00; scanning cycles: 35.
Discovered: 4228 distinct venue/pair listings.
Selected in scan batches: **4224**.
Checked against exchange metadata: **4224**.
Real 5m OHLCV requests attempted: **4224**.
Validated recent closed-candle histories: **3817**.
Venue/pairs producing historical strategy samples: **227**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1204 | 1201 | 1198 | 3 |
| coinbase | 865 | 865 | 463 | 403 |
| bitstamp | 235 | 234 | 234 | 0 |
| okx | 1039 | 1039 | 1039 | 0 |
| kucoin | 885 | 885 | 883 | 2 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 374 | 26 | 114 | -2.51867% |
| cost_aware_momentum | 82 | 14 | 15 | -2.53148% |
| breakout | 425 | 25 | 133 | -2.35974% |
| dip_recovery | 85 | 11 | 39 | -1.77801% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
