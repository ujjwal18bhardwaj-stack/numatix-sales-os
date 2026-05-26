#!/usr/bin/env python3
"""Numatix Sales OS — CLI for Agent 02 (Cold Email Writer).

Chains Agent 01 (Signal Scraper) → Agent 02 (Cold Email Writer).

Usage:
    python cold_email.py Citadel "Two Sigma" "Jane Street"
    python cold_email.py --top 3 Citadel "Jane Street" -o emails.json
"""

import argparse
import json
import sys

from agents.signal_scraper import scan_companies
from agents.cold_email_writer import draft_cold_emails


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Agent 02: Generate cold emails from company buying signals"
    )
    parser.add_argument(
        "companies",
        nargs="+",
        help="One or more target company names",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=5,
        metavar="N",
        help="Number of top signals to turn into emails (default: 5)",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Write JSON output to a file instead of stdout",
    )
    args = parser.parse_args()

    print(f"[1/2] Scanning signals for: {', '.join(args.companies)} …", file=sys.stderr)
    feed = scan_companies(args.companies)
    print(f"      Found {len(feed.signals)} signals.", file=sys.stderr)

    print(f"[2/2] Drafting cold emails for top {args.top} signals …", file=sys.stderr)
    batch = draft_cold_emails(feed, top_n=args.top)
    print(f"      Generated {len(batch.emails)} email drafts.", file=sys.stderr)

    payload = json.loads(batch.model_dump_json(indent=2))
    output = json.dumps(payload, indent=2)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output + "\n")
        print(f"Wrote {len(batch.emails)} emails to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
