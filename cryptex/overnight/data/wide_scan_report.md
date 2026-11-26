# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-11-26T15:07:23.521595+00:00; scanning cycles: 138.
Discovered: 4255 distinct venue/pair listings.
Selected in scan batches: **4255**.
Checked against exchange metadata: **4255**.
Real 5m OHLCV requests attempted: **4255**.
Validated recent closed-candle histories: **4068**.
Venue/pairs producing historical strategy samples: **240**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1210 | 1210 | 1210 | 0 |
| coinbase | 852 | 852 | 665 | 187 |
| bitstamp | 237 | 237 | 237 | 0 |
| okx | 1078 | 1078 | 1078 | 0 |
| kucoin | 878 | 878 | 878 | 0 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 406 | 32 | 125 | -2.77582% |
| cost_aware_momentum | 108 | 19 | 16 | -3.16398% |
| breakout | 429 | 31 | 135 | -2.42679% |
| dip_recovery | 106 | 14 | 44 | -2.44769% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
