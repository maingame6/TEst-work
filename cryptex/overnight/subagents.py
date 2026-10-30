"""CRYPTEX paper-only subagent review teams.

Deterministic specialist reviewers (NOT independent LLMs); consume already validated
closed-candle indicator features. No exchange keys, trades, API calls or wallets.
The parent trader remains responsible for selecting a strategy signal and the
engine's hard risk gates remain authoritative.
"""
from __future__ import annotations
import math

ROLES = ("SETUP_SCOUT", "MARKET_REGIME", "EXECUTION_RISK")
COST_ROUND_TRIP = 2 * (0.0015 + 0.0025)  # fee + slippage both directions
REVERSION_PARENTS = frozenset((1, 5))


def _vote(role, decision, score, explanation):
    # Score is a bounded indicator preference, NOT a calibrated probability.
    return {"role": role, "vote": decision,
            "indicator_score": round(max(-1., min(1., float(score))), 3),
            "reason": explanation}


def subagent_team(parent_id, features, proposed=None, position=None):
    """Return 3 independently justified votes and a no-bypass parent outcome.

    The market-data pipeline must already have rejected stale/contradictory data.
    We do not invent prices; no signal means HOLD. Hard vetoes cannot be
    overridden by parent strategy or by another subagent.
    """
    if position:
        symbol = position.get("symbol")
        stage = "POSITION"
    else:
        symbol = proposed.get("symbol") if proposed else None
        stage = "ENTRY"
    x = features.get(symbol) if symbol else None
    if x is None:
        label = "No currently valid candle for selected instrument"
        votes = [
            _vote("SETUP_SCOUT", "HOLD", 0, label),
            _vote("MARKET_REGIME", "HOLD", 0, label),
            _vote("EXECUTION_RISK", "VETO", -1, label),
        ]
        return {"symbol": symbol, "stage": stage, "votes": votes,
                "result": "HOLD" if not position else "MISSING_DATA",
                "note": label, "parent_signal": bool(proposed),
                "exploratory": bool(proposed and proposed.get("exploratory"))}
    expected=("price", "ret3", "ret8", "z", "rsi", "vol", "vr", "hour_volume", "fast", "slow")
    valid = all(isinstance(x.get(k), (int, float)) and math.isfinite(x[k]) for k in expected)
    if not valid or x["price"] <= 0:
        votes = [_vote("SETUP_SCOUT", "HOLD", 0, "Nonfinite input"),
                 _vote("MARKET_REGIME", "HOLD", 0, "Nonfinite input"),
                 _vote("EXECUTION_RISK", "VETO", -1, "Invalid candle features")]
        return {"symbol": symbol, "stage": stage, "votes": votes,
                "result": "MISSING_DATA", "note": "Invalid candle features",
                "parent_signal": bool(proposed), "exploratory": bool(proposed and proposed.get("exploratory"))}

    reverse = parent_id in REVERSION_PARENTS
    momentum = float(x["ret3"])
    rsi = float(x["rsi"])
    z = float(x["z"])
    vol = float(x["vol"])
    volume = float(x["hour_volume"])
    flow = float(x["vr"])

    scout_pref = (-momentum if reverse else momentum)
    if reverse:
        scout_buy = z < -.45 or rsi < 48
        setup_reason = f"Mean-reversion hypothesis: z={z:+.2f}, RSI={rsi:.0f}"
    else:
        scout_buy = momentum > -.001 or x["fast"] >= x["slow"]
        setup_reason = f"Trend hypothesis: 15m={momentum:+.2%}, RSI={rsi:.0f}"
    scout = _vote("SETUP_SCOUT", "BUY" if scout_buy else "HOLD",
                  scout_pref * 60, setup_reason)

    benign = vol <= .045 and flow >= .3
    trend_confirm = x["ret8"] >= -.024 if not reverse else z < -.2
    regime_buy = benign and trend_confirm
    regime = _vote("MARKET_REGIME", "BUY" if regime_buy else "HOLD",
                   (1.-vol/.05) * .6 + (flow-1.) * .04,
                   f"Volatility={vol:.3%}; 1h flow={flow:.2f}x; 40m move={x['ret8']:+.2%}")

    # No fake liquidity or missing-data forgiveness. Check spot volume in USD,
    # not illiquid coin amount. Estimated round-trip friction is always shown.
    veto_reason = None
    if volume < 60000:
        veto_reason = f"hourly USD turnover {volume:,.0f} below 60,000"
    elif vol > .07:
        veto_reason = f"five-minute log-return volatility {vol:.2%} > 7%"
    elif flow < .18:
        veto_reason = f"volume ratio {flow:.2f} < 0.18"
    safety = _vote("EXECUTION_RISK", "VETO" if veto_reason else "PASS",
                   -1 if veto_reason else .5,
                   veto_reason or f"Liquidity ${volume:,.0f}/h; estimated round-trip friction {COST_ROUND_TRIP:.2%}")
    votes = [scout, regime, safety]
    supporters = sum(v["vote"] == "BUY" for v in votes)
    if position:
        # The original exit/stop checks happen in the runner. Subagents advise
        # but NEVER veto stops, exits or missing-data safeguards.
        outcome = "POSITION_REVIEW"
        note = f"{supporters}/2 entry-perspective reviewers still favour holding; exit rules remain authoritative"
    elif veto_reason:
        outcome = "VETO"
        note = veto_reason
    elif not proposed:
        outcome = "HOLD"
        note = "Parent proposed no entry"
    else:
        # For exploratory paper tests, log disagreement rather than silencing
        # experiments; preserve the small 1.2% allocation.
        outcome = "BUY"
        note = (f"Parent {('exploratory' if proposed.get('exploratory') else 'strategy')} signal; "
                f"{supporters}/2 nonrisk specialist support; risk gate passed")
    return {"symbol": symbol, "stage": stage, "votes": votes,
            "result": outcome, "note": note,
            "parent_signal": bool(proposed),
            "exploratory": bool(proposed and proposed.get("exploratory"))}


def format_votes(team):
    return "; ".join(f"{v['role']}={v['vote']}: {v['reason']}" for v in team["votes"])