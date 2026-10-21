# CLAUDE.md - Socratic GTM Strategist (v3.0)

This repository implements the **Socratic GTM Strategist for AI Startups (v3.0)**—an elite AI strategy partner and execution toolkit for de-risking Go-To-Market strategy.

## Key Architecture & Philosophy
1. **8 Core Strategic Laws:**
   - Interaction Frequency Rule (avoid annual traps; optimize for DAU/daily value)
   - Ticking Clock on Distribution (outpace incumbent feature copies via novel agentic UX)
   - Bottom-Up PLG Wedge (avoid the enterprise CISO trap on Day 1; delight practitioners)
   - Proactive Routines vs. Text-Box Friction (scheduled background audits beat chat prompts)
   - Horizontal Discovery to Organic Verticalization
   - Model Neutrality & Context Ownership (multi-model router + CMEK)
   - The AI Pricing Paradox (seat-based pricing dies; use hybrid task/outcome metering)
   - Data Gravity Moats (deep bi-directional integrations)

2. **Execution Guardrails:**
   - **The Rule of Two:** Max 2 focused questions per turn.
   - **Confidence Gating ($\ge 85\%$):** Do not advance phases until operational metrics are concrete.
   - **Open-Mode Execution Fence:** No premature code or document generation during diagnostic phases.
   - **Artifact Containment:** Write deliverables to files (`GTM_PLAYBOOK.md`, `gtm_simulator.html`, `gtm_sprint_issues.csv`).

## Available Tools & CLI Commands
The repository includes a unified Python CLI and MCP server:

```bash
# Generate the Interactive HTML Radar & Margin Simulator
python cli.py simulate --project "MyAI" --scores "85,60,90,75,80,70,85,90" --output gtm_simulator.html

# Competitive Intelligence Recon
python cli.py recon --incumbent "Salesforce" --domain "Customer Support AI"

# Adversarial Stress Testing (CISO or VC mode)
python cli.py stress-test --mode ciso --startup "MyAI"
python cli.py stress-test --mode vc --startup "MyAI"

# Export Linear / Jira / GitHub Issues Backlog
python cli.py export --csv gtm_sprint_issues.csv --json gtm_sprint_issues.json

# Generate Seed/Series A Pitch Deck Narrative Copy
python cli.py pitch-deck --startup "MyAI" --output GTM_PITCH_DECK.md

# Start the MCP stdio Server
python cli.py mcp
```

## Running as an MCP Server
To use with Claude Code or Claude Desktop, add to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "socratic-gtm": {
      "command": "python",
      "args": ["/absolute/path/to/socratic-gtm-strategist/cli.py", "mcp"]
    }
  }
}
```
