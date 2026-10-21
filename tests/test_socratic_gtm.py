import unittest
from unittest.mock import patch
import os
import sys
import json
import subprocess
import tempfile
import shutil
from pathlib import Path

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
        with patch("urllib.request.urlopen", side_effect=OSError("offline fixture")):
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

    def test_cli_start_mocked(self):
        """Test the interactive terminal walkthrough via piped stdin."""
        mock_inputs = "\n".join([
            "AuditCo",
            "Daily active usage through automated alerts and peer sharing.",
            "Incumbent has direct Salesforce distribution, but we route around it.",
            "Designed for end-user practitioners to avoid IT CISO friction on Day 1.",
            "Starting horizontal across GitHub workflows before verticalizing.",
            "Proactive cron routines run background scans every night.",
            "Multi-model router across Claude and GPT with CMEK context keys.",
            "Hybrid model charging platform fee plus metered tasks.",
            "Bi-directional webhook sync to Postgres and Salesforce."
        ]) + "\n"

        proc = subprocess.Popen(
            [sys.executable, os.path.join(ROOT_DIR, "cli.py"), "start"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=self.test_dir,
            encoding="utf-8"
        )
        stdout, stderr = proc.communicate(input=mock_inputs, timeout=10)
        self.assertEqual(proc.returncode, 0)
        self.assertIn("Interview intake complete.", stdout)
        playbook = Path(self.test_dir) / "auditco_GTM_PLAYBOOK.md"
        self.assertTrue(playbook.exists())
        content = playbook.read_text(encoding="utf-8")
        for answer in mock_inputs.splitlines()[1:]:
            self.assertIn(answer, content)
        self.assertNotIn("Resilience Score", stdout)
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "auditco_gtm_simulator.html")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "auditco_sprint_issues.csv")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "auditco_GTM_PITCH_DECK.md")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "auditco_adversarial_brief.md")))

    def test_server_api_endpoints(self):
        """Test the local web server REST endpoints including fallback voice behavior."""
        import urllib.request
        import queue
        import re
        import threading

        proc = subprocess.Popen(
            [sys.executable, "-u", os.path.join(ROOT_DIR, "server.py"), "--port", "0", "--no-browser"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            cwd=self.test_dir,
        )
        startup = queue.Queue()
        reader = threading.Thread(target=lambda: startup.put(proc.stderr.readline()), daemon=True)
        reader.start()
        try:
            try:
                line = startup.get(timeout=20)
            except queue.Empty:
                self.fail("Server did not emit its startup URL within 20 seconds")
            match = re.search(r"http://127\.0\.0\.1:(\d+)/ui/index\.html", line)
            self.assertIsNotNone(match, "Server startup failed: " + line)
            port = int(match.group(1))
            # 1. Test /api/status
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/status", timeout=5) as resp:
                self.assertEqual(resp.status, 200)
                data = json.loads(resp.read().decode())
                self.assertEqual(data.get("status"), "online")
                self.assertTrue(data.get("speech_support", {}).get("stt"))

            # 2. Test /api/chat
            req_data = json.dumps({"message": "Building an automated AI agent for sales.", "phase": 0}).encode()
            req = urllib.request.Request(f"http://127.0.0.1:{port}/api/chat", data=req_data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                self.assertEqual(resp.status, 200)
                data = json.loads(resp.read().decode())
                self.assertIn("reply", data)
                self.assertIn("Phase 1", data["reply"])

            # 3. Test /api/tts missing key (triggers fallback response)
            req_data = json.dumps({"text": "Hello world", "provider": "openai", "apiKey": ""}).encode()
            req = urllib.request.Request(f"http://127.0.0.1:{port}/api/tts", data=req_data, headers={"Content-Type": "application/json"})
            try:
                urllib.request.urlopen(req, timeout=5)
            except urllib.error.HTTPError as e:
                self.assertEqual(e.code, 400)
                body = json.loads(e.read().decode())
                self.assertTrue(body.get("fallback"))

            # 4. Test /api/stt missing key (triggers fallback response)
            req_data = b"dummy audio content"
            req = urllib.request.Request(f"http://127.0.0.1:{port}/api/stt", data=req_data, headers={"x-api-key": "", "Content-Type": "audio/webm"})
            try:
                urllib.request.urlopen(req, timeout=5)
            except urllib.error.HTTPError as e:
                self.assertEqual(e.code, 400)
                body = json.loads(e.read().decode())
                self.assertTrue(body.get("fallback"))

        finally:
            proc.terminate()
            try:
                proc.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.communicate(timeout=5)
            reader.join(timeout=1)

if __name__ == "__main__":
    unittest.main()
