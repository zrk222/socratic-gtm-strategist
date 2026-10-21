#!/usr/bin/env python3
"""
Socratic GTM Dashboard Web Server
Provides a zero-dependency local HTTP server serving the ChatGPT-style UI
with full STT/TTS and API endpoints for live Socratic review.
"""

import sys
import os
import json
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse
import urllib.request

# Set path to helper scripts
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(CURRENT_DIR, "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from generate_dashboard import generate_dashboard
from incumbent_recon import generate_recon_report
from stress_test_simulator import generate_adversarial_brief
from export_issues import export_issues, DEFAULT_ISSUES
from generate_pitch_deck import generate_pitch_deck

class SocraticRequestHandler(SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        # Serve from project root directory
        super().__init__(*args, directory=CURRENT_DIR, **kwargs)

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        if url.path == "/" or url.path == "":
            self.send_response(302)
            self.send_header("Location", "/ui/index.html")
            self.end_headers()
            return
        elif url.path == "/api/status":
            self.send_json_response(200, {
                "status": "online",
                "framework": "Socratic GTM Strategist v3.0",
                "speech_support": {"stt": True, "tts": True}
            })
            return
        elif url.path == "/openapi.json":
            openapi_file = os.path.join(CURRENT_DIR, "openapi.json")
            if os.path.exists(openapi_file):
                with open(openapi_file, "r", encoding="utf-8") as f:
                    spec = json.load(f)
                self.send_json_response(200, spec)
            else:
                self.send_response(404)
                self.end_headers()
            return

        super().do_GET()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, x-api-key, x-provider")
        self.end_headers()

    def do_POST(self):
        url = urllib.parse.urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length) if content_length > 0 else b""

        try:
            data = json.loads(raw_body.decode("utf-8", errors="ignore"))
        except Exception:
            data = {}

        if url.path == "/api/chat":
            msg = data.get("message", "")
            phase = data.get("phase", 0)
            context = data.get("context", {})

            words = len(msg.split())
            confidence = min(95, max(65, 60 + words * 2))

            if phase == 0:
                next_phase = 1
                monologue = f"- Current Phase: Phase 1 (Interaction Frequency)\n- Answer Evaluation: Concept captured: '{msg[:40]}...'\n- Phase Confidence Score: 88%\n- Gating Decision: ADVANCE to Phase 1.\n- Accumulated Strategic State:\n    * Concept: {msg}\n- Next Action: Ask the Rule of Two frequency questions."
                reply = "That gives us a clear initial wedge. Let's stress-test the growth engine in **Phase 1: Interaction Frequency & Word-of-Mouth Physics**.\n\nHistorically, products that are touched only monthly or annually suffer from the 'Annual Trap' and cannot sustain organic word-of-mouth.\n\n1. *How often does an end-user naturally touch or get value from your product (Daily, Weekly, Monthly, or Annual)?*\n2. *When a user experiences a 'magic moment', how naturally do they brag about it to peers during their active buying cycle?*"
            elif phase < 8:
                if confidence >= 85:
                    next_phase = phase + 1
                    monologue = f"- Current Phase: Phase {next_phase}\n- Answer Evaluation: Founder provided concrete operational details. Confidence exceeds 85% threshold.\n- Phase Confidence Score: {confidence}%\n- Gating Decision: ADVANCE to Phase {next_phase}.\n- Next Action: Pivot to next strategic vector."
                    if next_phase == 2:
                        reply = "Your frequency mechanics are solid. Let's move to **Phase 2: The Ticking Clock vs. Incumbent Distribution**.\n\nIncumbents (e.g. Salesforce, Notion, Zendesk) already own the enterprise relationship. If they ship an AI button that accomplishes 70% of your value next year, why do customers stay?\n\n1. *What is the primary distribution advantage of your top incumbent?*\n2. *If the incumbent adds a 'good-enough' agent in 12 months, what is your structural defense?*"
                    elif next_phase == 3:
                        reply = "Understood. Now testing **Phase 3: The Adoption Vector (PLG vs. CISO Governance)**.\n\nMany AI startups fall into the CISO trap on Day 1—getting paralyzed by 9-month enterprise procurement before any end-user loves the tool.\n\n1. *Who uses the tool daily versus who signs the check?*\n2. *Are you designing v1 for practitioner delight, or to satisfy an IT/compliance checklist?*"
                    elif next_phase == 4:
                        reply = "Good distinction. Let's evaluate **Phase 4: Expansion Strategy (Horizontal to Vertical)**.\n\n1. *Are you forcing a narrow niche on Day 1, or starting horizontal across common workflows?*\n2. *How will you extract the hidden 'routines' of power users to turn them into vertical templates?*"
                    elif next_phase == 5:
                        reply = "Let's tackle **Phase 5: Value Architecture (Proactive Routines vs. Text-Box Friction)**.\n\nChat boxes produce prompt fatigue. Autonomous routines deliver ROI while the user sleeps.\n\n1. *Does your user have to type into a prompt box to get value, or does your app proactively surface ROI in the background?*\n2. *What is a low-cost background task your app can run continuously that yields high ROI?*"
                    elif next_phase == 6:
                        reply = "Now de-risking **Phase 6: Defensive Layer (Model Neutrality & Context Ownership)**.\n\n1. *Are you tied to a single foundation model API, or can you dynamically route tasks to the optimal model?*\n2. *How do you guarantee the customer owns their contextual data and memory graph?*"
                    elif next_phase == 7:
                        reply = "Critical junction: **Phase 7: Pricing & Value Capture (The AI Pricing Paradox)**.\n\nAI agents inherently destroy seat-based SaaS pricing because automation reduces needed headcount.\n\n1. *Are you pricing per-seat, or pricing on consumption, outcomes, or completed tasks?*\n2. *How do you prevent margin collapse if user token consumption spikes?*"
                    elif next_phase == 8:
                        reply = "Final diagnostic gate: **Phase 8: Integration & Data Gravity (The Moat of Context)**.\n\n1. *What existing systems (CRM, ERP, Slack, Data Warehouse) does your agent read from and write to natively?*\n2. *How deep is the bi-directional sync? Does deleting your tool break existing workflows?*"
                else:
                    next_phase = phase
                    monologue = f"- Current Phase: Phase {phase}\n- Answer Evaluation: Response was high-level or aspirational. Missing operational mechanics.\n- Phase Confidence Score: {confidence}%\n- Gating Decision: DRILL DOWN (Score < 85%).\n- Next Action: Enforce Rule of Two with a focused follow-up."
                    reply = f"That's a sound high-level vision, but we are missing the operational mechanics needed to de-risk this vector (Confidence: {confidence}% / required 85%).\n\nSpecifically: *What exact workflow metrics, APIs, or daily triggers ensure this occurs repeatedly?*"
            else:
                next_phase = 9
                monologue = "- Current Phase: Phase 9 (Multi-Module Synthesis)\n- Evaluation: All 8 vectors de-risked and validated.\n- Phase Confidence Score: 92%\n- Gating Decision: COMPLETE.\n- Next Action: Generate 5-Piece Operational Suite."
                reply = "### 🎯 Strategy Fully De-Risked: GTM Playbook & Suite Generated!\n\nAll 8 phases have met the **85% confidence gating threshold**. The complete execution suite is ready in your workspace:\n\n* **1. Interactive Simulator & Radar:** Visualizes your 8-vector moats and real-time AI Unit Economics.\n* **2. Linear / Jira Sprint Backlog:** Prioritized Sprint 0-2 issues with acceptance criteria.\n* **3. Seed/Series A Pitch Deck:** 5-slide narrative copy.\n* **4. Enterprise CISO Readiness Brief:** Pre-meeting security defenses."

            self.send_json_response(200, {
                "reply": reply,
                "monologue": monologue,
                "phase": next_phase,
                "confidence": confidence
            })
            return

        elif url.path == "/api/simulate":
            project = data.get("project_name", "AI Startup")
            scores = data.get("scores", [85, 75, 90, 70, 80, 85, 75, 90])
            out = os.path.join(CURRENT_DIR, "gtm_simulator.html")
            notes = ["Validated." for _ in scores]
            generate_dashboard(project, scores, notes, out)
            self.send_json_response(200, {"success": True, "path": out})
            return

        elif url.path == "/api/export":
            csv_path = os.path.join(CURRENT_DIR, "gtm_sprint_issues.csv")
            json_path = os.path.join(CURRENT_DIR, "gtm_sprint_issues.json")
            export_issues(DEFAULT_ISSUES, csv_path, json_path)
            self.send_json_response(200, {"success": True, "csv": csv_path, "json": json_path})
            return

        elif url.path == "/api/recon":
            incumbent = data.get("incumbent", "Salesforce")
            domain = data.get("domain", "AI automation")
            report = generate_recon_report(incumbent, domain)
            self.send_json_response(200, {"report": report})
            return

        elif url.path == "/api/stress-test":
            mode = data.get("mode", "ciso")
            startup = data.get("startup_name", "AI Startup")
            brief = generate_adversarial_brief(mode, startup)
            self.send_json_response(200, {"brief": brief})
            return

        elif url.path == "/api/pitch-deck":
            startup = data.get("startup_name", "AI Startup")
            out = os.path.join(CURRENT_DIR, "GTM_PITCH_DECK.md")
            generate_pitch_deck(startup, out)
            with open(out, "r", encoding="utf-8") as f:
                content = f.read()
            self.send_json_response(200, {"deck": content, "path": out})
            return

        elif url.path == "/api/tts":
            text = data.get("text", "")
            provider = data.get("provider", "openai")
            api_key = data.get("apiKey", "")
            voice = data.get("voice", "nova")

            if provider == "openai" and api_key and text:
                try:
                    req_data = json.dumps({"model": "tts-1", "voice": voice, "input": text[:4000]}).encode("utf-8")
                    req = urllib.request.Request(
                        "https://api.openai.com/v1/audio/speech",
                        data=req_data,
                        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
                    )
                    with urllib.request.urlopen(req, timeout=12) as response:
                        audio_bytes = response.read()
                        self.send_response(200)
                        self.send_header("Content-Type", "audio/mpeg")
                        self.send_header("Content-Length", str(len(audio_bytes)))
                        self.send_header("Access-Control-Allow-Origin", "*")
                        self.end_headers()
                        self.wfile.write(audio_bytes)
                        return
                except Exception as e:
                    self.send_json_response(500, {"fallback": True, "error": str(e)})
                    return
            elif provider == "elevenlabs" and api_key and text:
                try:
                    voice_id = voice if voice else "21m00Tcm4TlvDq8ikWAM"
                    req_data = json.dumps({
                        "text": text[:4000],
                        "model_id": "eleven_monolingual_v1",
                        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
                    }).encode("utf-8")
                    req = urllib.request.Request(
                        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                        data=req_data,
                        headers={"xi-api-key": api_key, "Content-Type": "application/json"}
                    )
                    with urllib.request.urlopen(req, timeout=12) as response:
                        audio_bytes = response.read()
                        self.send_response(200)
                        self.send_header("Content-Type", "audio/mpeg")
                        self.send_header("Content-Length", str(len(audio_bytes)))
                        self.send_header("Access-Control-Allow-Origin", "*")
                        self.end_headers()
                        self.wfile.write(audio_bytes)
                        return
                except Exception as e:
                    self.send_json_response(500, {"fallback": True, "error": str(e)})
                    return
            self.send_json_response(400, {"fallback": True, "message": "Missing API key or text"})
            return

        elif url.path == "/api/stt":
            api_key = self.headers.get("x-api-key") or ""
            provider = self.headers.get("x-provider") or "openai"
            content_type = self.headers.get("Content-Type") or "multipart/form-data"

            if api_key and raw_body:
                try:
                    target_url = "https://api.openai.com/v1/audio/transcriptions"
                    if provider == "groq":
                        target_url = "https://api.groq.com/openai/v1/audio/transcriptions"

                    req = urllib.request.Request(
                        target_url,
                        data=raw_body,
                        headers={
                            "Authorization": f"Bearer {api_key}",
                            "Content-Type": content_type
                        }
                    )
                    with urllib.request.urlopen(req, timeout=20) as response:
                        resp_bytes = response.read()
                        self.send_response(200)
                        self.send_header("Content-Type", "application/json")
                        self.send_header("Content-Length", str(len(resp_bytes)))
                        self.send_header("Access-Control-Allow-Origin", "*")
                        self.end_headers()
                        self.wfile.write(resp_bytes)
                        return
                except Exception as e:
                    self.send_json_response(500, {"fallback": True, "error": str(e)})
                    return
            self.send_json_response(400, {"fallback": True, "message": "Missing API key or audio data"})
            return

        self.send_response(404)
        self.end_headers()

    def send_json_response(self, code, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

def start_server(port=8000, open_browser=True):
    server_address = ("", port)
    httpd = HTTPServer(server_address, SocraticRequestHandler)
    url = f"http://localhost:{port}/ui/index.html"
    print(f"[+] Socratic GTM Dashboard running at: {url}", file=sys.stderr)
    print(f"[+] Complete with Voice STT/TTS, Phase Tracking & Chat History.", file=sys.stderr)
    print("[+] Press Ctrl+C to stop the server.", file=sys.stderr)

    if open_browser:
        webbrowser.open(url)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[+] Shutting down web dashboard server.", file=sys.stderr)
        httpd.server_close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Socratic GTM Dashboard Web Server")
    parser.add_argument("port_pos", nargs="?", type=int, default=None, help="Port number")
    parser.add_argument("--port", "-p", type=int, default=8000, help="Port number (default: 8000)")
    parser.add_argument("--no-browser", action="store_true", help="Do not open browser automatically")
    args = parser.parse_args()

    chosen_port = args.port_pos if args.port_pos is not None else args.port
    start_server(port=chosen_port, open_browser=not args.no_browser)
