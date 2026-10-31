# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-10-31T23:52:24.363226+00:00; scanning cycles: 11.
Discovered: 4221 distinct venue/pair listings.
Selected in scan batches: **3654**.
Checked against exchange metadata: **3654**.
Real 5m OHLCV requests attempted: **3654**.
Validated recent closed-candle histories: **2965**.
Venue/pairs producing historical strategy samples: **187**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1201 | 855 | 847 | 8 |
| coinbase | 867 | 855 | 349 | 506 |
| bitstamp | 234 | 234 | 234 | 0 |
| okx | 1040 | 855 | 855 | 0 |
| kucoin | 879 | 855 | 680 | 175 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 290 | 18 | 100 | -2.36862% |
| cost_aware_momentum | 62 | 10 | 11 | -2.38974% |
| breakout | 340 | 19 | 116 | -2.23697% |
| dip_recovery | 69 | 8 | 35 | -1.81373% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
