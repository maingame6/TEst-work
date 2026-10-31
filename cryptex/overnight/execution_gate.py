"""Conservative, prospective PAPER entry screen. Price momentum is not a forecast."""
from __future__ import annotations
import math

FEE = .0015
SLIP = .0025
BUFFER = .002
VERSION = 3
ROUND_TRIP_BREAK_EVEN = ((1 + SLIP) * (1 + FEE)) / ((1 - SLIP) * (1 - FEE)) - 1
MIN_THREE_BAR_MOVE = ROUND_TRIP_BREAK_EVEN + BUFFER
MIN_HOURLY_TURNOVER = 100_000

def main_eligible(x, contrarian=False):
    """Veto weak/illiquid main-book buys; never interfere with sells or stops."""
    keys = ("price", "vol", "ret3", "z", "vr", "hour_volume", "rsi")
    if any(not isinstance(x.get(k), (int, float)) or not math.isfinite(x[k]) for k in keys):
        return False
    if x["price"] <= 0 or x["hour_volume"] < MIN_HOURLY_TURNOVER:
        return False
    if x["vr"] < 1.25 or x["vol"] > .04:
        return False
    if contrarian:
        return x["ret3"] <= -MIN_THREE_BAR_MOVE and x["z"] <= -1.25 and x["rsi"] < 40
    return x["ret3"] >= MIN_THREE_BAR_MOVE and 45 < x["rsi"] < 80

def research_eligible(x):
    """Conservative long-only filter on research model's completed-bar features."""
    keys = ("last", "r3", "vol", "volume", "hour_turnover")
    if any(not isinstance(x.get(k), (int, float)) or not math.isfinite(x[k]) for k in keys):
        return False
    return (x["last"] > 0
            and x["hour_turnover"] >= MIN_HOURLY_TURNOVER
            and x["volume"] >= 1.25 and x["vol"] <= .04
            and x["r3"] >= math.log1p(MIN_THREE_BAR_MOVE))

def next_candle_only(order, current_ts):
    """A stale queued buy must never fill at a newly observed candle hours later."""
    try:
        signal_ts = int(order["signal_ts"])
    except (ValueError, TypeError, KeyError):
        return False
    return (order.get("cost_gate_version") == VERSION
            and current_ts - signal_ts == 300)
