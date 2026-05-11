"""Retrieval domain models."""

from datetime import date

from pydantic import BaseModel, Field


class GuidelineMetadata(BaseModel):
    """Metadata needed for citation traceability and filtering."""

    document_name: str
    version: str
    section_heading: str
    page_number: int = Field(ge=1)
    state_applicability: list[str] = Field(default_factory=list)
    line_of_business: str
    effective_date: date | None = None
    expiration_date: date | None = None
    rule_category: str


class GuidelineChunk(BaseModel):
    """Retrieved guideline text chunk."""

    chunk_id: str
    text: str
    metadata: GuidelineMetadata


class RetrievalResult(BaseModel):
    """Search result with relevance score."""

    chunk: GuidelineChunk
    score: float = Field(ge=0, le=1)
    match_reason: str
