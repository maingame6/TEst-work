# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-11-15T16:44:05.870523+00:00; scanning cycles: 99.
Discovered: 4233 distinct venue/pair listings.
Selected in scan batches: **4233**.
Checked against exchange metadata: **4233**.
Real 5m OHLCV requests attempted: **4233**.
Validated recent closed-candle histories: **3996**.
Venue/pairs producing historical strategy samples: **237**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1206 | 1206 | 1206 | 0 |
| coinbase | 865 | 865 | 628 | 240 |
| bitstamp | 237 | 237 | 237 | 0 |
| okx | 1060 | 1060 | 1060 | 0 |
| kucoin | 865 | 865 | 865 | 0 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 416 | 35 | 135 | -2.64648% |
| cost_aware_momentum | 103 | 17 | 16 | -2.89040% |
| breakout | 438 | 35 | 141 | -2.37581% |
| dip_recovery | 111 | 12 | 50 | -2.21224% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
