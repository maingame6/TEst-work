# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-10-31T23:48:03.823806+00:00; scanning cycles: 9.
Discovered: 4221 distinct venue/pair listings.
Selected in scan batches: **2974**.
Checked against exchange metadata: **2974**.
Real 5m OHLCV requests attempted: **2974**.
Validated recent closed-candle histories: **2406**.
Venue/pairs producing historical strategy samples: **152**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1201 | 685 | 678 | 7 |
| coinbase | 867 | 685 | 266 | 419 |
| bitstamp | 234 | 234 | 234 | 0 |
| okx | 1040 | 685 | 685 | 0 |
| kucoin | 879 | 685 | 543 | 142 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 230 | 13 | 81 | -2.39635% |
| cost_aware_momentum | 51 | 8 | 8 | -2.49840% |
| breakout | 275 | 12 | 98 | -2.20504% |
| dip_recovery | 55 | 8 | 25 | -1.63414% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
