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

def cmd_start(args):
    """Interactive terminal Socratic interview mode."""
    banner = r"""
  ____                  _   _         ____ _____ __  __ 
 / ___|  ___   ___ _ __| |_(_) ___   / ___|_   _|  \/  |
 \___ \ / _ \ / __| '__| __| |/ __| | |  _  | | | |\/| |
  ___) | (_) | (__| |  | |_| | (__  | |_| | | | | |  | |
 |____/ \___/ \___|_|   \__|_|\___|  \____| |_| |_|  |_|
  AI Startup GTM Partner & Socratic Risk Auditor (v3.0)
=========================================================
"""
    print(banner)
    startup_name = input("Enter your AI Startup / Project Name: ").strip() or "MyAI"
    print(f"\n[+] Initializing Socratic Review for: {startup_name}\n")
    print("Answer the questions below to evaluate your GTM motion and build your execution suite.\n")

    phases = [
        ("Phase 1: Interaction Frequency & Virality", "How often does an end-user naturally touch or get value from your product (Daily, Weekly, Monthly, or Annual)? And how naturally do users brag about 'magic moments'?"),
        ("Phase 2: Ticking Clock vs Incumbents", "What is the primary distribution advantage of your top incumbent, and why would users stay with you if they ship an AI copycat in 12 months?"),
        ("Phase 3: The Adoption Vector (PLG vs CISO)", "Who uses the app day-to-day versus who signs the check? Are you designing for practitioner delight or enterprise IT compliance checklists on Day 1?"),
        ("Phase 4: Expansion Vector", "Are you forcing a narrow niche on Day 1, or starting horizontal to extract power-user routines before verticalizing?"),
        ("Phase 5: Proactive Routines vs Chatbox", "Does your user have to remember to prompt a text box, or does your app run scheduled background routines delivering ROI?"),
        ("Phase 6: Defensive Layer & Moats", "Are you tied to a single foundation model, and how do you guarantee customer ownership of context data?"),
        ("Phase 7: AI Pricing Paradox", "Are you pricing per-seat (which AI destroys), or pricing on consumption, outcomes, or tasks?"),
        ("Phase 8: Data Gravity & Integrations", "What existing systems does your agent read/write natively, and how deep is the bi-directional sync?")
    ]

    scores = []
    answers = []

    for name, question in phases:
        print(f"\n--- {name} ---")
        print(f"Q: {question}")
        ans = input("\nYour Answer: ").strip()
        answers.append(ans)
        # Heuristic confidence calculation
        words = len(ans.split())
        score = min(95, max(60, 60 + words))
        scores.append(score)
        status = "PASSED (>= 85%)" if score >= 85 else "BORDERLINE (< 85%)"
        print(f"[Score: {score}/100 - {status}]")

    print("\n=========================================================")
    print("[+] All 8 phases completed. Synthesizing 5-Piece Operational Suite...")
    
    # 1. Simulator
    sim_path = f"{startup_name.lower().replace(' ', '_')}_gtm_simulator.html"
    generate_dashboard(startup_name, scores, [f"Score: {s}/100" for s in scores], sim_path)
    print(f"  [✓] Interactive HTML Simulator: {sim_path}")

    # 2. Issues Backlog
    csv_path = f"{startup_name.lower().replace(' ', '_')}_sprint_issues.csv"
    json_path = f"{startup_name.lower().replace(' ', '_')}_sprint_issues.json"
    export_issues(DEFAULT_ISSUES, csv_path, json_path)
    print(f"  [✓] Linear/Jira Sprint Backlog: {csv_path}")

    # 3. Pitch Deck
    deck_path = f"{startup_name.lower().replace(' ', '_')}_GTM_PITCH_DECK.md"
    generate_pitch_deck(startup_name, deck_path)
    print(f"  [✓] Investor Pitch Deck Copy: {deck_path}")

    # 4. Adversarial Brief
    brief_path = f"{startup_name.lower().replace(' ', '_')}_adversarial_brief.md"
    generate_adversarial_brief("ciso", startup_name, brief_path)
    print(f"  [✓] Enterprise CISO Readiness Brief: {brief_path}")

    avg_score = round(sum(scores) / len(scores))
    print(f"\n[+] Audit Complete! Overall GTM Resilience Score: {avg_score}/100\n")

def cmd_mcp(args):
    mcp_server.main()

def main():
    parser = argparse.ArgumentParser(
        prog="socratic-gtm",
        description="Socratic GTM Strategist for AI Startups (v3.0) - CLI & MCP Toolsuite"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # start / interactive
    p_start = subparsers.add_parser("start", help="Launch interactive terminal Socratic review")
    p_start.set_defaults(func=cmd_start)

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
