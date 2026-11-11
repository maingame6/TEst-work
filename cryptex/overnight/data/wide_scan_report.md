# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-11-11T23:28:53.548365+00:00; scanning cycles: 78.
Discovered: 4221 distinct venue/pair listings.
Selected in scan batches: **4221**.
Checked against exchange metadata: **4221**.
Real 5m OHLCV requests attempted: **4221**.
Validated recent closed-candle histories: **3946**.
Venue/pairs producing historical strategy samples: **234**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1205 | 1205 | 1205 | 0 |
| coinbase | 863 | 863 | 588 | 278 |
| bitstamp | 236 | 236 | 236 | 0 |
| okx | 1052 | 1052 | 1052 | 0 |
| kucoin | 865 | 865 | 865 | 0 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 422 | 29 | 137 | -2.67626% |
| cost_aware_momentum | 100 | 16 | 20 | -2.93399% |
| breakout | 447 | 30 | 154 | -2.39252% |
| dip_recovery | 98 | 12 | 44 | -2.23377% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
