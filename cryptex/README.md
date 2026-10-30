# CRYPTEX — 10-agent Autonomous Trading Lab (test)

This is the original CRYPTEX_10_TRADERS.html prototype tested on 27 October 2026, copied unchanged into `index.html` for browser preview.

## Run
Open `cryptex/index.html` using a static web server (or the raw.githack preview URL for this branch).

- **SIM ENGINE**: seeded, synthetic market simulation; runs fully in the browser.
- **LIVE QUOTES**: requests public CoinGecko and DexScreener data, when available, but orders remain **paper-only**. Public endpoints can be rate-limited or fail due to CORS. These are not live executable orders.
- Ten $10 simulated accounts, strategy research, trade journal/CSV export, market modes.
- State may be persisted in local browser storage. Reset clears local simulation data.

## Safety and limitations
This is a research demo and not an investment service. No real funds, API secrets, exchange accounts, or wallet private keys are included. It makes no real trades. The `LIVE QUOTES` label does **not** mean live-money trading. Trading results in simulated markets do not predict real-world profitability.

## Source/release discipline
This is a separate branch; it does not replace MainGame Codes, Risky, or their production infrastructure. Keep future tests and changes separate from production deployments.
