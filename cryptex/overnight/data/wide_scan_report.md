# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-11-04T21:16:53.203169+00:00; scanning cycles: 40.
Discovered: 4231 distinct venue/pair listings.
Selected in scan batches: **4226**.
Checked against exchange metadata: **4226**.
Real 5m OHLCV requests attempted: **4226**.
Validated recent closed-candle histories: **3844**.
Venue/pairs producing historical strategy samples: **230**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1205 | 1204 | 1201 | 3 |
| coinbase | 865 | 865 | 487 | 378 |
| bitstamp | 236 | 235 | 235 | 0 |
| okx | 1039 | 1037 | 1037 | 0 |
| kucoin | 886 | 885 | 884 | 1 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 386 | 40 | 122 | -2.49122% |
| cost_aware_momentum | 104 | 27 | 16 | -2.40976% |
| breakout | 420 | 41 | 136 | -2.32166% |
| dip_recovery | 94 | 11 | 43 | -1.81359% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
