# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-11-18T04:14:43.028917+00:00; scanning cycles: 115.
Discovered: 4238 distinct venue/pair listings.
Selected in scan batches: **4238**.
Checked against exchange metadata: **4238**.
Real 5m OHLCV requests attempted: **4238**.
Validated recent closed-candle histories: **4017**.
Venue/pairs producing historical strategy samples: **239**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1209 | 1209 | 1209 | 0 |
| coinbase | 861 | 861 | 640 | 222 |
| bitstamp | 237 | 237 | 237 | 0 |
| okx | 1066 | 1066 | 1066 | 0 |
| kucoin | 865 | 865 | 865 | 0 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 452 | 32 | 125 | -2.63451% |
| cost_aware_momentum | 106 | 19 | 16 | -2.72527% |
| breakout | 448 | 31 | 149 | -2.36525% |
| dip_recovery | 120 | 14 | 48 | -2.27551% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
