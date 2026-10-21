import unittest
import os
import sys
import json
import subprocess
import tempfile
import shutil

# Add root directory to sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

SCRIPTS_DIR = os.path.join(ROOT_DIR, "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from generate_dashboard import generate_dashboard
from incumbent_recon import generate_recon_report
from stress_test_simulator import generate_adversarial_brief
from export_issues import export_issues, DEFAULT_ISSUES
from generate_pitch_deck import generate_pitch_deck

class TestSocraticGTM(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_generate_dashboard(self):
        out = os.path.join(self.test_dir, "test_sim.html")
        scores = [85, 75, 90, 70, 80, 85, 75, 90]
        notes = ["Note " + str(i) for i in range(8)]
        generate_dashboard("TestStartup", scores, notes, out)
        self.assertTrue(os.path.exists(out))
        with open(out, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("TestStartup", content)
        self.assertIn("radarChart", content)
        self.assertIn("AI Startup GTM Simulator", content)

    def test_incumbent_recon(self):
        out = os.path.join(self.test_dir, "test_recon.md")
        report = generate_recon_report("Salesforce", "CRM AI", out)
        self.assertTrue(os.path.exists(out))
        self.assertIn("SALESFORCE", report)
        self.assertIn("Strategic Pressure Points", report)

    def test_stress_test_ciso(self):
        out = os.path.join(self.test_dir, "test_ciso.md")
        brief = generate_adversarial_brief("ciso", "AuditApp", out)
        self.assertTrue(os.path.exists(out))
        self.assertIn("ENTERPRISE CISO", brief)
        self.assertIn("AuditApp", brief)

    def test_stress_test_vc(self):
        out = os.path.join(self.test_dir, "test_vc.md")
        brief = generate_adversarial_brief("vc", "AuditApp", out)
        self.assertTrue(os.path.exists(out))
        self.assertIn("TIER-1 VC PARTNER", brief)
        self.assertIn("AuditApp", brief)

    def test_export_issues(self):
        csv_out = os.path.join(self.test_dir, "test_issues.csv")
        json_out = os.path.join(self.test_dir, "test_issues.json")
        export_issues(DEFAULT_ISSUES, csv_out, json_out)
        self.assertTrue(os.path.exists(csv_out))
        self.assertTrue(os.path.exists(json_out))
        with open(json_out, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(len(data), len(DEFAULT_ISSUES))

    def test_generate_pitch_deck(self):
        out = os.path.join(self.test_dir, "test_deck.md")
        generate_pitch_deck("AuditApp", out)
        self.assertTrue(os.path.exists(out))
        with open(out, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("AUDITAPP: GO-TO-MARKET & MOAT DECK COPY", content)
        self.assertIn("SLIDE 1: THE WEDGE", content)

    def test_mcp_protocol_initialize(self):
        proc = subprocess.Popen(
            [sys.executable, os.path.join(ROOT_DIR, "cli.py"), "mcp"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8"
        )
        req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}) + "\n"
        stdout, _ = proc.communicate(input=req, timeout=5)
        resp = json.loads(stdout.strip())
        self.assertEqual(resp["id"], 1)
        self.assertEqual(resp["result"]["serverInfo"]["name"], "socratic-gtm-strategist")
        self.assertEqual(resp["result"]["serverInfo"]["version"], "3.0.0")

    def test_mcp_tools_list(self):
        proc = subprocess.Popen(
            [sys.executable, os.path.join(ROOT_DIR, "cli.py"), "mcp"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8"
        )
        req = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}) + "\n"
        stdout, _ = proc.communicate(input=req, timeout=5)
        resp = json.loads(stdout.strip())
        self.assertEqual(resp["id"], 2)
        tool_names = [t["name"] for t in resp["result"]["tools"]]
        self.assertIn("gtm_simulate_radar", tool_names)
        self.assertIn("gtm_incumbent_recon", tool_names)
        self.assertIn("gtm_stress_test", tool_names)
        self.assertIn("gtm_export_issues", tool_names)
        self.assertIn("gtm_generate_pitch_deck", tool_names)
        self.assertIn("gtm_socratic_evaluate", tool_names)

    def test_mcp_parse_error(self):
        proc = subprocess.Popen(
            [sys.executable, os.path.join(ROOT_DIR, "cli.py"), "mcp"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8"
        )
        req = "INVALID_JSON_LINE\n"
        stdout, _ = proc.communicate(input=req, timeout=5)
        resp = json.loads(stdout.strip())
        self.assertIsNone(resp["id"])
        self.assertEqual(resp["error"]["code"], -32700)

if __name__ == "__main__":
    unittest.main()
