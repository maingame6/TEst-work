# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-11-09T18:43:40.710490+00:00; scanning cycles: 67.
Discovered: 4212 distinct venue/pair listings.
Selected in scan batches: **4207**.
Checked against exchange metadata: **4207**.
Real 5m OHLCV requests attempted: **4207**.
Validated recent closed-candle histories: **3912**.
Venue/pairs producing historical strategy samples: **233**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1205 | 1205 | 1205 | 0 |
| coinbase | 867 | 867 | 572 | 298 |
| bitstamp | 236 | 234 | 234 | 0 |
| okx | 1040 | 1039 | 1039 | 0 |
| kucoin | 864 | 862 | 862 | 0 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 410 | 29 | 130 | -2.66553% |
| cost_aware_momentum | 98 | 16 | 17 | -2.97935% |
| breakout | 463 | 29 | 148 | -2.41591% |
| dip_recovery | 99 | 12 | 46 | -2.15957% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
