import datetime as dt
import unittest
from factor_dispatch_guard import decide, END
UTC=dt.timezone.utc
SYMBOLS=('BTC','ETH','SOL','XRP','ADA','DOGE','LTC','LINK','BCH','DOT','AVAX','XLM')
NOW=dt.datetime(2026,11,17,20,40,tzinfo=UTC)

def authority():
    return {'schema':1,'mode':'PAPER_ONLY','writer':'github','pending_writer':None}

def report(age=120):
    return {'mode':'PAPER_ONLY','real_orders':False,
            'independent_of_210_paper_wallets':True,'writer_access':False,
            'candidate_count':84,
            'generated_at':(NOW-dt.timedelta(minutes=age)).isoformat()}

def run(age=120,status='completed'):
    return {'created_at':(NOW-dt.timedelta(minutes=age)).isoformat(),
            'status':status,'conclusion':'success'}

class GuardTests(unittest.TestCase):
    def test_stale_and_old_run_is_eligible(self):
        self.assertTrue(decide(authority(),report(),[run()],NOW)[0])
    def test_fresh_report_blocks(self):
        self.assertFalse(decide(authority(),report(30),[],NOW)[0])
    def test_recent_run_prevents_duplicate_dispatch(self):
        self.assertFalse(decide(authority(),report(),[run(10)],NOW)[0])
        self.assertFalse(decide(authority(),report(),[run(200,'in_progress')],NOW)[0])
    def test_bounded_recovery_covers_full_30_day_prospective_sample(self):
        self.assertGreaterEqual((END-dt.datetime(2026,11,18,tzinfo=UTC)).days,30)
        self.assertTrue(decide(authority(),report(),[],dt.datetime(2026,11,25,tzinfo=UTC))[0])
        self.assertFalse(decide(authority(),report(),[],END)[0])
    def test_nonpaper_or_authority_handover_blocks(self):
        a=authority();a['writer']='server'
        self.assertFalse(decide(a,report(),[],NOW)[0])
        r=report();r['real_orders']=True
        self.assertFalse(decide(authority(),r,[],NOW)[0])
    def test_missing_and_future_times_block(self):
        r=report();r['generated_at']='INVALID'
        self.assertFalse(decide(authority(),r,[],NOW)[0])
        self.assertFalse(decide(authority(),report(-10),[],NOW)[0])
        self.assertFalse(decide(authority(),report(),[{'created_at':'INVALID'}],NOW)[0])


    def test_fresh_report_does_not_hide_missing_next_completed_hour(self):
        expected=(int(NOW.timestamp())//3600-1)*3600
        earlier=expected-3600
        r=report(age=20)
        r['symbols']=list(SYMBOLS)
        r['latest_observed_hour_ts_by_symbol']={symbol:earlier for symbol in SYMBOLS}
        allowed,why=decide(authority(),r,[run(40)],NOW)
        self.assertTrue(allowed,why)
        self.assertEqual(why,'LATEST_COMPLETED_HOUR_MISSING')

    def test_current_hourly_markers_skip_duplicate_dispatch(self):
        expected=(int(NOW.timestamp())//3600-1)*3600
        r=report(age=120)
        r['symbols']=list(SYMBOLS)
        r['latest_observed_hour_ts_by_symbol']={symbol:expected for symbol in SYMBOLS}
        self.assertEqual(decide(authority(),r,[run(120)],NOW)[1],
                         'LATEST_HOURLY_CANDLES_ALREADY_ARCHIVED')

    def test_hourly_feed_settle_and_recent_run_are_respected(self):
        expected=(int(NOW.timestamp())//3600-1)*3600
        r=report(age=120)
        r['symbols']=list(SYMBOLS)
        r['latest_observed_hour_ts_by_symbol']={symbol:expected-3600 for symbol in SYMBOLS}
        early=NOW.replace(minute=5)
        self.assertEqual(decide(authority(),r,[run(120)],early)[1],
                         'WAIT_FOR_COMPLETED_KRAKEN_HOUR')
        self.assertEqual(decide(authority(),r,[run(20)],NOW)[1],
                         'RECENT_FACTOR_WORKFLOW_ATTEMPT')

    def test_malformed_or_future_markers_fail_closed(self):
        expected=(int(NOW.timestamp())//3600-1)*3600
        r=report(age=120)
        r['symbols']=list(SYMBOLS)
        r['latest_observed_hour_ts_by_symbol']={symbol:expected-3600 for symbol in SYMBOLS}
        r['latest_observed_hour_ts_by_symbol'].pop('BTC')
        self.assertEqual(decide(authority(),r,[run(120)],NOW)[1],
                         'INVALID_HOURLY_CANDLE_MARKERS')
        r['latest_observed_hour_ts_by_symbol']['BTC']=expected+3600
        self.assertEqual(decide(authority(),r,[run(120)],NOW)[1],
                         'FUTURE_HOURLY_CANDLE_MARKER')

if __name__=='__main__':unittest.main()
