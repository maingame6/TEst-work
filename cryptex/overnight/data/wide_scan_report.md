# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-11-07T00:54:08.179862+00:00; scanning cycles: 53.
Discovered: 4209 distinct venue/pair listings.
Selected in scan batches: **4207**.
Checked against exchange metadata: **4207**.
Real 5m OHLCV requests attempted: **4207**.
Validated recent closed-candle histories: **3894**.
Venue/pairs producing historical strategy samples: **232**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1205 | 1205 | 1203 | 2 |
| coinbase | 867 | 865 | 554 | 311 |
| bitstamp | 236 | 236 | 236 | 0 |
| okx | 1039 | 1039 | 1039 | 0 |
| kucoin | 862 | 862 | 862 | 0 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 397 | 29 | 131 | -2.69050% |
| cost_aware_momentum | 97 | 16 | 16 | -3.00621% |
| breakout | 418 | 29 | 138 | -2.44098% |
| dip_recovery | 102 | 12 | 44 | -2.16531% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
