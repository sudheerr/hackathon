"""Claude orchestration service skeleton."""

import logging

from app.core.config import Settings
from app.domain.llm_outputs import (
    AgentEmail,
    ChecklistItem,
    CitationReference,
    ConcernItem,
    UnderwriterNote,
    UnderwritingReviewOutput,
)
from app.domain.policy import HomePolicy
from app.domain.retrieval import RetrievalResult
from app.domain.triggers import TriggerResult

logger = logging.getLogger(__name__)

PROMPT_VERSION = "underwriting-review-v0.1"


class ClaudeUnderwritingService:
    """Generate structured underwriting artifacts from retrieved evidence."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    @property
    def model_version(self) -> str:
        return self._settings.claude_model

    @property
    def prompt_version(self) -> str:
        return PROMPT_VERSION

    async def generate_review(
        self,
        policy: HomePolicy,
        triggers: list[TriggerResult],
        retrieval_results: list[RetrievalResult],
    ) -> UnderwritingReviewOutput:
        """Generate a structured underwriting review.

        The POC returns deterministic structured output when no Anthropic key is configured.
        A production implementation should call Claude with JSON schema/tool output and validate
        the response with the same Pydantic model.
        """
        if not self._settings.anthropic_api_key:
            logger.info("anthropic_key_missing_using_deterministic_poc_output")
            return self._generate_deterministic_poc_output(policy, triggers, retrieval_results)

        return self._generate_deterministic_poc_output(policy, triggers, retrieval_results)

    def _generate_deterministic_poc_output(
        self,
        policy: HomePolicy,
        triggers: list[TriggerResult],
        retrieval_results: list[RetrievalResult],
    ) -> UnderwritingReviewOutput:
        citations = [self._citation_from_result(result) for result in retrieval_results]
        checklist = [
            ChecklistItem(
                item_id=f"check-{trigger.trigger_code.lower()}",
                description=f"Review {trigger.description}",
                required_action=f"Validate requirements for {trigger.trigger_code}.",
                citations=citations_for_category(trigger.category, retrieval_results),
            )
            for trigger in triggers
        ]
        concerns = [
            ConcernItem(
                concern_id=f"concern-{trigger.trigger_code.lower()}",
                severity=trigger.severity.value,
                summary=trigger.description,
                rationale=(
                    "A deterministic trigger fired and retrieved underwriting guidance supports "
                    "human review before any underwriting action."
                ),
                citations=citations_for_category(trigger.category, retrieval_results) or citations[:1],
            )
            for trigger in triggers
            if citations_for_category(trigger.category, retrieval_results) or citations
        ]

        return UnderwritingReviewOutput(
            checklist=checklist,
            concerns=concerns,
            agent_email=AgentEmail(
                subject=f"Additional information requested for policy {policy.policy_id}",
                body=(
                    "Please provide the requested underwriting information so the submission "
                    "can be reviewed by an underwriter."
                ),
                citations=citations,
            ),
            underwriter_note=UnderwriterNote(
                summary=(
                    "First-pass review completed. Deterministic triggers and retrieved "
                    "guidelines indicate that human underwriting review is required."
                ),
                recommended_follow_up=[item.required_action for item in checklist],
                citations=citations,
            ),
            manual_review_required=bool(triggers),
            uncertainty=None if retrieval_results else "No relevant guideline citations were retrieved.",
        )

    def _citation_from_result(self, result: RetrievalResult) -> CitationReference:
        metadata = result.chunk.metadata
        return CitationReference(
            chunk_id=result.chunk.chunk_id,
            document_name=metadata.document_name,
            section_heading=metadata.section_heading,
            page_number=metadata.page_number,
        )


def citations_for_category(
    category: str,
    retrieval_results: list[RetrievalResult],
) -> list[CitationReference]:
    """Build citations for a rule category."""
    citations: list[CitationReference] = []
    for result in retrieval_results:
        if result.chunk.metadata.rule_category == category:
            metadata = result.chunk.metadata
            citations.append(
                CitationReference(
                    chunk_id=result.chunk.chunk_id,
                    document_name=metadata.document_name,
                    section_heading=metadata.section_heading,
                    page_number=metadata.page_number,
                )
            )
    return citations
