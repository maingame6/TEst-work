# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-10-31T23:37:20.483536+00:00; scanning cycles: 4.
Discovered: 4221 distinct venue/pair listings.
Selected in scan batches: **1274**.
Checked against exchange metadata: **1274**.
Real 5m OHLCV requests attempted: **1274**.
Validated recent closed-candle histories: **1052**.
Venue/pairs producing historical strategy samples: **50**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1201 | 260 | 257 | 3 |
| coinbase | 867 | 260 | 95 | 165 |
| bitstamp | 234 | 234 | 234 | 0 |
| okx | 1040 | 260 | 260 | 0 |
| kucoin | 879 | 260 | 206 | 54 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 48 | 0 | 22 | -2.49813% |
| cost_aware_momentum | 11 | 0 | 4 | -3.89728% |
| breakout | 70 | 1 | 28 | -2.09275% |
| dip_recovery | 20 | 5 | 11 | -0.65873% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
