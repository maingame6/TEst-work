# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-10-31T23:43:44.774815+00:00; scanning cycles: 7.
Discovered: 4221 distinct venue/pair listings.
Selected in scan batches: **2294**.
Checked against exchange metadata: **2294**.
Real 5m OHLCV requests attempted: **2294**.
Validated recent closed-candle histories: **1864**.
Venue/pairs producing historical strategy samples: **110**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1201 | 515 | 508 | 7 |
| coinbase | 867 | 515 | 192 | 323 |
| bitstamp | 234 | 234 | 234 | 0 |
| okx | 1040 | 515 | 515 | 0 |
| kucoin | 879 | 515 | 415 | 100 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 159 | 10 | 55 | -2.22061% |
| cost_aware_momentum | 38 | 6 | 8 | -2.55633% |
| breakout | 195 | 9 | 69 | -2.08266% |
| dip_recovery | 36 | 8 | 16 | -0.88677% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
