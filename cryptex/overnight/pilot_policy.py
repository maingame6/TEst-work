"""Frozen PAPER_ONLY forward pilot within existing $210 simulated accounts.

The 10 original + 11 research accounts remain the *only* bankroll. Three
existing original accounts test *distinct*, preregistered entry policies:
- ROTATOR: passive BTC control (immediately buys the first eligible next bar)
- VORTEX: ETH trend / follow-through
- FRACTAL: SOL mean reversion / dip
No claims of edge; trade costs, time-based exits, drawdown and holdout all matter.
Do not backfill signals, alter historic fills, or route to an exchange.
"""
from __future__ import annotations
import math

VERSION = "PILOT_V1_2026_11_02"
COOLDOWN_BARS = 12
# Parent index, market, frozen entry policy, fixed max holding time in 5m candles
PILOTS = {
    6: ("BTC", "BTC_PASSIVE_CONTROL", 3 * 288),
    7: ("ETH", "ETH_TREND_24H", 288),
    8: ("SOL", "SOL_DIP_12H", 144),
}
MIN_HOURLY_TURNOVER = 100_000.0
MAX_FIVE_MIN_VOL = .07
MIN_RELATIVE_VOLUME = .18
STOP = .06
TAKE_PROFIT = .06

def eligible(x):
    """Mandatory closed-candle quality and liquidity requirements.

    No simulated buy may use stale, missing, nonfinite, illiquid or crossed
    prices. The caller also verifies the price freshness and next-candle fill.
    """
    keys = ("price", "fast", "slow", "ret8", "ret21", "rsi", "z",
            "vol", "vr", "hour_volume")
    if not isinstance(x, dict) or any(
            type(x.get(k)) not in (int, float) or
            not math.isfinite(x[k]) for k in keys):
        return False
    return (x["price"] > 0 and x["fast"] > 0 and x["slow"] > 0
            and x["hour_volume"] >= MIN_HOURLY_TURNOVER
            and 0 <= x["vol"] <= MAX_FIVE_MIN_VOL
            and x["vr"] >= MIN_RELATIVE_VOLUME
            and 0 <= x["rsi"] <= 100)

def idea(parent_id, features, wallet, candle_ts):
    """Decision on observed closed candle, filled next actual closed candle.

    A control intentionally holds market exposure regardless of momentum:
    that is the comparison, *not* a profit prediction or a validated alpha.
    """
    spec = PILOTS.get(parent_id)
    if spec is None or not isinstance(wallet, dict):
        return None
    symbol, policy, hold_bars = spec
    x = features.get(symbol)
    if not eligible(x) or wallet.get("position") or wallet.get("pending"):
        return None
    last_exit = int(wallet.get("pilot_last_exit_ts") or 0)
    if last_exit and candle_ts - last_exit < 300 * COOLDOWN_BARS:
        return None
    if policy == "ETH_TREND_24H":
        if not (x["fast"] >= x["slow"] and x["ret8"] > 0 and x["rsi"] < 76):
            return None
    elif policy == "SOL_DIP_12H":
        if not (x["z"] <= 0 and x["rsi"] < 62 and x["ret21"] > -.06):
            return None
    return {"symbol": symbol, "score": float(x["ret8"]),
            "reason": f"PAPER {VERSION}: {policy}; forward-only entry, not proven profitable",
            "exploratory": False, "cost_gate_version": 4,
            "pilot_policy": policy, "pilot_version": VERSION,
            "pilot_hold_bars": hold_bars}

def queued_eligible(parent_id, order, quote):
    spec=PILOTS.get(parent_id)
    return bool(spec and order.get("pilot_version")==VERSION
                and order.get("pilot_policy")==spec[1]
                and order.get("symbol")==spec[0] and eligible(quote))

def exit_reason(position, features, candle_ts):
    """Only pilot-labelled holdings use these fixed exits.

    Existing legacy positions keep their original exit rules; no positions
    are rewritten or retrospectively attributed to the pilot.
    """
    policy=position.get("pilot_policy")
    if not policy:
        return None
    symbol=position["symbol"]
    x=features.get(symbol)
    if not eligible(x):
        return None  # Caller must preserve the held position on data loss.
    price=x["price"]
    gain=price/float(position["entry_mid"])-1.
    if gain <= -STOP:
        return "PILOT V1 observed 6% stop; next-candle simulated exit"
    bars=max(0,(candle_ts-int(position["entry_ts"]))//300)
    if policy=="ETH_TREND_24H" and x["fast"]<x["slow"] and bars>=12:
        return "PILOT V1 trend turned down; next-candle simulated exit"
    if policy=="SOL_DIP_12H" and gain>=TAKE_PROFIT:
        return "PILOT V1 dip reached 6% gross price rise; next-candle simulated exit"
    if bars>=int(position.get("pilot_hold_bars") or 288):
        return "PILOT V1 fixed holding window reached; next-candle simulated exit"
    return None
