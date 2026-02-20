"""Pydantic models for buying signals used across all agents."""

from __future__ import annotations

from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class SignalType(str, Enum):
    JOB_POSTING = "job_posting"
    LINKEDIN_ACTIVITY = "linkedin_activity"
    FUNDING_NEWS = "funding_news"
    PARTNERSHIP = "partnership"
    PRODUCT_LAUNCH = "product_launch"
    EXECUTIVE_HIRE = "executive_hire"


class BuyingSignal(BaseModel):
    """A single buying signal detected for a company."""

    company: str = Field(description="Company name")
    signal_type: SignalType = Field(description="Category of buying signal")
    headline: str = Field(description="Short description of the signal")
    source: str = Field(
        description="Where this signal was observed, e.g. LinkedIn, job board URL, news outlet"
    )
    relevance_score: int = Field(
        ge=1,
        le=10,
        description="1-10 score of how relevant this signal is for selling an algorithmic trading platform",
    )
    reasoning: str = Field(
        description="Why this signal suggests buying intent for a quant/trading platform"
    )
    timestamp: str = Field(
        description="ISO-8601 date or date-time when the signal was observed or published"
    )


class SignalFeed(BaseModel):
    """Ranked feed of buying signals returned by Agent 01."""

    signals: List[BuyingSignal] = Field(
        description="Buying signals sorted by relevance_score descending"
    )
