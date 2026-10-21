#!/usr/bin/env python3
"""
Socratic GTM Strategist - Unified CLI & MCP Entrypoint
Usage:
    python cli.py simulate [--project NAME] [--scores 85,70,...] [--output PATH]
    python cli.py recon --incumbent NAME [--domain DOMAIN] [--output PATH]
    python cli.py stress-test [--mode ciso|vc] [--startup NAME] [--output PATH]
    python cli.py export [--csv PATH] [--json PATH]
    python cli.py pitch-deck [--startup NAME] [--output PATH]
    python cli.py mcp
"""

import sys
import os
import argparse

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

current_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.join(current_dir, "scripts")
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from generate_dashboard import generate_dashboard
from incumbent_recon import generate_recon_report
from stress_test_simulator import generate_adversarial_brief
from export_issues import export_issues, DEFAULT_ISSUES
from generate_pitch_deck import generate_pitch_deck
import mcp_server

def cmd_simulate(args):
    scores = [int(s.strip()) for s in args.scores.split(",")]
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
    generate_dashboard(args.project, scores, notes, args.output)

def cmd_recon(args):
    generate_recon_report(args.incumbent, args.domain, args.output)

def cmd_stress_test(args):
    generate_adversarial_brief(args.mode, args.startup, args.output)

def cmd_export(args):
    export_issues(DEFAULT_ISSUES, args.csv, args.json)

def cmd_pitch_deck(args):
    generate_pitch_deck(args.startup, args.output)

def cmd_mcp(args):
    mcp_server.main()

def main():
    parser = argparse.ArgumentParser(
        prog="socratic-gtm",
        description="Socratic GTM Strategist for AI Startups (v3.0) - CLI & MCP Toolsuite"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # simulate
    p_sim = subparsers.add_parser("simulate", help="Generate interactive HTML Radar & Margin Simulator")
    p_sim.add_argument("--project", default="AI Startup", help="Project/startup name")
    p_sim.add_argument("--scores", default="85,75,90,70,80,85,75,90", help="Comma-separated 8 scores (0-100)")
    p_sim.add_argument("--output", default="gtm_simulator.html", help="Output HTML file path")
    p_sim.set_defaults(func=cmd_simulate)

    # recon
    p_rec = subparsers.add_parser("recon", help="Run competitive AI reconnaissance on an incumbent")
    p_rec.add_argument("--incumbent", required=True, help="Competitor or incumbent name (e.g. Salesforce, Notion)")
    p_rec.add_argument("--domain", default="AI workflow automation", help="Startup vertical domain")
    p_rec.add_argument("--output", default="incumbent_recon.md", help="Output markdown path")
    p_rec.set_defaults(func=cmd_recon)

    # stress-test
    p_st = subparsers.add_parser("stress-test", help="Run CISO or VC adversarial grilling")
    p_st.add_argument("--mode", choices=["ciso", "vc"], default="ciso", help="Persona mode")
    p_st.add_argument("--startup", default="My AI Startup", help="Startup name")
    p_st.add_argument("--output", default="adversarial_brief.md", help="Output markdown path")
    p_st.set_defaults(func=cmd_stress_test)

    # export
    p_exp = subparsers.add_parser("export", help="Export sprint issues for Linear, Jira, GitHub Issues & Notion")
    p_exp.add_argument("--csv", default="gtm_sprint_issues.csv", help="Output CSV path")
    p_exp.add_argument("--json", default="gtm_sprint_issues.json", help="Output JSON path")
    p_exp.set_defaults(func=cmd_export)

    # pitch-deck
    p_pd = subparsers.add_parser("pitch-deck", help="Generate 5-slide Seed/Series A pitch deck copy")
    p_pd.add_argument("--startup", default="My AI Startup", help="Startup name")
    p_pd.add_argument("--output", default="GTM_PITCH_DECK.md", help="Output markdown path")
    p_pd.set_defaults(func=cmd_pitch_deck)

    # mcp
    p_mcp = subparsers.add_parser("mcp", help="Run the Model Context Protocol (MCP) stdio server")
    p_mcp.set_defaults(func=cmd_mcp)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)

if __name__ == "__main__":
    main()
