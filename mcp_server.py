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

# Real stdout stream for JSON-RPC framing
_mcp_stdout = sys.stdout

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
                    "items": {"type": "integer", "minimum": 0, "maximum": 100},
                    "minItems": 8, "maxItems": 8,
                    "description": "8 integer scores (0-100) for the 8 GTM vectors: [Frequency, Incumbent, PLG, Expansion, Routine, Neutrality, Pricing, Gravity]"
                },
                "output_path": {"type": "string", "description": "Output path for the HTML file (default: gtm_simulator.html)"}
            },
            "required": ["project_name"]
        }
    },
    {
        "name": "gtm_incumbent_recon",
        "description": "Run competitive AI reconnaissance on a named incumbent or competitor to surface unverified search snippets with source links and retrieval timestamps, or explicit unavailable status.",
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
        "description": "Generate 5 Seed/Series A pitch deck template slides with evidence-required fields; does not infer traction or margins.",
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
        "description": "Record founder-reported input and return a phase-specific review prompt. Always REVIEW_REQUIRED; confidence is null. No model evaluation or strategic validation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "phase": {"type": "integer", "minimum": 1, "maximum": 8, "description": "Phase number (1 through 8)"},
                "founder_answer": {"type": "string", "description": "Founder's answer to the phase questions"},
                "context": {"type": "string", "description": "Summary of previously validated startup context"}
            },
            "required": ["phase", "founder_answer"]
        }
    }
]

def validate_arguments(tool_name, args):
    tool = next((tool for tool in TOOLS_SCHEMA if tool["name"] == tool_name), None)
    if tool is None:
        raise ValueError(f"Unknown tool: {tool_name}")
    if not isinstance(args, dict):
        raise ValueError("arguments must be an object")
    schema = tool["inputSchema"]
    missing = set(schema.get("required", [])) - set(args)
    if missing:
        raise ValueError("Missing required arguments: " + ", ".join(sorted(missing)))
    if set(args) - set(schema["properties"]):
        raise ValueError("Unknown tool argument")
    for key, value in args.items():
        field = schema["properties"][key]
        expected = field["type"]
        valid = ((expected == "string" and isinstance(value, str) and value.strip()
                  and len(value) <= 10000 and "\\x00" not in value)
                 or (expected == "integer" and type(value) is int)
                 or (expected == "array" and isinstance(value, list)))
        if not valid:
            raise ValueError(f"Invalid {key}: expected {expected}")
        if "enum" in field and value not in field["enum"]:
            raise ValueError(f"Invalid {key}: choose from {field['enum']}")
        if key == "phase" and not 1 <= value <= 8:
            raise ValueError("phase must be between 1 and 8")
        if key == "scores":
            if len(value) != 8 or any(type(s) is not int or not 0 <= s <= 100 for s in value):
                raise ValueError("scores must contain exactly 8 integers from 0 to 100")


def handle_tool_call(tool_name, args):
    validate_arguments(tool_name, args)
    if tool_name == "gtm_simulate_radar":
        project = args.get("project_name", "AI Startup")
        scores = args.get("scores", [None] * 8)
        out = args.get("output_path", "gtm_simulator.html")
        notes = ["User-supplied scenario; evidence review required."] * 8
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
        from socratic_gtm.assessment import assess_answer
        return json.dumps(assess_answer(args["phase"], args["founder_answer"]), indent=2)

    else:
        raise ValueError(f"Unknown tool: {tool_name}")

def send_response(response):
    body = json.dumps(response)
    _mcp_stdout.write(body + "\n")
    _mcp_stdout.flush()

def main():
    """A bounded newline-delimited JSON-RPC stdio adapter."""
    global _mcp_stdout
    _mcp_stdout = sys.stdout
    sys.stdout = sys.stderr

    def error(msg_id, code, message):
        send_response({"jsonrpc": "2.0", "id": msg_id,
                       "error": {"code": code, "message": message}})

    while True:
        line = sys.stdin.readline(65537)
        if not line:
            break
        if len(line) > 65536:
            while line and not line.endswith("\n"):
                line = sys.stdin.readline(65537)
            error(None, -32700, "Message exceeds 65536 characters")
            continue
        if not line.strip():
            continue
        try:
            req = json.loads(line, parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))
        except (ValueError, RecursionError):
            error(None, -32700, "Invalid JSON")
            continue
        if (not isinstance(req, dict) or req.get("jsonrpc") != "2.0"
                or not isinstance(req.get("method"), str)
                or ("id" in req and type(req["id"]) not in (int, str))):
            error(None, -32600, "Invalid JSON-RPC 2.0 request")
            continue
        if "id" not in req:
            # Notifications never execute mutating request methods or receive replies.
            continue
        msg_id, method = req["id"], req["method"]
        params = req.get("params", {})
        if not isinstance(params, dict):
            error(msg_id, -32602, "params must be an object")
            continue
        if method == "initialize":
            send_response({"jsonrpc": "2.0", "id": msg_id, "result": {
                "protocolVersion": "2024-11-05", "capabilities": {"tools": {}},
                "serverInfo": {"name": "socratic-gtm-strategist", "version": "3.0.0"}}})
        elif method == "ping":
            send_response({"jsonrpc": "2.0", "id": msg_id, "result": {}})
        elif method == "tools/list":
            send_response({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS_SCHEMA}})
        elif method == "tools/call":
            name, arguments = params.get("name"), params.get("arguments", {})
            if (not isinstance(name, str) or not isinstance(arguments, dict)
                    or name not in {tool["name"] for tool in TOOLS_SCHEMA}):
                error(msg_id, -32602, "Known tool name and object arguments are required")
                continue
            try:
                text = handle_tool_call(name, arguments)
                result = {"content": [{"type": "text", "text": str(text)}]}
            except (ValueError, TypeError, OSError) as exc:
                result = {"content": [{"type": "text", "text": str(exc)}], "isError": True}
            except Exception:
                # Keep protocol stdout usable without leaking local traceback paths.
                result = {"content": [{"type": "text", "text": "Tool failed; check local output access and retry."}],
                          "isError": True}
            send_response({"jsonrpc": "2.0", "id": msg_id, "result": result})
        else:
            error(msg_id, -32601, f"Unknown method: {method}")


if __name__ == "__main__":
    main()
