#!/usr/bin/env python3
"""Numatix Sales OS — CLI entry point for Agent 01 (Signal Scraper)."""

import argparse
import json
import sys

from agents.signal_scraper import scan_companies


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Agent 01: Scan companies for buying signals"
    )
    parser.add_argument(
        "companies",
        nargs="+",
        help="One or more target company names to scan",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Write JSON output to a file instead of stdout",
    )
    args = parser.parse_args()

    feed = scan_companies(args.companies)
    payload = json.loads(feed.model_dump_json(indent=2))
    output = json.dumps(payload, indent=2)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output + "\n")
        print(f"Wrote {len(feed.signals)} signals to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
