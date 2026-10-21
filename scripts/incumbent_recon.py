#!/usr/bin/env python3
"""
Incumbent Reconnaissance & Competitor AI Intelligence Tool
Queries recent AI product updates, releases, and changelog announcements
for named incumbents to pressure-test startup novelty.
"""

import sys
import os
import json
import argparse
import urllib.request
import urllib.parse
import re

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def search_incumbent(query, max_results=5):
    """Fetch search snippets via DuckDuckGo HTML/Instant API or fallback."""
    encoded_query = urllib.parse.quote(f"{query} AI agent release announcement 2026")
    url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    results = []
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as response:
            html = response.read().decode('utf-8')
            # Extract basic title and snippet patterns
            snippets = re.findall(r'<a class="result__snippet[^>]*>(.*?)</a>', html, re.DOTALL)
            titles = re.findall(r'<a class="result__url[^>]*>(.*?)</a>', html, re.DOTALL)
            for i in range(min(len(snippets), max_results)):
                clean_snippet = re.sub(r'<[^>]+>', '', snippets[i]).strip()
                results.append({
                    "snippet": clean_snippet,
                    "query": query
                })
    except Exception as e:
        results.append({
            "snippet": f"Could not complete live web search ({str(e)}). Review incumbent roadmap manually.",
            "query": query
        })
    return results

def generate_recon_report(incumbent, product_domain, output_path=None):
    print(f"[*] Running Incumbent Intelligence Recon on: {incumbent} ({product_domain})...")
    findings = search_incumbent(f"{incumbent} {product_domain}")

    report = f"""# INCUMBENT INTELLIGENCE RECON: {incumbent.upper()}

**Target Competitor:** {incumbent}  
**Product Domain:** {product_domain}  
**Assessment Date:** 2026

## 1. Verified Competitive Signals
"""
    if findings:
        for idx, item in enumerate(findings, 1):
            report += f"{idx}. {item['snippet']}\n\n"
    else:
        report += "- No immediate breaking announcements detected in direct search index.\n\n"

    report += f"""## 2. Strategic Pressure Points for Phase 2
* **Feature Parity Trap:** Does your startup assume {incumbent} will remain a static legacy system, or are they already piloting proactive background routines?
* **Distribution Advantage:** {incumbent} controls the existing identity, permissioning, and billing relationship. Your wedge must offer an experience they structurally cannot build without cannibalizing their core model.
* **Defense Recommendation:** Build deep integration bi-directionality with {incumbent} rather than trying to displace their primary record of truth.
"""

    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"[+] Recon report written to: {output_path}")

    return report

def main():
    parser = argparse.ArgumentParser(description="Incumbent Reconnaissance & Threat Assessment")
    parser.add_argument("--incumbent", required=True, help="Name of leading competitor/incumbent (e.g. Salesforce, Notion, Zendesk)")
    parser.add_argument("--domain", default="AI workflow automation", help="Startup product domain")
    parser.add_argument("--output", default="incumbent_recon.md", help="Output report file path")
    args = parser.parse_args()

    report = generate_recon_report(args.incumbent, args.domain, args.output)
    print("\n" + report)

if __name__ == "__main__":
    main()
