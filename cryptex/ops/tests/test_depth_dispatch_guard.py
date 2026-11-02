import datetime as dt,pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from depth_dispatch_guard import decide
UTC=dt.timezone.utc
NOW=dt.datetime(2026,11,2,10,10,tzinfo=UTC)
def authority():
 return {"schema":1,"mode":"PAPER_ONLY","writer":"github","pending_writer":None,
         "approved_server_droplet_id":"610231290",
         "protected_csgorisky_droplet_id":"612199466"}
def report(age=18):
 return {"mode":"PAPER_ONLY","real_orders":False,
         "no_paper_portfolio_mutation":True,"markets_targeted":15,
         "generated_at":(NOW-dt.timedelta(minutes=age)).isoformat(),
         "venues":{v:{} for v in ("kraken","coinbase","bitstamp","okx","kucoin")}}
def job(age=12,status="completed",conclusion="success"):
 return {"created_at":(NOW-dt.timedelta(minutes=age)).isoformat(),
         "status":status,"conclusion":conclusion}
class DepthDispatchGuardTests(unittest.TestCase):
 def test_due_at_thirteen_minutes(self):
  ok,reason=decide(authority(),report(age=13),[job(age=20)],NOW)
  self.assertTrue(ok,reason)
 def test_recent_fresh_report_is_not_recollected(self):
  self.assertFalse(decide(authority(),report(age=12),[job(age=20)],NOW)[0])
 def test_recent_or_ongoing_collector_prevents_duplicate(self):
  self.assertFalse(decide(authority(),report(age=40),[job(age=4)],NOW)[0])
  self.assertFalse(decide(authority(),report(age=40),[job(age=35,status="in_progress")],NOW)[0])
  self.assertFalse(decide(authority(),report(age=40),[job(age=45,status="queued")],NOW)[0])
 def test_unknown_run_time_fails_closed(self):
  self.assertFalse(decide(authority(),report(),[{"created_at":"BAD"}],NOW)[0])
  self.assertFalse(decide(authority(),report(),None,NOW)[0])
 def test_wrong_writer_or_csgorisky_machine_refuses_dispatch(self):
  auth=authority();auth["writer"]="server"
  self.assertFalse(decide(auth,report(),[],NOW)[0])
  auth=authority();auth["pending_writer"]="server"
  self.assertFalse(decide(auth,report(),[],NOW)[0])
  auth=authority();auth["protected_csgorisky_droplet_id"]="610231290"
  self.assertFalse(decide(auth,report(),[],NOW)[0])
 def test_wrong_market_report_or_real_order_flag_refuses(self):
  rep=report();rep["real_orders"]=True
  self.assertFalse(decide(authority(),rep,[],NOW)[0])
  rep=report();rep["markets_targeted"]=14
  self.assertFalse(decide(authority(),rep,[],NOW)[0])
  rep=report();rep["venues"]={"kraken":{}}
  self.assertFalse(decide(authority(),rep,[],NOW)[0])
 def test_future_timestamp_does_not_start_a_job(self):
  rep=report(-10)
  self.assertFalse(decide(authority(),rep,[],NOW)[0])
 def test_after_pilot_deadline_refuses(self):
  after=dt.datetime(2026,11,16,0,tzinfo=UTC)
  self.assertFalse(decide(authority(),report(10000),[],after)[0])
 def test_recent_collector_status_cannot_be_success_claim(self):
  # A failed collector remains an actual failure, but a very recent attempt
  # must not immediately be spammed by every 5-minute core run.
  self.assertFalse(decide(authority(),report(50),[job(age=3,conclusion="failure")],NOW)[0])
if __name__=="__main__":unittest.main()
