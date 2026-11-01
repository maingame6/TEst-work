"""Offline public market sampling contracts; no exchange or VPS calls."""
import csv,datetime as dt,json,pathlib,sys,tempfile,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
import market_depth_pilot as P
NOW=1793530200000
STAMP="2026-11-01T11:00:00+00:00"
def book():
    return {"bids":[[99.0,25],[98.0,30]],
            "asks":[[100.0,25],[101.0,30]],"timestamp":NOW-4500}
def candle(t,close=100.0):
    return [t,close,close+1,close-1,close,100]
class Dummy:
    has={"fetchOrderBook":True,"fetchOHLCV":True}
    def __init__(self):
        self.markets={"BTC/USDT":{"spot":True,"active":True}}
    def fetch_order_book(self,symbol,limit):
        return book()
    def fetch_ohlcv(self,symbol,timeframe,limit):
        return [candle(NOW-600000),candle(NOW-300000),candle(NOW)] # last is incomplete
class MarketDataTests(unittest.TestCase):
    def test_only_five_named_venues_and_15_public_spot_pairs(self):
        self.assertEqual(len(P.WATCH),5)
        self.assertEqual(sum(map(len,P.WATCH.values())),15)
        self.assertTrue(all(x.count("/")==1 for syms in P.WATCH.values() for x in syms))
    def test_bid_ask_and_depth_have_correct_price_units(self):
        r=P.parse_book(book(),NOW,.008)
        self.assertEqual(r["status"],"OBSERVED_DIAGNOSTIC")
        self.assertGreater(r["spread_bps"],0)
        self.assertGreater(r["bid_depth_1pct_quote"],1000)
        self.assertGreater(r["ask_depth_1pct_quote"],1000)
        self.assertLess(r["same_snapshot_roundtrip_net_pct"],0)
        self.assertLess(r["buy_vwap_1000_quote"],101)
    def test_stale_exchange_timestamp_cannot_pass(self):
        b=book();b["timestamp"]=NOW-300000
        with self.assertRaisesRegex(ValueError,"STALE"):
            P.parse_book(b,NOW,.008)
    def test_missing_orderbook_timestamp_is_explicit(self):
        b=book();b["timestamp"]=None
        r=P.parse_book(b,NOW,.008)
        self.assertIsNone(r["exchange_book_age_seconds"])
    def test_out_of_order_levels_and_empty_levels_do_not_fabricate_depth(self):
        b=book();b["bids"]=[]
        with self.assertRaises(ValueError):P.parse_book(b,NOW,.008)
        b=book();b["asks"]=[[100,1],[101,1]]
        r=P.parse_book(b,NOW,.008)
        self.assertEqual(r["status"],"INSUFFICIENT_BOOK_DEPTH")
        self.assertIsNone(r["same_snapshot_roundtrip_net_pct"])
    def test_crossed_books_fail(self):
        b=book();b["bids"]=[[110,5]]
        with self.assertRaises(ValueError):P.parse_book(b,NOW,.008)
    def test_incomplete_and_corrupt_five_minute_candles_discarded(self):
        raw=[candle(NOW-600000),candle(NOW-300000),candle(NOW),
             [NOW-1000000,-1,2,0,1,2]]
        out=P.extract_candles(raw,NOW,"kraken","BTC/USD",STAMP)
        self.assertEqual(len(out),2)
        self.assertTrue(all(r["historical_not_execution"] for r in out))
        self.assertTrue(all(r["acquired_after_close"] for r in out))
        self.assertEqual(out[-1]["acquisition_delay_seconds"],0)
    def test_independent_orderbook_and_candle_failures(self):
        d=Dummy()
        row,bars=P.gather_market(d,"okx","BTC/USDT",NOW,STAMP)
        self.assertEqual(row["status"],"OBSERVED_DIAGNOSTIC")
        self.assertEqual(len(bars),2)
        self.assertEqual(row["closed_candles_in_payload"],2)
    def test_exchange_book_time_is_measured_after_network_response(self):
        d=Dummy()
        moments=iter([NOW+9000,NOW+11000])
        row,bars=P.gather_market(d,"okx","BTC/USDT",NOW,STAMP,
                                 clock_ms=lambda:next(moments))
        self.assertAlmostEqual(row["exchange_book_age_seconds"],13.5,places=2)
        self.assertEqual(row["observed_at"],
            dt.datetime.fromtimestamp((NOW+9000)/1000,dt.timezone.utc).isoformat())
        self.assertEqual(bars[-1]["acquired_at"],
            dt.datetime.fromtimestamp((NOW+11000)/1000,dt.timezone.utc).isoformat())
        self.assertEqual(bars[-1]["acquisition_delay_seconds"],11)
    def test_inactive_market_not_transformed_into_trade(self):
        d=Dummy();d.markets["BTC/USDT"]["active"]=False
        row,bars=P.gather_market(d,"okx","BTC/USDT",NOW,STAMP)
        self.assertEqual(row["reason"],"INACTIVE_OR_NOT_SPOT")
        self.assertEqual(bars,[])
    def test_csv_dedupes_historical_bars_and_caps_records(self):
        with tempfile.TemporaryDirectory() as folder:
            p=pathlib.Path(folder)/"candles.csv"
            a={"venue":"okx","symbol":"BTC/USDT","candle_start_ms":123}
            n=P.merge_rows(p,[a],P.CANDLE_HEADERS,
                           ("venue","symbol","candle_start_ms"),max_rows=20)
            self.assertEqual(n,1)
            n=P.merge_rows(p,[a],P.CANDLE_HEADERS,
                           ("venue","symbol","candle_start_ms"),max_rows=20)
            self.assertEqual(n,1)
            with p.open() as f:self.assertEqual(len(list(csv.DictReader(f))),1)
    def test_readonly_report_does_not_claim_profit(self):
        result=P.report([{"venue":"kraken","symbol":"BTC/USD",
                         "status":"OBSERVED_DIAGNOSTIC"}],[],STAMP)
        self.assertFalse(result["real_orders"])
        self.assertTrue(result["no_paper_portfolio_mutation"])
        self.assertIn("NOT a fill",result["interpretation"])
    def test_fee_is_not_claimed_as_our_tier(self):
        self.assertEqual(len(P.FEE_ASSUMED),5)
        for value in P.FEE_ASSUMED.values():
            self.assertGreater(value,0)
            self.assertLess(value,.1)

if __name__=="__main__":unittest.main()
