# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-10-31T23:45:52.538622+00:00; scanning cycles: 8.
Discovered: 4221 distinct venue/pair listings.
Selected in scan batches: **2634**.
Checked against exchange metadata: **2634**.
Real 5m OHLCV requests attempted: **2634**.
Validated recent closed-candle histories: **2129**.
Venue/pairs producing historical strategy samples: **129**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1201 | 600 | 593 | 7 |
| coinbase | 867 | 600 | 228 | 372 |
| bitstamp | 234 | 234 | 234 | 0 |
| okx | 1040 | 600 | 600 | 0 |
| kucoin | 879 | 600 | 474 | 126 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 194 | 12 | 67 | -2.26295% |
| cost_aware_momentum | 45 | 7 | 8 | -2.33630% |
| breakout | 242 | 11 | 85 | -2.12599% |
| dip_recovery | 44 | 8 | 21 | -1.13252% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
