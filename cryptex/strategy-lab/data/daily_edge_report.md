# CRYPTEX daily swing hypothesis screen

Historical paper backtest only. NO REAL ORDERS or automatic strategy selection.

Generated: 2026-11-17T21:20:26.837294+00:00
Locked registry SHA256: 523b26683da6f2f98cf9580c1234e0bc14232c243ac47444819e49712cb0e0fa
Verified common daily Kraken candles: 720
Original $210 ledger: UNTOUCHED.

## Results: simulated next-day fills including 0.8% taker fee and 0.25% slippage PER SIDE

| Candidate | 2025 net % | 2026 held-out net % | 2026 stress % | 2026 BTC hold % | Exits in 2026 |
|---|---:|---:|---:|---:|---:|
| BTC_TREND_90 | +5.86 | -23.43 | -24.19 | -27.47 | 1 |
| BTC_MOM_30 | -7.48 | -0.21 | -1.69 | -27.47 | 3 |
| ROTATE3_30 | +45.15 | +0.60 | -2.37 | -27.47 | 6 |
| ROTATE3_90 | +11.80 | -37.21 | -39.06 | -27.47 | 5 |
| ROTATE6_60 | -12.34 | -34.26 | -37.78 | -27.47 | 11 |
| ROTATE6_120 | +25.44 | -39.55 | -41.63 | -27.47 | 6 |
| ROTATE3_60_BUFFER | +40.95 | -33.85 | -35.48 | -27.47 | 5 |

**Promotion:** ALL BLOCKED, historical result is not repeated forward performance.

Only genuinely completed UTC daily Kraken OHLC candles. Signals look backwards; fills start on the next daily opening print. No parameter tuning on held-out year. Any apparent winner must survive forward observations, fee stress and matched benchmark plus statistical scrutiny.
The 2026 period has been inspected; it cannot be treated as untouched for any subsequent new strategy search.
