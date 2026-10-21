#!/usr/bin/env python3
"""
Executable GTM Runbook Export Tool
Converts Socratic GTM Playbook recommendations into import-ready issue backlogs
for Linear, Jira, GitHub Issues, and Notion.
"""

import sys
import os
import csv
import json
import argparse

DEFAULT_ISSUES = [
    {
        "Title": "[Sprint 0 - Telemetry] Instrument Magic Moment Timestamp",
        "Milestone": "Sprint 0 (The Wedge)",
        "Priority": "Urgent",
        "Estimate": "3",
        "Description": "Instrument product telemetry to measure the exact timestamp when a user experiences the primary value proposition. Must trigger within 90s of onboarding.",
        "Acceptance Criteria": "1. Telemetry event `magic_moment_reached` fired with latency property.\n2. Dashboard displays median time-to-value across new signups."
    },
    {
        "Title": "[Sprint 0 - PLG] Remove Pre-Signup Corporate Email Barrier",
        "Milestone": "Sprint 0 (The Wedge)",
        "Priority": "High",
        "Estimate": "2",
        "Description": "Ensure individual practitioners can pilot the tool without IT/CISO approval or corporate domain restrictions.",
        "Acceptance Criteria": "1. Social/Google auth enabled.\n2. No mandatory credit card or enterprise contract required for core initial wedge."
    },
    {
        "Title": "[Sprint 1 - Routine] Implement Background Asynchronous Cron Task",
        "Milestone": "Sprint 1 (The Routine)",
        "Priority": "High",
        "Estimate": "5",
        "Description": "Shift UX from a reactive text box to an automated background routine that proactively scans and surfaces ROI alerts via Slack/email.",
        "Acceptance Criteria": "1. Scheduled worker executes low-cost background audits.\n2. High-value summary notification generated without user manual prompting."
    },
    {
        "Title": "[Sprint 1 - Gravity] Build Bi-Directional Webhook Sync",
        "Milestone": "Sprint 1 (The Routine)",
        "Priority": "High",
        "Estimate": "5",
        "Description": "Build bi-directional read/write sync with primary customer system of record (HubSpot, Salesforce, GitHub, or Postgres).",
        "Acceptance Criteria": "1. Two-way sync verified.\n2. Deleting the startup app creates noticeable data workflow disruption (high switching barrier)."
    },
    {
        "Title": "[Sprint 2 - Pricing] Implement Hybrid Task/Outcome Metering",
        "Milestone": "Sprint 2 (The Scale)",
        "Priority": "Medium",
        "Estimate": "5",
        "Description": "Transition billing engine from legacy per-seat tiers to base platform fee + metered task credits to prevent AI labor margin cannibalization.",
        "Acceptance Criteria": "1. Stripe/Lago integration meters executed agent work units.\n2. Automatic overage alerts trigger when usage approaches credit ceilings."
    },
    {
        "Title": "[Sprint 2 - Defense] Multi-Model Router & CMEK Memory Layer",
        "Milestone": "Sprint 2 (The Scale)",
        "Priority": "Medium",
        "Estimate": "8",
        "Description": "Abstract foundation model calls behind a dynamic fallback router; ensure customer contextual data is encrypted with customer-controlled keys.",
        "Acceptance Criteria": "1. System can swap between Claude, GPT, and local SLMs via config flag.\n2. Zero customer training data leakage guarantee audited."
    }
]

def export_issues(issues, output_csv="gtm_sprint_issues.csv", output_json="gtm_sprint_issues.json"):
    os.makedirs(os.path.dirname(os.path.abspath(output_csv)), exist_ok=True)
    
    # Export CSV
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["Title", "Milestone", "Priority", "Estimate", "Description", "Acceptance Criteria"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for issue in issues:
            writer.writerow(issue)
    print(f"[+] Linear/Jira CSV exported to: {output_csv}", file=sys.stderr)

    # Export JSON
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(issues, f, indent=2)
    print(f"[+] JSON backlog exported to: {output_json}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Export GTM Runbook Issues")
    parser.add_argument("--csv", default="gtm_sprint_issues.csv", help="Output CSV path")
    parser.add_argument("--json", default="gtm_sprint_issues.json", help="Output JSON path")
    args = parser.parse_args()

    export_issues(DEFAULT_ISSUES, args.csv, args.json)

if __name__ == "__main__":
    main()
