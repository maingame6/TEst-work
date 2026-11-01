"""Offline PAPER_ONLY writer-gate tests. Zero network, zero GitHub or VPS mutation."""
import copy, datetime as dt, pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from writer_control import authorized,validate,check_transition,independent_proof_valid,SafetyError

NOW=dt.datetime(2026,11,1,15,tzinfo=dt.timezone.utc)
def owner(writer="github",epoch=1,pending=None,time=None):
    return {"schema":1,"mode":"PAPER_ONLY","writer":writer,"epoch":epoch,
            "pending_writer":pending,"changed_at":(time or NOW).isoformat(),
            "approved_server_droplet_id":"610231290",
            "protected_csgorisky_droplet_id":"612199466"}
def proof():
    return {"generated_at":NOW.isoformat(),"droplet_id":"610231290","mode":"PAPER_ONLY","real_orders":False,
            "remote_branch_writes":False,"csgo_risky_shared_processes":False,
            "capacity_check_passed":True,"integrity_checks":13,"paper_accounts":21,
            "missed_intervals":0,"distinct_server_processed_candles":6,
            "minimum_inter_observation_seconds":290,
            "maximum_inter_observation_seconds":315}

class WriterAuthorityTests(unittest.TestCase):
    def test_default_github_owner_only(self):
        self.assertTrue(authorized(owner(),"github"))
        self.assertFalse(authorized(owner(),"server"))
    def test_drain_fences_everyone(self):
        self.assertFalse(authorized(owner("drain",2,"server"),"github"))
        self.assertFalse(authorized(owner("drain",2,"server"),"server"))
    def test_server_owner_fences_github(self):
        self.assertTrue(authorized(owner("server",3),"server"))
        self.assertFalse(authorized(owner("server",3),"github"))
    def test_old_epoch_rejected(self):
        self.assertFalse(authorized(owner("github",4),"github",3))
    def test_unknown_mode_and_invalid_host_rejected(self):
        x=owner();x["mode"]="LIVE"
        with self.assertRaises(SafetyError):validate(x)
        x=owner();x["approved_server_droplet_id"]="612199466"
        with self.assertRaises(SafetyError):validate(x)
    def test_invalid_actor_rejected(self):
        with self.assertRaises(SafetyError):authorized(owner(),"unknown")
    def test_no_direct_switch_without_drain(self):
        with self.assertRaises(SafetyError):
            check_transition(owner(),owner("server",2),NOW,False,proof())
    def test_github_to_drain_permitted(self):
        self.assertTrue(check_transition(owner(),owner("drain",2,"server"),NOW,False,None))
    def test_inflight_competing_jobs_block_takeover(self):
        old=owner("drain",2,"server",NOW-dt.timedelta(minutes=14))
        with self.assertRaises(SafetyError):
            check_transition(old,owner("server",3),NOW,True,proof())
    def test_takeover_requires_full_drain_duration(self):
        old=owner("drain",2,"server",NOW-dt.timedelta(minutes=12))
        with self.assertRaises(SafetyError):
            check_transition(old,owner("server",3),NOW,False,proof())
    def test_takeover_requires_real_server_proof(self):
        old=owner("drain",2,"server",NOW-dt.timedelta(minutes=14))
        with self.assertRaises(SafetyError):
            check_transition(old,owner("server",3),NOW,False,None)
        self.assertTrue(check_transition(old,owner("server",3),NOW,False,proof()))
    def test_wrong_droplet_always_blocked(self):
        p=proof();p["droplet_id"]="612199466"
        self.assertFalse(independent_proof_valid(p))
    def test_missing_or_paper_histories_cannot_fake_server(self):
        for key,bad in (("distinct_server_processed_candles",0),
                        ("missed_intervals",1),("capacity_check_passed",False),
                        ("real_orders",True),("csgo_risky_shared_processes",True),
                        ("maximum_inter_observation_seconds",900)):
            p=proof();p[key]=bad
            self.assertFalse(independent_proof_valid(p),key)
    def test_server_to_drain_then_github_recovery(self):
        self.assertTrue(check_transition(owner("server",3),owner("drain",4,"github"),NOW,False,None))
        old=owner("drain",4,"github",NOW-dt.timedelta(minutes=14))
        self.assertTrue(check_transition(old,owner("github",5),NOW,False,None))
    def test_old_and_future_server_proofs_are_rejected(self):
        old=owner("drain",2,"server",NOW-dt.timedelta(minutes=14))
        evidence=proof()
        evidence["generated_at"]=(NOW-dt.timedelta(hours=4)).isoformat()
        with self.assertRaises(SafetyError):
            check_transition(old,owner("server",3),NOW,False,evidence)
        evidence["generated_at"]=(NOW+dt.timedelta(hours=1)).isoformat()
        with self.assertRaises(SafetyError):
            check_transition(old,owner("server",3),NOW,False,evidence)
    def test_invalid_epoch_or_skipped_epoch_rejected(self):
        with self.assertRaises(SafetyError):
            check_transition(owner(),owner("drain",4,"server"),NOW,False,None)

if __name__=="__main__":unittest.main()
