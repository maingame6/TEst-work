# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-11-03T09:28:33.154513+00:00; scanning cycles: 32.
Discovered: 4223 distinct venue/pair listings.
Selected in scan batches: **4223**.
Checked against exchange metadata: **4223**.
Real 5m OHLCV requests attempted: **4223**.
Validated recent closed-candle histories: **3803**.
Venue/pairs producing historical strategy samples: **223**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1201 | 1201 | 1197 | 4 |
| coinbase | 865 | 865 | 451 | 415 |
| bitstamp | 234 | 234 | 234 | 0 |
| okx | 1039 | 1039 | 1039 | 0 |
| kucoin | 884 | 884 | 882 | 2 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 351 | 25 | 114 | -2.54875% |
| cost_aware_momentum | 80 | 13 | 14 | -2.59767% |
| breakout | 397 | 24 | 134 | -2.36768% |
| dip_recovery | 85 | 11 | 39 | -1.77801% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
