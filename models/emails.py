"""Pydantic models for cold email drafts produced by Agent 02."""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class ColdEmail(BaseModel):
    """A single personalised cold-email draft."""

    company: str = Field(description="Target company name")
    recipient_title: str = Field(
        description="Job title / persona this email is addressed to, e.g. 'Head of Quant Research'"
    )
    subject: str = Field(description="Email subject line (≤60 chars, no spam triggers)")
    body: str = Field(
        description=(
            "Plain-text email body. "
            "Opening line references the specific buying signal. "
            "2-3 short paragraphs. "
            "Clear call-to-action in the last line."
        )
    )
    signal_used: str = Field(
        description="The headline of the buying signal that personalises this email"
    )
    relevance_score: int = Field(
        ge=1,
        le=10,
        description="Inherited relevance score from the source buying signal",
    )
    follow_up_angle: Optional[str] = Field(
        default=None,
        description="One-sentence idea for a follow-up if there is no reply within 5 days",
    )


class ColdEmailBatch(BaseModel):
    """Batch of cold-email drafts produced from a signal feed."""

    emails: List[ColdEmail] = Field(
        description="Cold-email drafts sorted by relevance_score descending"
    )
