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
    # Exit decisions require a fresh, finite close, not today's new-entry
    # turnover/volume screen. A liquidity dip must never veto a protective
    # paper exit from an already-held position.
    if not isinstance(x,dict) or type(x.get("price")) not in (int,float):
        return None
    price=x["price"]
    if not math.isfinite(price) or price<=0:
        return None
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

# Stop loss-making pilot versions opening more PAPER entries after enough
# genuinely completed V4 trades. Never change, delete or backfill old fills.
LOSS_GUARD_MIN_CLOSES = 20
LOSS_GUARD_MAX_WINS = 2
LOSS_GUARD_MAX_MEAN_NET_PCT = -1.0


def after_cost_loss_guard(parent_id, wallet, trades):
    """Return an auditable PAPER entry pause for persistently losing pilots.

    Only closed, version-matched pilot V1 fills with recorded net P&L qualify.
    The passive BTC benchmark remains untouched. Existing positions and exits
    must always be processed by the caller, even while new buys are paused.
    This is a downside control, not a profitable-strategy claim.
    """
    if parent_id not in (7, 8) or not isinstance(wallet, dict):
        return None
    stored = wallet.get("pilot_loss_pause")
    if isinstance(stored, dict) and stored.get("version") == VERSION:
        return stored
    rows = []
    for trade in trades:
        if (not isinstance(trade, dict) or trade.get("bot") != wallet.get("name")
                or trade.get("side") != "SELL"
                or trade.get("pilot_version") != VERSION
                or trade.get("entry_cost_gate_version") != 4):
            continue
        net = trade.get("net_return_pct")
        if type(net) not in (int, float) or not math.isfinite(net):
            continue
        try:
            ts = int(trade["ts"])
        except (KeyError, ValueError, TypeError):
            continue
        rows.append((ts, float(net)))
    rows.sort(key=lambda row: row[0])
    if len(rows) < LOSS_GUARD_MIN_CLOSES:
        return None
    recent = rows[-LOSS_GUARD_MIN_CLOSES:]
    wins = sum(net > 0 for _, net in recent)
    mean_net_pct = sum(net for _, net in recent) / len(recent)
    if wins > LOSS_GUARD_MAX_WINS or mean_net_pct > LOSS_GUARD_MAX_MEAN_NET_PCT:
        return None
    return {"version": VERSION, "sample_size": len(recent),
            "wins_after_cost": wins, "mean_net_return_pct": round(mean_net_pct, 5),
            "reason": "PILOT V1: repeated after-cost losses; future PAPER buys paused",
            "paper_only": True}
