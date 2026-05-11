"""Audit models."""

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field

from app.domain.llm_outputs import UnderwritingReviewOutput
from app.domain.retrieval import RetrievalResult
from app.domain.triggers import TriggerResult


class ReviewAuditRecord(BaseModel):
    """Audit record for one underwriting review workflow run."""

    audit_id: str
    policy_id: str
    correlation_id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    triggers_fired: list[TriggerResult]
    retrieved_chunks: list[RetrievalResult]
    prompt_version: str
    model_version: str
    output_json: UnderwritingReviewOutput
    reviewer_actions: list[dict[str, Any]] = Field(default_factory=list)
