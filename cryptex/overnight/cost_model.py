"""Single assumed execution-cost source for all CRYPTEX PAPER strategies.

These are *hypothetical* spot trading assumptions, not an exchange fee quote.
The returned net rate always pays entry fee+slippage AND exit fee+slippage.
"""
from __future__ import annotations
import math
FEE = .0015
SLIP = .0025
STRESS_FEE = .0025
STRESS_SLIP = .005

def buy_factor(fee=FEE, slip=SLIP):
    validate(fee,slip)
    return (1+slip)*(1+fee)

def sell_factor(fee=FEE, slip=SLIP):
    validate(fee,slip)
    return (1-slip)*(1-fee)

def validate(fee,slip):
    if not all(isinstance(v,(int,float)) and math.isfinite(v) and 0<=v<1 for v in (fee,slip)):
        raise ValueError("Invalid hypothetical execution cost")

def break_even(fee=FEE, slip=SLIP):
    return buy_factor(fee,slip)/sell_factor(fee,slip)-1

def returns(entry_mid,exit_mid,fee=FEE,slip=SLIP):
    if not all(isinstance(v,(int,float)) and math.isfinite(v) and v>0 for v in (entry_mid,exit_mid)):
        raise ValueError("Missing or invalid completed-candle mid-price")
    gross=exit_mid/entry_mid-1
    slip_only=exit_mid*(1-slip)/(entry_mid*(1+slip))-1
    net=exit_mid*sell_factor(fee,slip)/(entry_mid*buy_factor(fee,slip))-1
    return {"gross":gross,"net":net,"slippage_drag":gross-slip_only,
            "fee_drag":slip_only-net,"total_drag":gross-net}

def cost_assumptions():
    return {"base":{"fee_per_side":FEE,"slippage_per_side":SLIP,
                      "round_trip_break_even_pct":round(100*break_even(),5)},
            "stress":{"fee_per_side":STRESS_FEE,"slippage_per_side":STRESS_SLIP,
                        "round_trip_break_even_pct":round(100*break_even(STRESS_FEE,STRESS_SLIP),5)},
            "caveat":"Assumptions, not exchange fill receipts. All exits include hypothetical costs; exchange tiers, market impact, spreads and outages can make results worse."}
