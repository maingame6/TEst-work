# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-11-14T03:10:33.959641+00:00; scanning cycles: 90.
Discovered: 4233 distinct venue/pair listings.
Selected in scan batches: **4233**.
Checked against exchange metadata: **4233**.
Real 5m OHLCV requests attempted: **4233**.
Validated recent closed-candle histories: **3974**.
Venue/pairs producing historical strategy samples: **236**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1206 | 1206 | 1206 | 0 |
| coinbase | 865 | 865 | 606 | 262 |
| bitstamp | 237 | 237 | 237 | 0 |
| okx | 1060 | 1060 | 1060 | 0 |
| kucoin | 865 | 865 | 865 | 0 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 395 | 29 | 121 | -2.72573% |
| cost_aware_momentum | 96 | 16 | 16 | -3.02420% |
| breakout | 416 | 29 | 135 | -2.44190% |
| dip_recovery | 126 | 12 | 59 | -2.14692% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
