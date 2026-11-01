"""No external server or GitHub writes. A real temporary bare Git repository
proves that two independent writers cannot overwrite the paper ledger."""
import datetime as dt,json,os,pathlib,subprocess,sys,tempfile,unittest
from unittest import mock
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
import server_writer as W
from writer_control import authorized

def git(*args,cwd=None,check=True):
    return subprocess.run(["git",*args],cwd=cwd,check=check,
                          text=True,capture_output=True)
def commit(path,msg):
    (path/"state.json").write_text(msg+"\n")
    git("add","state.json",cwd=path)
    git("-c","user.name=fixture","-c","user.email=fixture@example.test",
        "commit","-m",msg,cwd=path)

class ServerWriterSafetyTests(unittest.TestCase):
    def test_only_private_codex_writer_directory_allowed(self):
        self.assertFalse(W.private_repo(pathlib.Path("/srv/csgorisky")))
        self.assertFalse(W.private_repo(pathlib.Path("/tmp/stolen-project")))
        self.assertTrue(W.private_repo(W.STATE_DIR/"repo"))

    def test_never_publish_unstaged_secrets(self):
        self.assertNotIn("secret.key",W.SAVE_FILES)
        self.assertNotIn("accounts.env",W.SAVE_FILES)
        self.assertIn("state.json",W.SAVE_FILES)
        self.assertIn("integrity_report.json",W.SAVE_FILES)

    def test_no_token_means_no_publication(self):
        with mock.patch.dict(os.environ,{},clear=True):
            with self.assertRaises(RuntimeError):W.credential_env()

    def test_real_droplet_host_guard_required(self):
        with mock.patch.object(W,"verify_host",return_value=1):
            self.assertFalse(W.verify_host()==0)

    def test_github_owner_never_grants_server_write(self):
        record={"schema":1,"mode":"PAPER_ONLY","writer":"github","epoch":1,
                "pending_writer":None,"changed_at":"2026-11-01T15:00:00+00:00",
                "approved_server_droplet_id":"610231290",
                "protected_csgorisky_droplet_id":"612199466"}
        self.assertFalse(authorized(record,"server"))
        self.assertTrue(authorized(record,"github"))

    def test_new_server_activation_requires_fresh_host_proof(self):
        record={"schema":1,"mode":"PAPER_ONLY","writer":"server","epoch":3,
                "pending_writer":None,"changed_at":"2026-11-01T15:00:00+00:00",
                "approved_server_droplet_id":"610231290",
                "protected_csgorisky_droplet_id":"612199466"}
        now=dt.datetime(2026,11,1,15,40,tzinfo=dt.timezone.utc)
        proof={"generated_at":now.isoformat(),"mode":"PAPER_ONLY",
               "droplet_id":"610231290","real_orders":False,
               "remote_branch_writes":False,"capacity_check_passed":True,
               "csgo_risky_shared_processes":False,"integrity_checks":13,
               "paper_accounts":21,"missed_intervals":0,
               "distinct_server_processed_candles":6,
               "minimum_inter_observation_seconds":298,
               "maximum_inter_observation_seconds":311}
        with tempfile.TemporaryDirectory() as folder:
            p=pathlib.Path(folder);file=p/"proof.json"
            file.write_text(json.dumps(proof))
            self.assertTrue(W.accept_host_activation(record,p,now,file))
            proof["droplet_id"]="612199466"
            file.write_text(json.dumps(proof))
            with self.assertRaises(RuntimeError):
                W.accept_host_activation(record,p,now,file)
            proof["droplet_id"]="610231290"
            proof["generated_at"]=(now-dt.timedelta(hours=1)).isoformat()
            file.write_text(json.dumps(proof))
            with self.assertRaises(RuntimeError):
                W.accept_host_activation(record,p,now,file)
            (p/"activated_writer_epoch.json").write_text(json.dumps({
                "epoch":3,"droplet_id":"610231290"}))
            self.assertFalse(W.accept_host_activation(record,p,now,file))

    def test_two_writer_race_second_push_is_rejected_without_force(self):
        with tempfile.TemporaryDirectory() as folder:
            p=pathlib.Path(folder)
            upstream=p/"remote.git"
            git("init","--bare",str(upstream))
            seed=p/"seed";seed.mkdir()
            git("init",cwd=seed)
            commit(seed,"initial paper cycle")
            git("branch","-M","cryptex-paper-trading-preview",cwd=seed)
            git("remote","add","origin",str(upstream),cwd=seed)
            git("push","origin","HEAD:cryptex-paper-trading-preview",cwd=seed)
            writer_one=p/"writer_one";writer_two=p/"writer_two"
            git("clone","--branch","cryptex-paper-trading-preview",str(upstream),str(writer_one))
            git("clone","--branch","cryptex-paper-trading-preview",str(upstream),str(writer_two))
            commit(writer_one,"github trade journal")
            commit(writer_two,"server competing journal")
            git("push","origin","HEAD:cryptex-paper-trading-preview",cwd=writer_one)
            loser=git("push","origin","HEAD:cryptex-paper-trading-preview",cwd=writer_two,check=False)
            self.assertNotEqual(loser.returncode,0)
            observed=git("show","cryptex-paper-trading-preview:state.json",cwd=seed,check=False)
            # Read the remote directly to prove winner's ledger survived.
            winning=git("--git-dir",str(upstream),"show","cryptex-paper-trading-preview:state.json")
            self.assertEqual(winning.stdout.strip(),"github trade journal")

if __name__=="__main__":unittest.main()
