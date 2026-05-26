"""Agent 02 — Cold Email Writer.

Accepts a ``SignalFeed`` (from Agent 01) and produces a batch of
personalised cold-email drafts, one per top buying signal.

Usage (as a library):
    from agents.cold_email_writer import draft_cold_emails
    from agents.signal_scraper import scan_companies

    feed   = scan_companies(["Citadel", "Two Sigma"])
    batch  = draft_cold_emails(feed)
    print(batch.model_dump_json(indent=2))
"""

from __future__ import annotations

import anthropic

import config
from models.emails import ColdEmail, ColdEmailBatch
from models.signals import BuyingSignal, SignalFeed

SYSTEM_PROMPT = """\
You are an elite B2B sales copywriter for **Numatix**, an algorithmic \
trading platform that helps quantitative hedge funds, prop-trading desks, \
and asset managers automate complex trading strategies, reduce execution \
latency, and improve alpha generation.

Your task: write highly personalised cold-email drafts that convert.

**Numatix value props** (weave in naturally — never list all at once):
- Sub-microsecond order routing with built-in risk controls
- Visual strategy builder — no-code backtesting on tick data
- Seamless connectivity: 40+ prime brokers & exchanges out of the box
- Live P&L attribution and real-time risk dashboards
- SOC-2 Type II certified; co-location available in NY4/LD4/TY3

**Email craft rules**:
1. OPEN with the specific buying signal — make it obvious you did your homework.
2. Bridge from their news/activity to a *concrete pain* it implies.
3. Position Numatix as the natural solution in one punchy sentence.
4. CTA: ask for a 20-minute call, never a demo link as the first ask.
5. Subject line: ≤60 chars, conversational, no ALL-CAPS or spam words.
6. Total body word count: 80-120 words. Tight is right.
7. Tone: peer-to-peer, confident, zero fluff.
"""


def _build_user_message(signals: list[BuyingSignal]) -> str:
    lines = ["Write one cold email for each of the following buying signals:\n"]
    for i, s in enumerate(signals, 1):
        lines.append(
            f"Signal {i}:\n"
            f"  Company:         {s.company}\n"
            f"  Type:            {s.signal_type.value}\n"
            f"  Headline:        {s.headline}\n"
            f"  Source:          {s.source}\n"
            f"  Relevance score: {s.relevance_score}/10\n"
            f"  Reasoning:       {s.reasoning}\n"
        )
    return "\n".join(lines)


def draft_cold_emails(feed: SignalFeed, top_n: int = 5) -> ColdEmailBatch:
    """Draft personalised cold emails for the highest-scored buying signals.

    Args:
        feed:  A ``SignalFeed`` returned by Agent 01.
        top_n: How many top signals to turn into emails (default 5).

    Returns:
        A ``ColdEmailBatch`` with drafts sorted by relevance_score desc.
    """
    signals = sorted(feed.signals, key=lambda s: s.relevance_score, reverse=True)[:top_n]

    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

    response = client.messages.parse(
        model=config.MODEL,
        max_tokens=8192,
        system=SYSTEM_PROMPT,
        thinking={"type": "adaptive"},
        messages=[{"role": "user", "content": _build_user_message(signals)}],
        output_format=ColdEmailBatch,
    )

    batch: ColdEmailBatch = response.parsed_output
    batch.emails.sort(key=lambda e: e.relevance_score, reverse=True)
    return batch
