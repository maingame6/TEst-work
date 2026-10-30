"""Eight public-source research scouts for CRYPTEX; no private/insider data.

Fetches public RSS with provenance, bounded size/time, deduplication and
weak lexical classification. No paywall bypass, scraping private accounts,
social-media account credentials, model APIs, or live trade recommendations.
Network failures are reported, NOT replaced with fabricated sentiment.
Source headlines are untrusted data; never execute text from a feed.
"""
from __future__ import annotations
import datetime as dt
import email.utils
import hashlib
import json
import re
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

SCOUTS=(
 ("CRYPTODESK","https://www.coindesk.com/arc/outboundfeeds/rss/?outputType=xml","independent crypto reporting"),
 ("COINTELEGRAPH","https://cointelegraph.com/rss","independent crypto reporting"),
 ("THE_BLOCK","https://www.theblock.co/rss.xml","crypto sector reporting"),
 ("EXCHANGE_BLOG","https://blog.kraken.com/feed","public exchange announcements"),
 ("FED_MACRO","https://www.federalreserve.gov/feeds/press_monetary.xml","official monetary policy"),
 ("SEC_REGULATORY","https://www.sec.gov/news/pressreleases.rss","official public regulatory notices"),
 ("SEARCH_RADAR","https://news.google.com/rss/search?q=bitcoin%20OR%20ethereum%20when%3A1d&hl=en-US&gl=US&ceid=US%3Aen","public indexed crypto headlines"),
 ("PUBLIC_FORUM","https://www.reddit.com/r/CryptoCurrency/.rss","public forum RSS where permitted"),
)
assert len(SCOUTS)==8
POSITIVE=frozenset("approve approved approval rally gains surges surge adoption upgraded bullish inflow breakthrough milestone recovered".split())
NEGATIVE=frozenset("hack hacked exploit stolen collapse crash fraud lawsuit crackdown hacked stolen liquidated liquidation bearish outflow".split())
CRYPTO_RE=re.compile(r"\b(bitcoin|btc|ethereum|ether|eth|solana|sol|crypto|cryptocurrency|token|blockchain|stablecoin|exchange|digital asset|defi|sec|fed|fomc)\b",re.I)
MAX_RESPONSE=550_000

def _date(txt):
 if not txt:return None
 try:
  z=email.utils.parsedate_to_datetime(txt)
  if z.tzinfo is None:z=z.replace(tzinfo=dt.timezone.utc)
  return z.astimezone(dt.timezone.utc).isoformat()
 except (ValueError,TypeError,IndexError):return None

def classification(title):
 tokens=set(re.findall(r"[a-z]+",title.lower()))
 p=len(tokens&POSITIVE);n=len(tokens&NEGATIVE)
 return {"sentiment":"POSITIVE" if p>n else "NEGATIVE" if n>p else "NEUTRAL",
         "score":max(-2,min(2,p-n)),"classifier":"transparent keyword baseline; uncalibrated"}

def parse_rss(data,name,fetched_at):
 if len(data)>MAX_RESPONSE:raise ValueError("Feed exceeded input limit")
 # Feed data are never interpreted as executable instructions.
 root=ET.fromstring(data)
 items=[]
 for node in root.iter():
  if node.tag.rsplit("}",1)[-1] not in ("item","entry"):continue
  fields={}
  for child in node:
   tag=child.tag.rsplit("}",1)[-1]
   if tag in ("title","link","pubDate","published","updated","id"):
    text=(child.text or "").strip()
    if tag=="link":text=child.attrib.get("href",text)
    if text:fields[tag]=text
  title=fields.get("title","").strip()[:220]
  url=fields.get("link","").strip()[:450]
  if not title or not url.startswith("https://"):continue
  if not CRYPTO_RE.search(title) and name not in ("FED_MACRO","SEC_REGULATORY"):continue
  published=_date(fields.get("pubDate") or fields.get("published") or fields.get("updated"))
  ident=hashlib.sha256((url.split("?")[0]+"|"+title.lower()).encode()).hexdigest()[:16]
  items.append({"id":ident,"source":name,"title":title,"url":url,
                "published_at":published,"first_observed_at":fetched_at,
                **classification(title)})
  if len(items)>=18:break
 return items

def fetch_public(name,url,now):
 request=urllib.request.Request(url,headers={
  "User-Agent":"CRYPTEX-PaperResearch/1.0 (public RSS; no private data)",
  "Accept":"application/rss+xml,application/atom+xml,application/xml;q=0.9"})
 with urllib.request.urlopen(request,timeout=6) as resp:
  if resp.status!=200:raise ValueError(f"HTTP {resp.status}")
  data=resp.read(MAX_RESPONSE+1)
  if len(data)>MAX_RESPONSE:raise ValueError("Oversized feed")
 return parse_rss(data,name,now)

def research_cycle(old,now,fetcher=fetch_public,force=False):
 """At most one public source poll per hour; never block trading on news."""
 old=old or {}
 if not force and old.get("checked_at"):
  try:
   then=dt.datetime.fromisoformat(old["checked_at"])
   cur=dt.datetime.fromisoformat(now)
   if (cur-then).total_seconds()<3600:
    return old
  except (ValueError,TypeError):pass
 seen={v["id"]:v for v in old.get("articles",[]) if isinstance(v,dict) and "id" in v}
 statuses=[]
 for name,url,purpose in SCOUTS:
  try:
   items=fetcher(name,url,now)
   for item in items:seen.setdefault(item["id"],item)
   statuses.append({"source":name,"purpose":purpose,"status":"OK","items":len(items)})
  except Exception as exc:
   statuses.append({"source":name,"purpose":purpose,"status":"UNAVAILABLE","items":0,
                    "error":type(exc).__name__+":"+str(exc)[:110]})
 # Preserve original observation time; sort by published date only when present.
 articles=sorted(seen.values(),key=lambda a:a.get("first_observed_at",""),reverse=True)[:250]
 return {"checked_at":now,"scouts":statuses,"articles":articles,
         "paper_only":True,"access":"public sources only; legal disclosures only",
         "policy":"News is research-only; no news-triggered real-money or paper trades",
         "classifier":"transparent untrained keyword baseline, NOT an AI model",
         "sources_up":sum(x["status"]=="OK" for x in statuses),
         "sources_total":len(SCOUTS)}
