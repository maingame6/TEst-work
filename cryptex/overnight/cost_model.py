"""Single assumed execution-cost source for all CRYPTEX PAPER strategies.

Kraken Pro published Tier 1 spot taker fee 0.80% per fill (confirmed 31 Oct 2026).\nNo claim about account-specific tier. 0.25% per side slippage is conservative\nresearch assumption, not an executable quote. Historical pre-V4 paper fills\nretain their original fee assumptions.\nSource: https://www.kraken.com/pro/fees
The returned net rate always pays entry fee+slippage AND exit fee+slippage.
"""
from __future__ import annotations
import math
FEE = .0080
SLIP = .0025
STRESS_FEE = .0080
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
            "published_fee_source":"https://www.kraken.com/pro/fees",
            "fee_tier":"Kraken Pro spot Tier 1 taker: 0.80% per side",
            "maker_alternative_per_side":.004,
            "caveat":"0.80% published taker fee, estimated 0.25% slippage each side; not account-specific fill receipts. Wider spread, market impact and outages can make results worse. Historical V3 charges were lower and are not silently restated."}
