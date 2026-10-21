"""
Socratic GTM Strategist (v3.0) - Python SDK for Local & Cloud Agents
Provides direct library access for LangChain, CrewAI, AutoGen, LlamaIndex, and custom agents.
"""

import os
import sys

# Ensure scripts directory is available
_current_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_current_dir)
_scripts_dir = os.path.join(_parent_dir, "scripts")
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)

from generate_dashboard import generate_dashboard
from incumbent_recon import generate_recon_report
from stress_test_simulator import generate_adversarial_brief
from export_issues import export_issues, DEFAULT_ISSUES
from generate_pitch_deck import generate_pitch_deck

def get_system_prompt() -> str:
    """Return the complete Socratic GTM Strategist v3.0 system prompt."""
    prompt_path = os.path.join(_parent_dir, "SKILL.md")
    if os.path.exists(prompt_path):
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def get_langchain_tools():
    """Return LangChain-compatible structured tool definitions."""
    try:
        from langchain.tools import tool
    except ImportError:
        raise ImportError("LangChain is required to use get_langchain_tools(). Install with `pip install langchain`.")

    @tool
    def simulate_radar(project_name: str, scores: list[int], output_path: str = "gtm_simulator.html") -> str:
        """Generate interactive HTML GTM Radar & AI Margin Simulator."""
        notes = ["Validated." for _ in scores]
        generate_dashboard(project_name, scores, notes, output_path)
        return f"Dashboard generated at {output_path}"

    @tool
    def incumbent_recon(incumbent: str, product_domain: str = "AI automation") -> str:
        """Run competitive AI intelligence on an incumbent competitor."""
        return generate_recon_report(incumbent, product_domain)

    @tool
    def adversarial_stress_test(mode: str, startup_name: str) -> str:
        """Run CISO or VC adversarial stress test."""
        return generate_adversarial_brief(mode, startup_name)

    @tool
    def export_sprint_issues(csv_path: str = "gtm_sprint_issues.csv") -> str:
        """Export prioritized Linear/Jira/GitHub sprint issues."""
        export_issues(DEFAULT_ISSUES, csv_path, "gtm_sprint_issues.json")
        return f"Issues exported to {csv_path}"

    @tool
    def generate_deck_copy(startup_name: str) -> str:
        """Generate 5-slide Seed/Series A pitch deck copy."""
        generate_pitch_deck(startup_name, "GTM_PITCH_DECK.md")
        return "Pitch deck generated in GTM_PITCH_DECK.md"

    return [simulate_radar, incumbent_recon, adversarial_stress_test, export_sprint_issues, generate_deck_copy]

__all__ = [
    "generate_dashboard",
    "generate_recon_report",
    "generate_adversarial_brief",
    "export_issues",
    "generate_pitch_deck",
    "get_system_prompt",
    "get_langchain_tools"
]
