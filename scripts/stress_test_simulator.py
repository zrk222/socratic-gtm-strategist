#!/usr/bin/env python3
"""
Adversarial Stress Test Simulator: The CISO & VC Inquisition
Generates adversarial grilling scenarios and pre-meeting defense briefs
for founders pitching to enterprise buyers or venture investors.
"""

import sys
import os
import argparse

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

CISO_QUESTIONS = [
    {
        "domain": "Data Egress & Model Training",
        "question": "Does our proprietary enterprise context ever hit public foundation model APIs, and what legally binding guarantee prevents our IP from training future model weights?",
        "weak_answer": "We use OpenAI Enterprise with zero data retention turned on.",
        "strong_answer": "All inference routes through dedicated VPC endpoints with customer-managed encryption keys (CMEK) and zero-day data retention agreements; data in flight never leaves our boundary."
    },
    {
        "domain": "Agentic Tool Execution & Blast Radius",
        "question": "If your agent has write-access to our CRM or ERP, how do you prevent prompt-injection attacks from hallucinating an unintended database update or bulk exfiltration?",
        "weak_answer": "Our system prompt tells the LLM not to delete records.",
        "strong_answer": "Tool execution is sandboxed behind deterministic RBAC policies, read-only defaults, dual-human approval gates on destructive operations, and cryptographic action auditing."
    },
    {
        "domain": "Tenant Isolation & Compliance",
        "question": "Can you provide your SOC2 Type II report, and do you support single-tenant isolation or on-prem deployment for regulated data?",
        "weak_answer": "We're SOC2 compliant in spirit and working on the audit.",
        "strong_answer": "SOC2 Type II report available under mutual NDA, with complete logical database sharding per tenant and optional VPC-peered private deployment."
    }
]

VC_QUESTIONS = [
    {
        "domain": "Defensibility vs Foundation Labs",
        "question": "If OpenAI or Google releases an update next month that does this natively inside their chat UI or OS, why doesn't your business go to zero?",
        "weak_answer": "Our UI is cleaner and we focus on this specific niche.",
        "strong_answer": "Foundation labs build horizontal models, not deep bi-directional enterprise data integrations. Our switching cost is not the model—it's the accumulated context graph, custom workflows, and system-of-record sync that labs cannot replicate."
    },
    {
        "domain": "Gross Margin Collapse Under Scale",
        "question": "As users automate more tasks, your token consumption increases exponentially. How does your unit economics survive without per-seat expansion?",
        "weak_answer": "API prices drop 50% every year, so margins will improve.",
        "strong_answer": "We price on an outcome/work-unit basis that scales directly with customer value capture, while dynamic task routing sends 80% of routine jobs to low-cost specialized SLMs, keeping gross margins above 75%."
    },
    {
        "domain": "Distribution Velocity & CAC Payback",
        "question": "Enterprise sales cycles take 9 months. How do you reach $1M ARR before burning through your seed round?",
        "weak_answer": "We are hiring two enterprise SDRs to do outbound cold outreach.",
        "strong_answer": "We use a bottom-up PLG wedge where individual practitioners adopt free local tools, creating internal power-user champions before procurement is ever engaged."
    }
]

def generate_adversarial_brief(mode, startup_name, output_path=None):
    is_ciso = mode.lower() == "ciso"
    role_title = "Enterprise CISO Security Inquisition" if is_ciso else "Tier-1 VC Partner Stress Test"
    questions = CISO_QUESTIONS if is_ciso else VC_QUESTIONS

    brief = f"""# ADVERSARIAL STRESS TEST: {role_title.upper()}
**Startup Under Audit:** {startup_name}  
**Persona:** {"Fortune 500 Chief Information Security Officer" if is_ciso else "General Partner (Enterprise AI Fund)"}  
**Format:** High-stakes objection handling and defense readiness  

---

"""
    for idx, item in enumerate(questions, 1):
        brief += f"""### Scenario {idx}: {item['domain']}
* **The Brutal Question:**
  > *"{item['question']}"*
* **❌ The Fatal Red Flag Response (Why Deals Die):**
  > "{item['weak_answer']}"
* **✅ The Institutional Defense (Winning Response):**
  > "{item['strong_answer']}"

---
"""

    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(brief)
        print(f"[+] Adversarial Brief generated at: {output_path}", file=sys.stderr)

    return brief

def main():
    parser = argparse.ArgumentParser(description="Generate CISO or VC Adversarial Briefs")
    parser.add_argument("--mode", choices=["ciso", "vc"], default="ciso", help="Adversarial persona mode")
    parser.add_argument("--startup", default="My AI Startup", help="Startup name")
    parser.add_argument("--output", default="adversarial_brief.md", help="Output file path")
    args = parser.parse_args()

    brief = generate_adversarial_brief(args.mode, args.startup, args.output)
    print("\n" + brief)

if __name__ == "__main__":
    main()
