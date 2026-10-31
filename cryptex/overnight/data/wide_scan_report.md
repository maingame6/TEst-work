# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-10-31T23:54:33.840878+00:00; scanning cycles: 12.
Discovered: 4221 distinct venue/pair listings.
Selected in scan batches: **3860**.
Checked against exchange metadata: **3860**.
Real 5m OHLCV requests attempted: **3860**.
Validated recent closed-candle histories: **3161**.
Venue/pairs producing historical strategy samples: **196**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1201 | 940 | 932 | 8 |
| coinbase | 867 | 867 | 355 | 512 |
| bitstamp | 234 | 234 | 234 | 0 |
| okx | 1040 | 940 | 940 | 0 |
| kucoin | 879 | 879 | 700 | 179 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 314 | 19 | 108 | -2.38812% |
| cost_aware_momentum | 66 | 11 | 11 | -2.34937% |
| breakout | 361 | 20 | 123 | -2.24347% |
| dip_recovery | 76 | 9 | 36 | -1.86774% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
