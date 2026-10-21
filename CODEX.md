# CODEX.md - Socratic GTM Strategist Instructions

## Purpose
This repository provides the Socratic GTM Strategist operating system for AI startups.

## Operational Instructions
When operating in this codebase:
1. Reference `SKILL.md` for the complete 8-phase Socratic dialogue framework.
2. Run tools using `python cli.py <subcommand>`:
   - `python cli.py simulate`: Generates the HTML radar chart and margin simulator.
   - `python cli.py recon --incumbent <Name>`: Runs live competitor intelligence.
   - `python cli.py stress-test --mode <ciso|vc>`: Conducts adversarial stress-test scenarios.
   - `python cli.py export`: Emits sprint issues for Linear/Jira.
   - `python cli.py pitch-deck`: Formats pitch deck narrative slides.
   - `python cli.py mcp`: Exposes all tools as a standard Model Context Protocol server.
3. Keep conversational pacing intact: 2 questions per turn maximum, enforce the 85% confidence threshold before advancing phases.
