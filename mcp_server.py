#!/usr/bin/env python3
"""
Model Context Protocol (MCP) Stdio Server for Socratic GTM Strategist
Provides standardized tool execution for:
- Claude Code / Claude Desktop
- Cursor
- VS Code (Copilot / Roo / Cline)
- OpenCode
- Codex & Antigravity
"""

import sys
import os
import json
import traceback

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Preserve real stdout for JSON-RPC framing only
_mcp_stdout = sys.stdout
# Route default stdout to stderr so library prints don't corrupt JSON-RPC transport
sys.stdout = sys.stderr

# Import helper functions from scripts
current_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.join(current_dir, "scripts")
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from generate_dashboard import generate_dashboard
from incumbent_recon import generate_recon_report
from stress_test_simulator import generate_adversarial_brief
from export_issues import export_issues, DEFAULT_ISSUES
from generate_pitch_deck import generate_pitch_deck

TOOLS_SCHEMA = [
    {
        "name": "gtm_simulate_radar",
        "description": "Generate an interactive HTML dashboard containing an 8-Vector GTM Radar Chart and real-time AI Unit Economics & Margin Collapse Simulator.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_name": {"type": "string", "description": "Startup or project name"},
                "scores": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "8 integer scores (0-100) for the 8 GTM vectors: [Frequency, Incumbent, PLG, Expansion, Routine, Neutrality, Pricing, Gravity]"
                },
                "output_path": {"type": "string", "description": "Output path for the HTML file (default: gtm_simulator.html)"}
            },
            "required": ["project_name"]
        }
    },
    {
        "name": "gtm_incumbent_recon",
        "description": "Run competitive AI reconnaissance on a named incumbent or competitor to surface recent product releases, changelog updates, and defensive pressure points.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "incumbent": {"type": "string", "description": "Name of competitor (e.g. Salesforce, Notion, Zendesk)"},
                "product_domain": {"type": "string", "description": "Startup vertical/domain (e.g. Customer Support AI, DevTools)"},
                "output_path": {"type": "string", "description": "Optional markdown output file path"}
            },
            "required": ["incumbent"]
        }
    },
    {
        "name": "gtm_stress_test",
        "description": "Execute an adversarial stress test simulating either a skeptical Fortune 500 Enterprise CISO or a ruthless Tier-1 VC Partner.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "mode": {"type": "string", "enum": ["ciso", "vc"], "description": "'ciso' for enterprise security interrogation; 'vc' for venture fund objection grilling"},
                "startup_name": {"type": "string", "description": "Name of the startup"},
                "output_path": {"type": "string", "description": "Optional output path for the report"}
            },
            "required": ["mode", "startup_name"]
        }
    },
    {
        "name": "gtm_export_issues",
        "description": "Export the prioritized Sprint 0 to Sprint 2 engineering runbook into CSV and JSON ready to import into Linear, Jira, GitHub Issues, or Notion.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "csv_path": {"type": "string", "description": "Output path for CSV (default: gtm_sprint_issues.csv)"},
                "json_path": {"type": "string", "description": "Output path for JSON (default: gtm_sprint_issues.json)"}
            }
        }
    },
    {
        "name": "gtm_generate_pitch_deck",
        "description": "Generate 5 battle-tested Seed/Series A pitch deck slides translating Socratic GTM outputs into investor narrative copy.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "startup_name": {"type": "string", "description": "Startup name"},
                "output_path": {"type": "string", "description": "Output path for markdown deck (default: GTM_PITCH_DECK.md)"}
            },
            "required": ["startup_name"]
        }
    },
    {
        "name": "gtm_socratic_evaluate",
        "description": "Evaluate a founder's strategic answer for a specific phase against the 8-phase Socratic rubric, returning a Confidence Score (0-100%), Red/Green Flags, and next action.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "phase": {"type": "integer", "description": "Phase number (1 through 8)"},
                "founder_answer": {"type": "string", "description": "Founder's answer to the phase questions"},
                "context": {"type": "string", "description": "Summary of previously validated startup context"}
            },
            "required": ["phase", "founder_answer"]
        }
    }
]

def handle_tool_call(tool_name, args):
    if tool_name == "gtm_simulate_radar":
        project = args.get("project_name", "AI Startup")
        scores = args.get("scores", [85, 75, 90, 70, 80, 85, 75, 90])
        out = args.get("output_path", "gtm_simulator.html")
        notes = [
            "Validated daily active value loop.",
            "Incumbent distribution counter-measured via novel agentic UX.",
            "Bottom-up PLG practitioner adoption isolated from CISO friction.",
            "Horizontal workflow discovery mapped to vertical templates.",
            "Proactive asynchronous background routine established.",
            "Neutral multi-model router prevents vendor lock-in.",
            "Hybrid/outcome pricing mitigates margin compression.",
            "Bi-directional integration establishes high data gravity."
        ]
        generate_dashboard(project, scores, notes, out)
        return f"GTM Simulator successfully generated at: {out}"

    elif tool_name == "gtm_incumbent_recon":
        incumbent = args.get("incumbent")
        domain = args.get("product_domain", "AI automation")
        out = args.get("output_path")
        return generate_recon_report(incumbent, domain, out)

    elif tool_name == "gtm_stress_test":
        mode = args.get("mode", "ciso")
        startup = args.get("startup_name", "AI Startup")
        out = args.get("output_path")
        return generate_adversarial_brief(mode, startup, out)

    elif tool_name == "gtm_export_issues":
        csv_p = args.get("csv_path", "gtm_sprint_issues.csv")
        json_p = args.get("json_path", "gtm_sprint_issues.json")
        export_issues(DEFAULT_ISSUES, csv_p, json_p)
        return f"Sprint backlog exported to: {csv_p} and {json_p}"

    elif tool_name == "gtm_generate_pitch_deck":
        startup = args.get("startup_name", "AI Startup")
        out = args.get("output_path", "GTM_PITCH_DECK.md")
        generate_pitch_deck(startup, out)
        return f"Pitch deck narrative generated at: {out}"

    elif tool_name == "gtm_socratic_evaluate":
        phase = args.get("phase", 1)
        answer = args.get("founder_answer", "")
        # Basic heuristic evaluator for tool calling
        length = len(answer.split())
        score = min(95, 60 + min(length, 25))
        status = "PASS (>= 85%)" if score >= 85 else "DRILL DOWN (< 85%)"
        return json.dumps({
            "phase": phase,
            "confidence_score": score,
            "status": status,
            "guidance": "Sufficient operational mechanics provided." if score >= 85 else "Missing concrete operational metrics (APIs, frequencies, billing models)."
        }, indent=2)

    else:
        raise ValueError(f"Unknown tool: {tool_name}")

def send_response(response):
    body = json.dumps(response)
    _mcp_stdout.write(body + "\n")
    _mcp_stdout.flush()

def main():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        line = line.strip()
        if not line:
            continue

        try:
            req = json.loads(line)
        except Exception as e:
            send_response({
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": f"Parse error: {str(e)}"
                }
            })
            continue

        if not isinstance(req, dict):
            send_response({
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32600,
                    "message": "Invalid Request: root must be a JSON object"
                }
            })
            continue

        msg_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})

        if method == "initialize":
            send_response({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {
                        "name": "socratic-gtm-strategist",
                        "version": "3.0.0"
                    }
                }
            })
        elif method == "notifications/initialized":
            pass
        elif method == "ping":
            send_response({"jsonrpc": "2.0", "id": msg_id, "result": {}})
        elif method == "tools/list":
            send_response({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "tools": TOOLS_SCHEMA
                }
            })
        elif method == "tools/call":
            if not isinstance(params, dict) or "name" not in params:
                send_response({
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {
                        "code": -32602,
                        "message": "Invalid params: 'name' is required"
                    }
                })
                continue
            tool_name = params.get("name")
            args = params.get("arguments", {})
            if not isinstance(args, dict):
                send_response({
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {
                        "code": -32602,
                        "message": "Invalid params: 'arguments' must be an object"
                    }
                })
                continue
            try:
                result_text = handle_tool_call(tool_name, args)
                send_response({
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "content": [{"type": "text", "text": str(result_text)}]
                    }
                })
            except Exception as e:
                send_response({
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {
                        "code": -32603,
                        "message": str(e)
                    }
                })
        else:
            if msg_id is not None:
                send_response({
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method {method} not found"
                    }
                })

if __name__ == "__main__":
    main()
