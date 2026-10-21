#!/usr/bin/env python3
"""Retrieve unverified competitive search leads with explicit provenance."""
import argparse
from datetime import datetime, timezone
from html import escape
from html.parser import HTMLParser
import os
import sys
import urllib.parse
import urllib.request


class SearchResults(HTMLParser):
    def __init__(self):
        super().__init__()
        self.results = []
        self.current = None
        self.capture = None
        self.text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class", "").split()
        if tag == "a" and "result__a" in classes:
            href = attrs.get("href", "")
            parsed = urllib.parse.urlsplit(href)
            href = urllib.parse.parse_qs(parsed.query).get("uddg", [href])[0]
            if urllib.parse.urlsplit(href).scheme in {"http", "https"}:
                self.current = {"url": href, "title": "", "snippet": ""}
                self.results.append(self.current)
                self.capture, self.text = "title", []
        elif "result__snippet" in classes and self.current:
            self.capture, self.text = "snippet", []

    def handle_data(self, text):
        if self.capture:
            self.text.append(text)

    def handle_endtag(self, tag):
        if self.capture and tag in {"a", "div"}:
            self.current[self.capture] = " ".join("".join(self.text).split())
            self.capture = None


def search_incumbent(query, max_results=5):
    year = datetime.now(timezone.utc).year
    encoded = urllib.parse.quote(f"{query} AI agent release announcement {year}")
    url = f"https://html.duckduckgo.com/html/?q={encoded}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=8) as response:
        raw = response.read(1000001)
    if len(raw) > 1000000:
        raise ValueError("Search response exceeds 1000000 bytes")
    parser = SearchResults()
    parser.feed(raw.decode("utf-8"))
    return [result for result in parser.results if result["title"]][:max_results]


def generate_recon_report(incumbent, product_domain, output_path=None):
    if not isinstance(incumbent, str) or not incumbent.strip():
        raise ValueError("incumbent must be a non-empty string")
    if not isinstance(product_domain, str):
        raise ValueError("product_domain must be a string")
    retrieved_at = datetime.now(timezone.utc).isoformat() + " UTC"
    failure = None
    try:
        findings = search_incumbent(f"{incumbent} {product_domain}")
    except (OSError, ValueError) as exc:
        findings, failure = [], type(exc).__name__
    state = "UNVERIFIED" if findings else "UNAVAILABLE"
    report = (f"# INCUMBENT INTELLIGENCE RECON: {escape(incumbent.upper())}\n\n"
              f"**Product Domain:** {escape(product_domain)}\n\n"
              f"**Retrieved:** {retrieved_at}\n\n"
              f"**Evidence Status:** {state}\n\n"
              "Search snippets are leads, not verified product capabilities. Open the primary "
              "source, record its publication date, and check current applicability before using it.\n\n"
              "## 1. Competitive Search Leads\n\n")
    if failure:
        report += f"Live search failed ({failure}). Competitor capabilities remain unknown.\n\n"
    elif not findings:
        report += "No source-bearing results were parsed; this is not evidence that no announcements exist.\n\n"
    for item in findings:
        url = urllib.parse.quote(item["url"], safe=":/?=&%#")
        report += f"- [{escape(item['title'])}](<{url}>): {escape(item['snippet'])}\n"
    report += ("\n## 2. Strategic Pressure Points for Phase 2\n\n"
               "- Which customer alternatives have comparable capabilities, based on dated primary sources?\n"
               "- What switching reason is supported by customer interviews or observed behavior?\n"
               "- Which experiment would falsify the proposed advantage?\n")
    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as stream:
            stream.write(report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--incumbent", required=True)
    parser.add_argument("--domain", default="AI workflow automation")
    parser.add_argument("--output", default="incumbent_recon.md")
    args = parser.parse_args()
    print(generate_recon_report(args.incumbent, args.domain, args.output))


if __name__ == "__main__":
    main()
