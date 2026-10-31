"""Experimental mathematical analogies and open-source-inspired shadow agents.

DISCLAIMER: None of these is mathematically derived from OpenAI's proofs.
They are falsifiable hypotheses on real historical closed OHLCV bars, NOT
profitable systems, independent AI models, or exchange execution.

Inspirations: OpenAI 2026 Navier-Stokes and ten math advances;
Qlib (cross-sectional ranks), Freqtrade (multi-indicator thresholds),
Hummingbot (execution friction / spread caution), LEAN (event-driven
one-step-later fills). No third-party source code copied.
"""
from __future__ import annotations
import math
import statistics
from execution_gate import research_eligible

MATH_MODELS=(
 "FLUID_ADVECTION","FLUID_VISCOSITY","GEOMETRIC_DIVERSITY",
 "ERROR_CODE_CONSENSUS","GRAPH_COHERENCE","LATTICE_ANALOG",
)
OPEN_MODELS=("FREQTRADE_STYLE","QLIB_STYLE","HUMMINGBOT_FRICTION","LEAN_EVENT","NAUTILUS_REGIME")
MODEL_NAMES=MATH_MODELS+OPEN_MODELS
assert len(MODEL_NAMES)==11
ROUND_TRIP_COST=2*(.0015+.0025)

def mean(x):return sum(x)/len(x) if x else 0.
def clamp(x,a=-1.,b=1.):return max(a,min(b,x))
def logreturns(b):
 p=[float(c["close"]) for c in b]
 if len(p)<2 or any(not math.isfinite(x) or x<=0 for x in p):
  return []
 return [math.log(y/x) for x,y in zip(p,p[1:])]

def _features(b):
 if len(b)<70:return None
 r=logreturns(b)
 if not r or len(r)<69:return None
 p=[float(c["close"]) for c in b]
 v=[float(c.get("volume",0)) for c in b]
 if any(not math.isfinite(x) or x<0 for x in v):return None
 vmean=mean(v[-22:-1])
 sigma=statistics.pstdev(r[-24:]) or 1e-9
 r3=sum(r[-3:]);r8=sum(r[-8:]);r21=sum(r[-21:])
 flow=v[-1]/vmean if vmean>0 else 0.
 return {"r":r,"p":p,"v":v,"r3":r3,"r8":r8,"r21":r21,
         "vol":sigma,"volume":flow,"last":p[-1],
         "d3":mean(r[-3:])-mean(r[-8:]),"m8":mean(p[-8:]),
         "m21":mean(p[-21:]),"hour_turnover":sum(c["volume"]*c["close"] for c in b[-12:])}

def _correlation(a,b):
 if len(a)<25 or len(b)<25:return 0.
 a=a[-24:];b=b[-24:]
 ma=mean(a);mb=mean(b)
 da=statistics.pstdev(a);db=statistics.pstdev(b)
 return clamp(mean([(x-ma)*(y-mb) for x,y in zip(a,b)])/(da*db)) if da and db else 0.

def _knn_past_only(b):
 """Historical analog forward outcomes use EXCLUSIVELY timestamps before now.

 Last observation i is an observation of old history, outcome i+3 must
 precede most recent sample; no training label can use current/future data.
 """
 r=logreturns(b)
 if len(r)<80:return (0.,0)
 query=[sum(r[-k:]) for k in (2,5,13)]
 pairs=[]
 # An eligible historical pattern ends at j; future r[j:j+3] is still historical.
 for j in range(30,len(r)-12):
  pat=[sum(r[j-k:j]) for k in (2,5,13)]
  dist=sum(((x-y)/max(0.003,abs(y),.01))**2 for x,y in zip(query,pat))
  future=sum(r[j:j+3])
  pairs.append((dist,j,future))
 if len(pairs)<15:return (0.,0)
 nearest=sorted(pairs,key=lambda z:z[0])[:min(9,len(pairs))]
 wins=sum(x[2]>ROUND_TRIP_COST for x in nearest)
 # Historical relative similarity not a proven forecast.
 edge=mean([z[2] for z in nearest])-ROUND_TRIP_COST
 return (clamp(edge/.015),wins)

def evaluate(histories, held_positions=None):
 """Return one ranked idea per model from fresh, aligned completed histories.
 Scores are signed, not probabilities. A model may abstain/hold.
 """
 held_positions=held_positions or {}
 f={s:_features(b) for s,b in histories.items() if b and len(b)>=70}
 f={s:x for s,x in f.items() if x is not None and x["hour_turnover"]>=60000 and x["vol"]<.09 and x["volume"]>=.12}
 if len(f)<3:return {m:{"action":"HOLD","symbol":None,"score":0.,
    "reason":"Insufficient valid/independent crypto candle data","sample_ok":False} for m in MODEL_NAMES}
 market=mean([x["r8"] for x in f.values()])
 graph_count=sum(x["r8"]>0 for x in f.values())
 results={}
 for model in MODEL_NAMES:
  ranking=[]
  for sym,x in f.items():
   shock=x["r"][-1]-x["r"][-2]
   if model=="FLUID_ADVECTION":
    # Toy advection: volume-weighted acceleration of log-price velocity.
    # This is NOT a numerical solution of the Navier-Stokes PDE.
    score=clamp((x["d3"]*.7+shock*.3)*(1+min(2,x["volume"])/3)/.008)
    description="Volume-weighted 5m momentum acceleration (fluid-flow analogy)"
   elif model=="FLUID_VISCOSITY":
    # momentum - a diffusion/noise penalty, motivated by damping.
    score=clamp((x["r8"]/8-x["vol"]*.50)/.004)
    description="Momentum less empirical log-return diffusion/noise"
   elif model=="GEOMETRIC_DIVERSITY":
    # Convert geometric packing intuition into decorrelation, not proof.
    corr=max((abs(_correlation(x["r"],h["r"])) for t,h in f.items()
              if t!=sym and held_positions.get(t)),default=0.)
    score=clamp(x["r8"]/.025-corr*.75)
    description="Cross-asset decorrelation penalty (sphere-packing analogy)"
   elif model=="ERROR_CODE_CONSENSUS":
    scales=(x["r3"],x["r8"],x["r21"])
    agreement=sum(z>0 for z in scales)
    score=clamp((agreement-1.6)/1.4) if abs(x["r8"])>.001 else 0.
    description="Agreement across three return horizons (code redundancy analogy)"
   elif model=="GRAPH_COHERENCE":
    cluster=graph_count/len(f)
    score=clamp((x["r8"]-market)/.016+(.2 if cluster>.6 else -.1))
    description="Relative-strength shock in asset co-movement graph"
   elif model=="LATTICE_ANALOG":
    score,wins=_knn_past_only(histories[sym])
    description=f"Historical nearest-vector analog, {wins}/9 after-cost positives in old samples"
   elif model=="FREQTRADE_STYLE":
    score=clamp(x["r8"]/.017+(x["m8"]/x["m21"]-1)*25-x["vol"]*14)
    description="Own EMA/momentum trend score inspired by Freqtrade strategy testing"
   elif model=="QLIB_STYLE":
    rank=sorted([t["r8"]-t["vol"]*.65 for t in f.values()])
    raw=x["r8"]-x["vol"]*.65
    score=clamp((sum(y<=raw for y in rank)/len(rank)-.5)*1.8)
    description="Cross-sectional factor rank concept inspired by Microsoft Qlib"
   elif model=="LEAN_EVENT":
    # Deterministic, event-driven trend continuation with completed-bar
    # confirmation. Architecture-inspired, NO QuantConnect code imported.
    score=clamp((min(x["r3"],x["r8"])/.012) if x["r3"]>0 and x["r8"]>0 else -.3)
    description="Event-driven completed-candle confirmation (LEAN-inspired)"
   elif model=="NAUTILUS_REGIME":
    # Regime-aware direction with strong shock suppression.
    score=clamp((x["r8"]/.015) if x["vol"]<.024 and x["volume"]>.5 else -.4)
    description="Deterministic volatility regime guard (NautilusTrader-inspired)"
   else:
    # Hummingbot's real market making needs order book and execution; no quotes
    # available => HOLD, but log lack of L2 explicitly.
    results[model]={"action":"HOLD","symbol":None,"score":0.,
        "reason":"No verified L2 order book, bid/ask or queue position: market maker disallowed",
        "sample_ok":False}
    break
   if math.isfinite(score):ranking.append((score,sym,description))
  if model in results:continue
  if not ranking:
   results[model]={"action":"HOLD","symbol":None,"score":0.,"reason":"No eligible asset","sample_ok":False}
   continue
  score,sym,description=max(ranking)
  # Distinct thresholds; investigate failures as well as wins.
  threshold=.09 if model in ("FLUID_ADVECTION","QLIB_STYLE","GRAPH_COHERENCE") else .14
  results[model]={"action":"BUY" if score>threshold and research_eligible(x) else "HOLD",
      "symbol":sym,"score":round(score,5),
      "reason":description+f"; score={score:+.3f}, gate={threshold:.2f}; after-cost candidate screen (not a forecast)",
      "sample_ok":True}
 return results
