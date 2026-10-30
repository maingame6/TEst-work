# CRYPTEX Overnight — persistent autonomous PAPER-trading research desk

**No real funds. No exchange API key. No live execution code. No guaranteed returns.**

This is a safe, independent upgrade of the 27 October 2026 CRYPTEX 10-agent lab. It leaves the original `cryptex/index.html` browser simulator unchanged. It runs autonomous **paper** decisions continuously on a computer/server with the engine process running; being saved to GitHub does **not** mean it is running.

## Start it (24/7 on an always-on computer or VPS)

Requires Python 3.10+ (stdlib only); computer with outbound HTTPS. The dashboard is **local-only** by default:

```sh
python3 engine.py serve
# Open http://127.0.0.1:8765 on the same computer.
```

To run a single data/paper cycle:

```sh
python3 engine.py once
```

To run via Docker (recommended for unattended 24/7 with automatic restarts), from this directory:

```sh
docker compose up -d --build
docker compose logs -f --tail=100
# dashboard: http://127.0.0.1:8765 on hosting machine
```

For a remote private VPS dashboard, SSH tunnel `ssh -L 8765:127.0.0.1:8765 user@your-vps`, then open localhost:8765. Never open the raw API to the public Internet without separate authentication/TLS; there is no login in this prototype.

The SQLite database is persisted to `/data` in Docker, or `data/cryptex.sqlite3` locally; restarts do not reset the $100 accounts. Back up that database while the server is stopped, or use SQLite online backup semantics.

## Actual source policy (not just 'lots of data')

- **Kraken public 5-minute OHLCV** (open, high, low, close, real volume, trade counts, VWAP) for up to 12 tickers, where the requested USD pairs exist. The current/uncommitted candle is ignored. 45+ historical committed candles needed before a signal. Last close must be fresh. All fills are simulated at the NEXT committed candle after a decision — no look-ahead same-bar fills. Kraken retains at most 720 recent OHLC intervals; this is a short-term signal, not a comprehensive backtest.
- **CoinGecko public spot reference**, queried on a separate 15-min cadence, crosschecks prices; >5% mismatch vetoes individual coins. If this independent feed fails, the primary Kraken feed is still marked as the only available source. No fake fallback prices.
- **DexScreener Solana boosted-token radar**, 15-minute research view; paid promotion is NOT quality. Missing verifiable mint-authority, LP lock, top-10-holder <=20%, >=$50k hourly volume, no prior developer rug and score >=0.60 => token NOT eligible for execution. This prototype has no trustworthy automated source for every gate, so it deliberately DOES NOT TRADE discovered DEX tokens. The trading universe is listed Kraken-quoted pairs only.
- Metadata from external sources can be late, stale, missing, unavailable, out of sync, or inaccurate. All failures must appear in the log. No self-generated missing values are represented as authentic.

## Strategy lab — ten paper wallets

Ten $10 paper budgets (aggregate $100): GAMBLER (trend), HOUSE (range/grid proxy), SPY (volume only, not actual wallet following), MEME HUNTER (listed-asset momentum), BREAKOUT (Donchian), CONTRARIAN (RSI), ROTATOR (relative strength), VORTEX (flow analogy only), FRACTAL (time scales/entropy), SHOCKWAVE (untested lead/lag correlations). **All trades require valid measured quotes**, are fully journaled, and are simulated, not real trades.

Original strict-risk policy carried forward: **maximum 8% of aggregate paper equity per order**, no averaging down, no leverage, one position per trader, 6% stop *trigger*, trailing starts only after 12% gain; daily equity loss 5% or peak drawdown 15% disables new orders until manually reviewed. Stops are checked only at bar closes, and filled on the following bar — this can be worse than the nominal 6% in a crash. Simulated cost is 0.15% fee per side and 0.25% conservative slippage/spread per side; these are adjustable in source, are not venue guarantees, and may grossly underestimate illiquid meme execution.

## 'Gets smarter' — constrained adaptation, not AI magic

After at least 20 closed **real-quote paper** trades, each bot re-evaluates the last 40 realized net returns and shrinks future allocations when its sample expectancy or confidence is weak. This is cautious, bounded online adaptation. It does not widen stops, disable checks, turn on real-money trades or 'learn' from synthetic market price histories. There is no claim of positive risk-adjusted edge, neural network retraining, or genuine machine intelligence in this version. For more sophisticated ML, use a rigorously timestamped dataset and walk-forward out-of-sample tests with purging/embargo before any promotion to a live executor.

## Diagnostics

```sh
python3 -m unittest discover -s tests -v
python3 engine.py state
```

On feed outage, new trades are blocked. If running unattended, also configure an external uptime alarm and alert on `DEGRADED` for more than 10 minutes. The current prototype cannot prevent losses while offline or guarantee fast exit after a gap. Funding with real money or adding exchange keys requires a different, separately reviewed executor with least-privilege API scopes, no withdrawal permissions, vault storage, idempotent orders, exchange reconciliation, kill switch, audit and regulatory checks. Do **not** paste keys into the public repo, browser local storage, this chat, or a GitHub Pages page.