# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-11-19T03:20:49.758309+00:00; scanning cycles: 118.
Discovered: 4247 distinct venue/pair listings.
Selected in scan batches: **4247**.
Checked against exchange metadata: **4247**.
Real 5m OHLCV requests attempted: **4247**.
Validated recent closed-candle histories: **4030**.
Venue/pairs producing historical strategy samples: **240**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1209 | 1209 | 1209 | 0 |
| coinbase | 861 | 861 | 644 | 218 |
| bitstamp | 237 | 237 | 237 | 0 |
| okx | 1070 | 1070 | 1070 | 0 |
| kucoin | 870 | 870 | 870 | 0 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 418 | 32 | 136 | -2.62689% |
| cost_aware_momentum | 106 | 19 | 16 | -2.72746% |
| breakout | 422 | 31 | 137 | -2.40640% |
| dip_recovery | 151 | 17 | 73 | -2.07842% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
