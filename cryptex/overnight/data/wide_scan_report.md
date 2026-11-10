# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-11-10T18:29:23.441787+00:00; scanning cycles: 70.
Discovered: 4213 distinct venue/pair listings.
Selected in scan batches: **4213**.
Checked against exchange metadata: **4213**.
Real 5m OHLCV requests attempted: **4213**.
Validated recent closed-candle histories: **3928**.
Venue/pairs producing historical strategy samples: **232**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1205 | 1205 | 1205 | 0 |
| coinbase | 863 | 863 | 578 | 288 |
| bitstamp | 236 | 236 | 236 | 0 |
| okx | 1045 | 1045 | 1045 | 0 |
| kucoin | 864 | 864 | 864 | 0 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 393 | 29 | 127 | -2.70817% |
| cost_aware_momentum | 96 | 16 | 16 | -3.02420% |
| breakout | 406 | 29 | 127 | -2.48484% |
| dip_recovery | 114 | 12 | 58 | -2.10839% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
