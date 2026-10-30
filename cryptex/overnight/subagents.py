"""CRYPTEX: 640 deterministic paper-research subagent reviews.

Ten parent strategies, each with sixty parameterised factor-voters and four
hard-gate analysts: 64 transparent observations per valid closed candle.
These are NOT 640 neural networks or separately trained language models.
They share the same validated market data. Their vote correlations matter.
No token swaps, live exchange integrations, leverage, secrets or real orders.
"""
from __future__ import annotations
import math

FACTOR_NAMES = (
    "TREND_SPREAD", "TREND_STATE", "RETURN_5M", "RETURN_10M", "RETURN_15M",
    "RETURN_40M", "RETURN_50M", "RETURN_105M", "MOMENTUM_ACCELERATION",
    "BREAKOUT_DISTANCE", "RSI_POSITION", "ZSCORE_DISTANCE",
    "VOLATILITY_REGIME", "RELATIVE_VOLUME", "PRICE_ENTROPY",
)
SENSITIVITY = (("FAST", .045), ("BALANCED", .12), ("SELECTIVE", .23), ("STRICT", .39))
GUARDS = ("DATA_QUALITY", "USD_TURNOVER", "VOLATILITY_LIMIT", "FLOW_LIMIT")
ROLES = tuple(f"{factor}_{level}" for factor in FACTOR_NAMES for level,_ in SENSITIVITY) + GUARDS
assert len(ROLES) == len(set(ROLES)) == 64
REVERSION_PARENTS = frozenset((1, 5))
COST_ROUND_TRIP = 2 * (.0015 + .0025)

REQUIRED = (
    "price", "fast", "slow", "one", "ret2", "ret3", "ret8", "ret10",
    "ret21", "rsi", "z", "vol", "vr", "priorhigh", "entropy", "hour_volume",
)

def _clip(v):
    if not math.isfinite(float(v)):
        return 0.
    return max(-1.,min(1.,float(v)))

def _vote(role, decision, score, reason):
    return {"role":role,"vote":decision,
            "indicator_score":round(_clip(score),4),"reason":reason}

def _safedata(x):
    return bool(isinstance(x,dict) and all(
        type(x.get(k)) in (float,int) and math.isfinite(float(x[k]))
        for k in REQUIRED
    ) and x["price"]>0 and x["slow"]>0 and x["priorhigh"]>0
    and x["hour_volume"]>=0 and x["vol"]>=0 and x["vr"]>=0)

def _factors(x, parent):
    reverse= -1 if parent in REVERSION_PARENTS else 1
    d = lambda v: _clip(reverse*v)
    trend=(x["fast"]/x["slow"]-1)
    series=(
        d(trend*50),
        d((1 if trend>0 else -1)*.50+(x["ret8"]*8)),
        d(x["one"]*80),
        d(x["ret2"]*62),
        d(x["ret3"]*48),
        d(x["ret8"]*26),
        d(x["ret10"]*23),
        d(x["ret21"]*14),
        d((x["ret3"]/3.-x["ret8"]/8.)*220),
        d((x["price"]/x["priorhigh"]-1)*75),
        d((x["rsi"]-50.)/22.),
        d(x["z"]*.60),
        _clip((.028-x["vol"])/.028),
        _clip((x["vr"]-1.)*.50),
        _clip((.93-x["entropy"])*3),
    )
    assert len(series)==len(FACTOR_NAMES)
    return series

def _empty(symbol,stage,proposed,position,note):
    votes=[_vote(role, "VETO" if role in GUARDS else "HOLD",
                 -1 if role in GUARDS else 0,note) for role in ROLES]
    return {
        "symbol":symbol,"stage":stage,"votes":votes,
        "result":"MISSING_DATA" if position else "VETO",
        "note":note,"parent_signal":bool(proposed),
        "exploratory":bool(proposed and proposed.get("exploratory")),
        "support":0,"opposition":0,"neutral":60,"veto_count":4,
        "factor_score":0,
    }

def subagent_team(parent_id,features,proposed=None,position=None,watch_symbol=None):
    """64 votes: 15 factor families × four thresholds, plus 4 hard gates.

    Teams provide diagnoses and a conditional buy gate, not fake profit forecasts.
    A parent still decides if/what to buy; vetoes prevent new paper entries.
    Existing position exits/stops always outrank specialist votes.
    """
    if parent_id not in range(10):
        raise ValueError("Unknown parent strategy")
    symbol=(position.get("symbol") if position else
            proposed.get("symbol") if proposed else watch_symbol)
    stage="POSITION" if position else "ENTRY"
    x=features.get(symbol) if symbol else None
    if not _safedata(x):
        return _empty(symbol,stage,proposed,position,
                      "Missing or invalid closed-candle indicator input")
    factor_values=_factors(x,parent_id)
    votes=[]
    for factor, score in zip(FACTOR_NAMES, factor_values):
        for level,threshold in SENSITIVITY:
            decision=("BUY" if score>=threshold else
                      "CAUTION" if score<=-threshold else "HOLD")
            votes.append(_vote(f"{factor}_{level}",decision,score,
                f"{factor} sensitivity {level}; score {score:+.3f}; threshold {threshold:.3f}"))
    guards=(
        (x["price"]>0 and x["slow"]>0 and x["priorhigh"]>0 and math.isfinite(x["price"]),
         f"positive finite close {x['price']:.8g}"),
        (x["hour_volume"]>=60000,
         f"closed-candle hourly turnover USD {x['hour_volume']:.0f} (min 60000)"),
        (x["vol"]<=.07,f"realized volatility {x['vol']:.4f} (max .0700)"),
        (x["vr"]>=.18,f"relative volume {x['vr']:.3f} (min .180)"),
    )
    for role,(passed,detail) in zip(GUARDS,guards):
        votes.append(_vote(role,"PASS" if passed else "VETO",.5 if passed else -1,detail))
    if len(votes)!=64 or any(v["role"]!=r for v,r in zip(votes,ROLES)):
        raise AssertionError("Missing/misordered specialist result")
    vetoes=[v for v in votes if v["vote"]=="VETO"]
    support=sum(v["vote"]=="BUY" for v in votes[:60])
    opposition=sum(v["vote"]=="CAUTION" for v in votes[:60])
    neutral=60-support-opposition
    mean_score=sum(v["indicator_score"] for v in votes[:60])/60.
    if position:
        outcome="POSITION_REVIEW"
        note=f"{support} favourable / {opposition} cautious, 4 hard gates; exit overrides all votes"
    elif vetoes:
        outcome="VETO"
        note="HARD GATE: "+", ".join(v["role"] for v in vetoes)
    elif not proposed:
        outcome="HOLD"
        note=f"No parent entry; specialists {support} favourable, {opposition} cautious"
    else:
        # Intentionally allow exploratory paper tests despite factor disagreement;
        # this captures counterexamples instead of filtering out every loss.
        outcome="BUY"
        note=(f"Parent {'exploratory' if proposed.get('exploratory') else 'strategy'} "
              f"paper signal; {support} favourable, {opposition} cautious, "
              "all 4 mandatory execution guards passed")
    return {
        "symbol":symbol,"stage":stage,"votes":votes,"result":outcome,
        "note":note,"parent_signal":bool(proposed),
        "exploratory":bool(proposed and proposed.get("exploratory")),
        "support":support,"opposition":opposition,"neutral":neutral,
        "veto_count":len(vetoes),"factor_score":round(mean_score,4),
    }

def format_votes(team):
    """Compact complete vote tape: roles are uniquely defined in ROLES."""
    return ";".join(
        f"{v['role']}:{v['vote']}:{v['indicator_score']:+.3f}"
        for v in team["votes"]
    )
