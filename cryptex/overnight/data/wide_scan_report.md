# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-11-23T21:17:23.299703+00:00; scanning cycles: 133.
Discovered: 4256 distinct venue/pair listings.
Selected in scan batches: **4255**.
Checked against exchange metadata: **4255**.
Real 5m OHLCV requests attempted: **4255**.
Validated recent closed-candle histories: **4059**.
Venue/pairs producing historical strategy samples: **244**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1210 | 1210 | 1210 | 0 |
| coinbase | 855 | 855 | 659 | 197 |
| bitstamp | 237 | 237 | 237 | 0 |
| okx | 1078 | 1078 | 1078 | 0 |
| kucoin | 876 | 875 | 875 | 0 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 422 | 34 | 136 | -2.63071% |
| cost_aware_momentum | 124 | 21 | 32 | -2.50625% |
| breakout | 440 | 33 | 147 | -2.38197% |
| dip_recovery | 110 | 14 | 48 | -2.24744% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
