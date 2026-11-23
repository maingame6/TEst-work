# CRYPTEX daily swing hypothesis screen

Historical paper backtest only. NO REAL ORDERS or automatic strategy selection.

Generated: 2026-11-23T08:56:57.641803+00:00
Locked registry SHA256: 523b26683da6f2f98cf9580c1234e0bc14232c243ac47444819e49712cb0e0fa
Verified common daily Kraken candles: 720
Original $210 ledger: UNTOUCHED.

## Results: simulated next-day fills including 0.8% taker fee and 0.25% slippage PER SIDE

| Candidate | 2025 net % | 2026 held-out net % | 2026 stress % | 2026 BTC hold % | Exits in 2026 |
|---|---:|---:|---:|---:|---:|
| BTC_TREND_90 | +4.39 | -25.59 | -26.33 | -31.54 | 2 |
| BTC_MOM_30 | -7.48 | -0.21 | -1.69 | -31.54 | 3 |
| ROTATE3_30 | +51.98 | +0.60 | -2.37 | -31.54 | 6 |
| ROTATE3_90 | +17.06 | -38.98 | -40.78 | -31.54 | 6 |
| ROTATE6_60 | -10.12 | -34.26 | -37.78 | -31.54 | 11 |
| ROTATE6_120 | +23.69 | -39.96 | -42.02 | -31.54 | 7 |
| ROTATE3_60_BUFFER | +44.51 | -33.85 | -35.48 | -31.54 | 5 |

**Promotion:** ALL BLOCKED, historical result is not repeated forward performance.

Only genuinely completed UTC daily Kraken OHLC candles. Signals look backwards; fills start on the next daily opening print. No parameter tuning on held-out year. Any apparent winner must survive forward observations, fee stress and matched benchmark plus statistical scrutiny.
The 2026 period has been inspected; it cannot be treated as untouched for any subsequent new strategy search.
