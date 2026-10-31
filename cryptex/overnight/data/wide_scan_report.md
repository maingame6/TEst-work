# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-10-31T23:50:14.839809+00:00; scanning cycles: 10.
Discovered: 4221 distinct venue/pair listings.
Selected in scan batches: **3314**.
Checked against exchange metadata: **3314**.
Real 5m OHLCV requests attempted: **3314**.
Validated recent closed-candle histories: **2682**.
Venue/pairs producing historical strategy samples: **173**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1201 | 770 | 763 | 7 |
| coinbase | 867 | 770 | 303 | 467 |
| bitstamp | 234 | 234 | 234 | 0 |
| okx | 1040 | 770 | 770 | 0 |
| kucoin | 879 | 770 | 612 | 158 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 259 | 18 | 87 | -2.32041% |
| cost_aware_momentum | 62 | 10 | 11 | -2.38974% |
| breakout | 312 | 17 | 106 | -2.20217% |
| dip_recovery | 60 | 8 | 29 | -1.65491% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
