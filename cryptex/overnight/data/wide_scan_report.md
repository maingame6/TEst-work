# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-11-24T17:36:34.400608+00:00; scanning cycles: 135.
Discovered: 4256 distinct venue/pair listings.
Selected in scan batches: **4256**.
Checked against exchange metadata: **4256**.
Real 5m OHLCV requests attempted: **4256**.
Validated recent closed-candle histories: **4066**.
Venue/pairs producing historical strategy samples: **240**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1210 | 1210 | 1210 | 0 |
| coinbase | 855 | 855 | 665 | 191 |
| bitstamp | 237 | 237 | 237 | 0 |
| okx | 1078 | 1078 | 1078 | 0 |
| kucoin | 876 | 876 | 876 | 0 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 412 | 32 | 121 | -2.66345% |
| cost_aware_momentum | 105 | 19 | 16 | -2.75135% |
| breakout | 420 | 31 | 130 | -2.41267% |
| dip_recovery | 119 | 14 | 47 | -2.31105% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
