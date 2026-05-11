"""Structured LLM output models."""

from pydantic import BaseModel, Field


class CitationReference(BaseModel):
    """Citation pointing to a retrieved guideline chunk."""

    chunk_id: str
    document_name: str
    section_heading: str
    page_number: int


class ChecklistItem(BaseModel):
    """Underwriting checklist item."""

    item_id: str
    description: str
    required_action: str
    citations: list[CitationReference] = Field(default_factory=list)


class ConcernItem(BaseModel):
    """Underwriting concern that must cite supporting guidance."""

    concern_id: str
    severity: str
    summary: str
    rationale: str
    citations: list[CitationReference] = Field(min_length=1)


class AgentEmail(BaseModel):
    """Draft email to the agent."""

    subject: str
    body: str
    citations: list[CitationReference] = Field(default_factory=list)


class UnderwriterNote(BaseModel):
    """Draft note for underwriter review."""

    summary: str
    recommended_follow_up: list[str] = Field(default_factory=list)
    citations: list[CitationReference] = Field(default_factory=list)


class UnderwritingReviewOutput(BaseModel):
    """Structured review output from the LLM orchestration layer."""

    checklist: list[ChecklistItem] = Field(default_factory=list)
    concerns: list[ConcernItem] = Field(default_factory=list)
    agent_email: AgentEmail
    underwriter_note: UnderwriterNote
    manual_review_required: bool = False
    uncertainty: str | None = None
