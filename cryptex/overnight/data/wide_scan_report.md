# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-10-31T23:39:30.244465+00:00; scanning cycles: 5.
Discovered: 4221 distinct venue/pair listings.
Selected in scan batches: **1614**.
Checked against exchange metadata: **1614**.
Real 5m OHLCV requests attempted: **1614**.
Validated recent closed-candle histories: **1328**.
Venue/pairs producing historical strategy samples: **66**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1201 | 345 | 340 | 5 |
| coinbase | 867 | 345 | 127 | 218 |
| bitstamp | 234 | 234 | 234 | 0 |
| okx | 1040 | 345 | 345 | 0 |
| kucoin | 879 | 345 | 282 | 63 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 64 | 1 | 23 | -2.34949% |
| cost_aware_momentum | 13 | 0 | 4 | -3.52325% |
| breakout | 92 | 2 | 32 | -1.98677% |
| dip_recovery | 21 | 5 | 11 | -0.68720% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
