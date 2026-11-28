# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-11-28T18:22:00.473992+00:00; scanning cycles: 147.
Discovered: 4257 distinct venue/pair listings.
Selected in scan batches: **4257**.
Checked against exchange metadata: **4257**.
Real 5m OHLCV requests attempted: **4257**.
Validated recent closed-candle histories: **4076**.
Venue/pairs producing historical strategy samples: **241**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1210 | 1210 | 1210 | 0 |
| coinbase | 852 | 852 | 671 | 182 |
| bitstamp | 237 | 237 | 237 | 0 |
| okx | 1078 | 1078 | 1078 | 0 |
| kucoin | 880 | 880 | 880 | 0 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 398 | 32 | 120 | -2.81233% |
| cost_aware_momentum | 108 | 19 | 16 | -3.16398% |
| breakout | 423 | 31 | 134 | -2.44013% |
| dip_recovery | 108 | 14 | 44 | -2.49248% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
