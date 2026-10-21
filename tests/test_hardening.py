"""Runtime regressions for the audit-hardening acceptance contract."""
import contextlib
import http.client
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from unittest.mock import patch

import server
import mcp_server
from scripts.generate_dashboard import generate_dashboard
from scripts.incumbent_recon import generate_recon_report
from scripts.generate_pitch_deck import generate_pitch_deck
from scripts.stress_test_simulator import generate_adversarial_brief

ROOT = Path(__file__).resolve().parents[1]


class HTTPHardening(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), server.SocraticRequestHandler)
        self.httpd.output_directory = Path(self.tmp.name)
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        self.port = self.httpd.server_port

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=3)
        self.tmp.cleanup()

    def request(self, method, path, body=None, headers=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=3)
        try:
            conn.request(method, path, body=body, headers=headers or {})
            response = conn.getresponse()
            return response.status, dict(response.getheaders()), response.read()
        finally:
            conn.close()

    def post(self, path, value, headers=None):
        return self.request("POST", path, json.dumps(value),
                            {"Content-Type": "application/json", **(headers or {})})

    def test_private_routes(self):
        for path in ("/.git/config", "/server.py", "/README.md", "/",
                     "/ui/../.git/config", "/%2e%2e/.git/config"):
            if path == "/":
                continue
            with self.subTest(path=path):
                self.assertEqual(self.request("GET", path)[0], 404)

    def test_no_directory_listing_or_head_disclosure(self):
        for path in ("/ui/", "/.git/", "/server.py"):
            with self.subTest(path=path):
                self.assertEqual(self.request("HEAD", path)[0], 404)

    def test_origin_host(self):
        for headers in ({"Origin": "https://evil.example"},
                        {"Origin": "null"},
                        {"Origin": f"http://localhost:{self.port + 1}"},
                        {"Host": "evil.example"},
                        {"Sec-Fetch-Site": "cross-site"}):
            with self.subTest(headers=headers):
                self.assertEqual(self.post("/api/export", {}, headers)[0], 403)
                self.assertEqual(list(Path(self.tmp.name).iterdir()), [])

    def test_request_recovery(self):
        for body in ("[1]", "null", "true", "{", '"hello"', '{"phase":NaN}'):
            with self.subTest(body=body):
                result = self.request("POST", "/api/chat", body,
                                      {"Content-Type": "application/json"})
                self.assertIn(result[0], (400, 422))
                self.assertIn("error", json.loads(result[2]))
                self.assertEqual(self.request("GET", "/api/status")[0], 200)

    def test_size_and_content_type(self):
        self.assertEqual(self.request("POST", "/api/chat", "x" * 65537,
                                      {"Content-Type": "application/json"})[0], 413)
        self.assertEqual(self.request("POST", "/api/chat", "{}",
                                      {"Content-Type": "text/plain"})[0], 415)
        self.assertEqual(self.request("POST", "/api/chat", "{}",
                                      {"Content-Type": "application/json",
                                       "Content-Length": "oops"})[0], 400)

    def test_nested_json_recovery(self):
        nested = '{"message":' + '[' * 2000 + '0' + ']' * 2000 + '}'
        self.assertEqual(self.request("POST", "/api/chat", nested,
                                     {"Content-Type": "application/json"})[0], 400)
        self.assertEqual(self.request("GET", "/api/status")[0], 200)

    def test_field_validation(self):
        for value in ({"message": []}, {"message": "hello", "phase": -1},
                      {"message": "hello", "phase": True},
                      {"message": "hello", "context": []},
                      {"message": "hello", "context": {"phases": []}}):
            with self.subTest(value=value):
                self.assertEqual(self.post("/api/chat", value)[0], 400)
        self.assertEqual(self.post("/api/stress-test", {"mode": "bad"})[0], 400)
        self.assertEqual(self.post("/api/simulate", {"scores": [101] * 8})[0], 400)

    def test_chat_is_intake_and_retains_context(self):
        result = json.loads(self.post("/api/chat", {"message": "A founder tool", "phase": 0})[2])
        self.assertIsNone(result["confidence"])
        self.assertEqual(result["phase"], 1)
        result = json.loads(self.post("/api/chat", {
            "message": "blah " * 40, "phase": 1, "context": result["context"]
        })[2])
        self.assertEqual(result["assessment"]["status"], "REVIEW_REQUIRED")
        self.assertEqual(result["context"]["phases"]["1"], "blah " * 40)
        self.assertNotIn("de-risked", result["reply"].lower())

    def test_export_is_downloadable(self):
        status, headers, body = self.post("/api/export", {})
        self.assertEqual(status, 200)
        result = json.loads(body)
        self.assertEqual(self.request("GET", result["csv"])[0], 200)
        self.assertNotIn("Access-Control-Allow-Origin", headers)
        self.assertEqual(self.request("GET", "/artifacts/../server.py")[0], 404)

    def test_voice_fallback_and_origin(self):
        status, _, body = self.post("/api/tts", {"text": "hello", "apiKey": ""})
        self.assertEqual(status, 400)
        self.assertTrue(json.loads(body)["fallback"])
        with patch("server.urllib.request.urlopen") as provider:
            self.assertEqual(self.post("/api/tts", {"text": "hello", "apiKey": "fixture"},
                                       {"Origin": "https://evil.example"})[0], 403)
            provider.assert_not_called()

    def test_voice_mock_forwarding_and_failure(self):
        with patch("server.urllib.request.urlopen", return_value=io.BytesIO(b"fixture-audio")) as provider:
            status, headers, body = self.post("/api/tts", {
                "provider": "openai", "apiKey": "fixture-key", "text": "hello", "voice": "nova"})
            self.assertEqual((status, headers["Content-Type"], body), (200, "audio/mpeg", b"fixture-audio"))
            self.assertEqual(provider.call_args.args[0].full_url, "https://api.openai.com/v1/audio/speech")
        with patch("server.urllib.request.urlopen", side_effect=OSError("provider unavailable")):
            status, _, body = self.post("/api/tts", {
                "provider": "elevenlabs", "apiKey": "fixture", "text": "hello"})
            self.assertEqual(status, 502)
            self.assertTrue(json.loads(body)["fallback"])

    def test_transcription_bounds_and_fixed_target(self):
        self.assertEqual(self.request("POST", "/api/stt", b"x",
                                     {"Content-Length": str(5242881), "x-api-key": "fixture"})[0], 413)
        with patch("server.urllib.request.urlopen", return_value=io.BytesIO(b'{"text":"fixture transcript"}')) as provider:
            status, _, body = self.request("POST", "/api/stt", b"fixture multipart",
                {"Content-Type": "multipart/form-data; boundary=fixture", "x-api-key": "fixture", "x-provider": "groq"})
            self.assertEqual(status, 200)
            self.assertEqual(json.loads(body)["text"], "fixture transcript")
            self.assertEqual(provider.call_args.args[0].full_url, "https://api.groq.com/openai/v1/audio/transcriptions")
        with patch("server.urllib.request.urlopen") as provider:
            status, _, _ = self.request("POST", "/api/stt", b"fixture",
                {"Content-Type": "multipart/form-data; boundary=fixture", "x-api-key": "fixture", "x-provider": "evil"})
            self.assertEqual(status, 400)
            provider.assert_not_called()


class OutputIntegrity(unittest.TestCase):
    def test_answer_integrity(self):
        result = json.loads(mcp_server.handle_tool_call("gtm_socratic_evaluate", {
            "phase": 1, "founder_answer": "blah " * 40
        }))
        self.assertEqual(result["status"], "REVIEW_REQUIRED")
        self.assertIsNone(result["confidence_score"])
        self.assertIn("guidance", result)

    def test_html_injection(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "radar.html"
            payload = '</script><img src=x onerror="window.injected=1">'
            generate_dashboard(payload, [0] * 8, [payload] * 8, path)
            html = path.read_text(encoding="utf-8")
            self.assertNotIn(payload, html)
            self.assertNotIn("const s = VECTOR_SCORES[i] ||", html)
            self.assertNotIn("${note}</td>", html)

    def test_score_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            for scores in ([0] * 7, [101] * 8, [-1] * 8, [True] * 8, ["85"] * 8):
                with self.subTest(scores=scores):
                    with self.assertRaises(ValueError):
                        generate_dashboard("Test", scores, ["note"] * 8, Path(tmp) / "bad.html")

    def test_recon_provenance_failure(self):
        with patch("scripts.incumbent_recon.urllib.request.urlopen",
                   side_effect=OSError("network unavailable")):
            report = generate_recon_report("Example", "tools")
        self.assertIn("UNAVAILABLE", report)
        self.assertNotIn("Verified Competitive Signals", report)
        self.assertIn("UTC", report)

    def test_recon_provenance_source(self):
        response = io.BytesIO(b'<a class="result__a" href="https://example.com/release">Release</a>'
                              b'<a class="result__snippet">A product update.</a>')
        with patch("scripts.incumbent_recon.urllib.request.urlopen", return_value=response):
            report = generate_recon_report("Example", "tools")
        self.assertIn("https://example.com/release", report)
        self.assertIn("UNVERIFIED", report)
        self.assertIn("UTC", report)

    def test_claim_integrity(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "deck.md"
            generate_pitch_deck("Test", path)
            deck = path.read_text(encoding="utf-8")
            self.assertNotIn("78%+", deck)
            self.assertNotIn("80% organic", deck)
            self.assertIn("EVIDENCE REQUIRED", deck)
        brief = generate_adversarial_brief("ciso", "Test")
        self.assertNotIn("SOC2 Type II report available", brief)
        self.assertIn("EVIDENCE REQUIRED", brief)
        with self.assertRaises(ValueError):
            generate_adversarial_brief("invalid", "Test")


class MCPHardening(unittest.TestCase):
    def exchange(self, messages):
        proc = subprocess.run([sys.executable, str(ROOT / "cli.py"), "mcp"],
                              input="\n".join(json.dumps(m) for m in messages) + "\n",
                              capture_output=True, text=True, encoding="utf-8", timeout=10)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return [json.loads(line) for line in proc.stdout.splitlines() if line.strip()]

    def test_mcp_recovery(self):
        responses = self.exchange([
            {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": []},
            {"jsonrpc": "2.0", "id": 2, "method": "ping"},
            {"jsonrpc": "2.0", "method": "ping"},
            {"jsonrpc": "2.0", "method": "tools/list"},
        ])
        self.assertEqual(len(responses), 2)
        self.assertEqual(responses[0]["error"]["code"], -32602)
        self.assertEqual(responses[1]["result"], {})

    def test_bad_envelopes(self):
        responses = self.exchange([
            {"id": 1, "method": "ping"},
            {"jsonrpc": "1.0", "id": 2, "method": "ping"},
            {"jsonrpc": "2.0", "id": True, "method": "ping"},
            {"jsonrpc": "2.0", "id": 4, "method": []},
            {"jsonrpc": "2.0", "id": 5, "method": "ping"},
        ])
        self.assertEqual([r["error"]["code"] for r in responses[:4]], [-32600] * 4)
        self.assertEqual(responses[4]["result"], {})

    def test_tool_arguments(self):
        for args in ({"phase": 99, "founder_answer": "hello"},
                     {"phase": 1, "founder_answer": []}, {}):
            with self.subTest(args=args):
                responses = self.exchange([{
                    "jsonrpc": "2.0", "id": 1, "method": "tools/call",
                    "params": {"name": "gtm_socratic_evaluate", "arguments": args}
                }])
                self.assertTrue(responses[0]["result"]["isError"])

    def test_notification_does_not_execute_tool(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "deck.md"
            responses = self.exchange([{
                "jsonrpc": "2.0", "method": "tools/call",
                "params": {"name": "gtm_generate_pitch_deck",
                           "arguments": {"startup_name": "Test", "output_path": str(target)}}
            }])
            self.assertEqual(responses, [])
            self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
