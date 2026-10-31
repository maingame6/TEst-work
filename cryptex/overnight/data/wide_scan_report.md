# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-10-31T23:35:12.154019+00:00; scanning cycles: 3.
Discovered: 4221 distinct venue/pair listings.
Attempted with exchange API: **875**.
Validated recent closed-candle histories: **729**.
Venue/pairs producing historical strategy samples: **38**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1201 | 175 | 174 | 1 |
| coinbase | 867 | 175 | 70 | 105 |
| bitstamp | 234 | 175 | 175 | 0 |
| okx | 1040 | 175 | 175 | 0 |
| kucoin | 879 | 175 | 135 | 40 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 32 | 0 | 17 | -2.10787% |
| cost_aware_momentum | 3 | 0 | 1 | -1.79014% |
| breakout | 58 | 1 | 25 | -2.07035% |
| dip_recovery | 12 | 2 | 6 | -1.08916% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
