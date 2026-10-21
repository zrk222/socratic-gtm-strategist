#!/usr/bin/env python3
"""Local-only GTM dashboard and bounded JSON API. No hosted authentication."""
import argparse
import json
from pathlib import Path
import sys
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit
import urllib.request
import re

from scripts.generate_dashboard import generate_dashboard
from scripts.incumbent_recon import generate_recon_report
from scripts.stress_test_simulator import generate_adversarial_brief
from scripts.export_issues import export_issues, DEFAULT_ISSUES
from scripts.generate_pitch_deck import generate_pitch_deck
from socratic_gtm.assessment import PHASES, assess_answer, validate_text

CURRENT_DIR = Path(__file__).resolve().parent
MAX_BODY = 65536
MAX_AUDIO = 5242880
MAX_PROVIDER_RESPONSE = 10485760
ARTIFACTS = {
    "gtm_simulator.html": "text/html; charset=utf-8",
    "gtm_sprint_issues.csv": "text/csv; charset=utf-8",
    "gtm_sprint_issues.json": "application/json",
    "GTM_PITCH_DECK.md": "text/markdown; charset=utf-8",
}


def reject_constant(value):
    raise ValueError(f"Non-finite JSON constant: {value}")


class SocraticRequestHandler(BaseHTTPRequestHandler):
    def setup(self):
        super().setup()
        self.connection.settimeout(10)

    def trusted_request(self):
        hosts = self.headers.get_all("Host", [])
        if len(hosts) != 1:
            return False
        try:
            host = urlsplit("//" + hosts[0])
            if (host.hostname not in {"localhost", "127.0.0.1"}
                    or host.port != self.server.server_port
                    or host.username or host.password or host.path):
                return False
        except ValueError:
            return False
        origins = self.headers.get_all("Origin", [])
        if len(origins) > 1 or (origins and origins[0] != "http://" + hosts[0]):
            return False
        return self.headers.get("Sec-Fetch-Site", "") != "cross-site"

    def respond(self, code, body, content_type="application/json", head=False):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Frame-Options", "DENY")
        self.end_headers()
        if not head:
            self.wfile.write(body)

    def send_json_response(self, code, data, head=False):
        self.respond(code, json.dumps(data, allow_nan=False).encode("utf-8"), head=head)

    def error(self, code, message, head=False):
        self.discard_rejected_body()
        self.close_connection = True
        body = {"error": message}
        if urlsplit(self.path).path in {"/api/tts", "/api/stt"}:
            body["fallback"] = True
        self.send_json_response(code, body, head=head)

    def discard_rejected_body(self):
        # Closing with unread input can replace the HTTP error with a TCP reset.
        if self.command != "POST" or getattr(self, "body_read", False):
            return
        self.body_read = True
        lengths = self.headers.get_all("Content-Length", [])
        if len(lengths) != 1 or self.headers.get("Transfer-Encoding"):
            return
        try:
            remaining = int(lengths[0])
        except ValueError:
            return
        if not 0 < remaining <= MAX_BODY:
            return
        previous_timeout = self.connection.gettimeout()
        deadline = time.monotonic() + 1
        try:
            while remaining:
                time_left = deadline - time.monotonic()
                if time_left <= 0:
                    break
                self.connection.settimeout(time_left)
                chunk = self.rfile.read1(remaining)
                if not chunk:
                    break
                remaining -= len(chunk)
        except OSError:
            pass
        finally:
            self.connection.settimeout(previous_timeout)

    def do_HEAD(self):
        self.serve_get(head=True)

    def do_GET(self):
        self.serve_get()

    def serve_get(self, head=False):
        if not self.trusted_request():
            return self.error(403, "Local same-origin requests only", head)
        path = urlsplit(self.path).path
        if path == "/":
            self.send_response(302)
            self.send_header("Location", "/ui/index.html")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        if path == "/api/status":
            return self.send_json_response(200, {
                "status": "online", "framework": "Socratic GTM Strategist v3.0",
                "assessment_mode": "founder_intake_review_required",
                "speech_support": {"stt": "browser-dependent", "tts": "browser-dependent",
                                   "note": "Microphone permission and optional provider credentials required"},
            }, head)
        if path == "/ui/index.html":
            file, content_type = CURRENT_DIR / "ui" / "index.html", "text/html; charset=utf-8"
        elif path == "/ui/session.js":
            file, content_type = CURRENT_DIR / "ui" / "session.js", "application/javascript; charset=utf-8"
        elif path == "/openapi.json":
            file, content_type = CURRENT_DIR / "ui" / "openapi.json", "application/json"
        elif path.startswith("/artifacts/") and path.removeprefix("/artifacts/") in ARTIFACTS:
            name = path.removeprefix("/artifacts/")
            file, content_type = self.output_path(name), ARTIFACTS[name]
        else:
            return self.error(404, "Route not found", head)
        try:
            self.respond(200, file.read_bytes(), content_type, head)
        except FileNotFoundError:
            self.error(404, "Artifact has not been generated", head)
        except OSError:
            self.error(500, "Could not read artifact", head)

    def output_path(self, name):
        directory = Path(getattr(self.server, "output_directory", Path.cwd() / "gtm_outputs")).resolve()
        path = directory / name
        if path.is_symlink() or path.resolve().parent != directory:
            raise ValueError("Output must remain inside the artifact directory")
        return path

    def do_POST(self):
        if not self.trusted_request():
            return self.error(403, "Local same-origin requests only")
        try:
            path = urlsplit(self.path).path
            if self.headers.get("Transfer-Encoding"):
                return self.error(400, "Transfer-Encoding is unsupported")
            lengths = self.headers.get_all("Content-Length", [])
            if len(lengths) != 1:
                return self.error(400, "One Content-Length is required")
            length = int(lengths[0])
            if length < 0:
                return self.error(400, "Content-Length must be non-negative")
            ceiling = MAX_AUDIO if path == "/api/stt" else MAX_BODY
            if length > ceiling:
                return self.error(413, f"Request body exceeds {ceiling} bytes")
            if path == "/api/stt" and not self.headers.get("x-api-key"):
                return self.error(400, "A provider key is required; browser fallback is available")
            if path != "/api/stt" and self.headers.get_content_type() != "application/json":
                return self.error(415, "Use application/json")
            self.body_read = True
            body = self.rfile.read(length)
            if len(body) != length:
                return self.error(400, "Incomplete request body")
            if path == "/api/stt":
                return self.voice_stt(body)
            data = json.loads(body.decode("utf-8"), parse_constant=reject_constant)
            if not isinstance(data, dict):
                raise ValueError("JSON body must be an object")
            if path == "/api/tts":
                return self.voice_tts(data)
            result = self.execute(path, data)
            self.send_json_response(200, result)
        except (ValueError, TypeError, UnicodeError, RecursionError) as exc:
            self.error(400, str(exc))
        except TimeoutError:
            self.error(408, "Request body timed out")
        except OSError:
            self.error(500, "Local tool could not complete; retry after checking output access")

    def provider_proxy(self, url, body, headers, content_type):
        request = urllib.request.Request(url, data=body, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                payload = response.read(MAX_PROVIDER_RESPONSE + 1)
            if len(payload) > MAX_PROVIDER_RESPONSE:
                return self.error(502, "Provider response exceeded the local limit")
            if content_type == "application/json":
                # Validate the response without disclosing a provider error body.
                result = json.loads(payload, parse_constant=reject_constant)
                if not isinstance(result, dict):
                    raise ValueError("Provider returned invalid transcription data")
            self.respond(200, payload, content_type)
        except (OSError, ValueError, RecursionError):
            self.error(502, "Voice provider unavailable; use browser voice or check provider settings")

    def voice_stt(self, body):
        provider = self.headers.get("x-provider", "openai")
        targets = {"openai": "https://api.openai.com/v1/audio/transcriptions",
                   "groq": "https://api.groq.com/openai/v1/audio/transcriptions"}
        if provider not in targets or not body:
            raise ValueError("Choose a supported transcription provider and supply audio")
        content_type = self.headers.get("Content-Type", "")
        if not content_type.startswith("multipart/form-data;") or "boundary=" not in content_type:
            return self.error(415, "Use multipart/form-data with a boundary")
        key = validate_text(self.headers.get("x-api-key"), "provider key", 1000)
        self.provider_proxy(targets[provider], body,
                            {"Authorization": "Bearer " + key, "Content-Type": content_type},
                            "application/json")

    def voice_tts(self, data):
        provider = data.get("provider", "openai")
        key = validate_text(data.get("apiKey"), "provider key", 1000)
        text = validate_text(data.get("text"), "speech text", 4000)
        voice = validate_text(data.get("voice") or ("nova" if provider == "openai" else "21m00Tcm4TlvDq8ikWAM"), "voice", 100)
        if provider == "openai":
            if voice not in {"alloy", "echo", "fable", "onyx", "nova", "shimmer"}:
                raise ValueError("Unsupported OpenAI voice")
            url = "https://api.openai.com/v1/audio/speech"
            body = {"model": "tts-1", "voice": voice, "input": text}
            headers = {"Authorization": "Bearer " + key}
        elif provider == "elevenlabs":
            if not re.fullmatch(r"[A-Za-z0-9_-]+", voice):
                raise ValueError("Voice ID contains invalid characters")
            url = "https://api.elevenlabs.io/v1/text-to-speech/" + voice
            body = {"model_id": "eleven_monolingual_v1", "text": text,
                    "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}}
            headers = {"xi-api-key": key}
        else:
            raise ValueError("Unsupported speech provider")
        headers["Content-Type"] = "application/json"
        self.provider_proxy(url, json.dumps(body).encode("utf-8"), headers, "audio/mpeg")

    def execute(self, path, data):
        if path == "/api/chat":
            message = validate_text(data.get("message"), "message")
            phase = data.get("phase", 0)
            if type(phase) is not int or not 0 <= phase <= 9:
                raise ValueError("phase must be an integer from 0 through 9")
            context = data.get("context", {})
            if not isinstance(context, dict) or not isinstance(context.get("phases", {}), dict):
                raise ValueError("context and context.phases must be objects")
            context = {**context, "phases": dict(context.get("phases", {}))}
            assessment = None
            if phase == 0:
                context["concept"] = message
                next_phase = 1
            elif phase <= 8:
                assessment = assess_answer(phase, message)
                context["phases"][str(phase)] = message
                next_phase = phase + 1
            else:
                next_phase = 9
            if next_phase <= 8:
                title, question = PHASES[next_phase - 1]
                reply = f"Recorded as founder-reported input; evidence review remains required.\n\nPhase {next_phase}: {title}\n\n{question}"
            else:
                reply = ("Interview intake complete. Answers still require evidence review. "
                         "No strategic validation or artifact generation has occurred in this chat. "
                         "Use the explicit generator actions or the CLI to create draft files.")
            return {"reply": reply, "monologue": "Intake summary: founder-reported; no automated strategic confidence.",
                    "phase": next_phase, "confidence": None, "context": context,
                    "assessment": assessment}

        if path == "/api/simulate":
            project = validate_text(data.get("project_name", "AI Startup"), "project_name", 200)
            out = self.output_path("gtm_simulator.html")
            generate_dashboard(project, data.get("scores", [None] * 8),
                               ["User-supplied scenario; evidence review required."] * 8, out)
            return {"success": True, "path": "/artifacts/" + out.name}
        if path == "/api/export":
            csv_path = self.output_path("gtm_sprint_issues.csv")
            json_path = self.output_path("gtm_sprint_issues.json")
            export_issues(DEFAULT_ISSUES, csv_path, json_path)
            return {"success": True, "csv": "/artifacts/" + csv_path.name,
                    "json": "/artifacts/" + json_path.name}
        if path == "/api/recon":
            return {"report": generate_recon_report(
                validate_text(data.get("incumbent", "Salesforce"), "incumbent", 200),
                validate_text(data.get("domain", "AI automation"), "domain", 200))}
        if path == "/api/stress-test":
            return {"brief": generate_adversarial_brief(
                data.get("mode", "ciso"),
                validate_text(data.get("startup_name", "AI Startup"), "startup_name", 200))}
        if path == "/api/pitch-deck":
            out = self.output_path("GTM_PITCH_DECK.md")
            generate_pitch_deck(validate_text(data.get("startup_name", "AI Startup"), "startup_name", 200), out)
            return {"deck": out.read_text(encoding="utf-8"), "path": "/artifacts/" + out.name}
        raise ValueError("Unknown API route")

    def log_message(self, format, *args):
        # Do not log founder answers or external snippets.
        return None


def start_server(port=8000, open_browser=True, host="127.0.0.1"):
    httpd = ThreadingHTTPServer((host, port), SocraticRequestHandler)
    httpd.output_directory = Path.cwd() / "gtm_outputs"
    url = f"http://127.0.0.1:{httpd.server_port}/ui/index.html"
    print(f"[+] Local GTM intake dashboard: {url}", file=sys.stderr)
    if open_browser:
        webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("port_pos", nargs="?", type=int)
    parser.add_argument("--port", "-p", default=8000, type=int)
    parser.add_argument("--host", choices=["127.0.0.1", "0.0.0.0"], default="127.0.0.1")
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()
    start_server(args.port_pos if args.port_pos is not None else args.port, not args.no_browser, args.host)
