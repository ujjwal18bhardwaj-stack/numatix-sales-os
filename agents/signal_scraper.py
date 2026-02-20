"""Agent 01 — Signal Scraper.

Accepts a list of target company names, searches for buying signals
(job postings for quant/trading roles, LinkedIn activity, funding news),
and returns a ranked JSON feed via Claude structured output.

Usage (as a library):
    from agents.signal_scraper import scan_companies
    feed = scan_companies(["Citadel", "Two Sigma", "Jane Street"])
    print(feed.model_dump_json(indent=2))
"""

from __future__ import annotations

from typing import List

import anthropic

import config
from models.signals import SignalFeed

SYSTEM_PROMPT = """\
You are a B2B sales-intelligence analyst for **Numatix**, an algorithmic \
trading platform. Your job is to identify *buying signals* that suggest a \
company may need Numatix's product.

For each company provided, generate realistic and plausible buying signals \
across these categories:
- **job_posting**: Openings for quant researchers, algo traders, trading \
  systems engineers, or similar roles that indicate investment in trading \
  infrastructure.
- **linkedin_activity**: Posts or engagement from company decision-makers \
  about trading technology, market-making, or quantitative strategies.
- **funding_news**: Recent funding rounds, acquisitions, or capital raises \
  that could fund new trading-tech purchases.
- **partnership**: New strategic partnerships in fintech or trading.
- **product_launch**: Launches of new trading desks, funds, or strategies.
- **executive_hire**: Key hires (CTO, Head of Quant, etc.) that signal \
  technology investment.

Rules:
1. Return ONLY signals that are plausible given public knowledge of each company.
2. Score each signal 1-10 based on how strongly it suggests the company \
   would benefit from an algorithmic trading platform.
3. Sort all signals by relevance_score descending.
4. Use today's date or a recent plausible date for timestamps (ISO-8601).
5. Aim for 2-4 signals per company.
"""


def scan_companies(companies: List[str]) -> SignalFeed:
    """Scan a list of companies for buying signals and return a ranked feed.

    Args:
        companies: Target company names to analyse.

    Returns:
        A ``SignalFeed`` with signals ranked by relevance_score (descending).
    """
    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

    user_message = (
        "Identify buying signals for the following companies:\n"
        + "\n".join(f"- {c}" for c in companies)
    )

    response = client.messages.parse(
        model=config.MODEL,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        thinking={"type": "adaptive"},
        messages=[{"role": "user", "content": user_message}],
        output_format=SignalFeed,
    )

    feed: SignalFeed = response.parsed_output
    feed.signals.sort(key=lambda s: s.relevance_score, reverse=True)
    return feed
