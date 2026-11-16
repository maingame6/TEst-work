# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-11-16T20:24:10.426963+00:00; scanning cycles: 106.
Discovered: 4229 distinct venue/pair listings.
Selected in scan batches: **4229**.
Checked against exchange metadata: **4229**.
Real 5m OHLCV requests attempted: **4229**.
Validated recent closed-candle histories: **3997**.
Venue/pairs producing historical strategy samples: **236**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1206 | 1206 | 1206 | 0 |
| coinbase | 861 | 861 | 629 | 234 |
| bitstamp | 237 | 237 | 237 | 0 |
| okx | 1061 | 1061 | 1061 | 0 |
| kucoin | 864 | 864 | 864 | 0 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 429 | 33 | 145 | -2.63445% |
| cost_aware_momentum | 102 | 17 | 16 | -2.99241% |
| breakout | 426 | 35 | 143 | -2.38372% |
| dip_recovery | 107 | 12 | 53 | -2.20005% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
