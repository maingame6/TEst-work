# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-11-15T21:18:20.535191+00:00; scanning cycles: 100.
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
| momentum_05 | 443 | 29 | 154 | -2.64936% |
| cost_aware_momentum | 102 | 16 | 16 | -2.92839% |
| breakout | 468 | 29 | 153 | -2.39359% |
| dip_recovery | 102 | 12 | 47 | -2.23538% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
