import datetime as dt
import unittest
from factor_dispatch_guard import decide, END
UTC=dt.timezone.utc
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
    def test_expiry_blocks_at_25_nov(self):
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

if __name__=='__main__':unittest.main()
