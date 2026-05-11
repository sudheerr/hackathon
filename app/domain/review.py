"""API review request and response models."""

from pydantic import BaseModel

from app.domain.llm_outputs import UnderwritingReviewOutput
from app.domain.retrieval import RetrievalResult
from app.domain.triggers import TriggerResult


class ReviewResponse(BaseModel):
    """Structured API response returned to the UI."""

    policy_id: str
    correlation_id: str
    manual_review_required: bool
    triggers: list[TriggerResult]
    retrieval_results: list[RetrievalResult]
    review: UnderwritingReviewOutput
