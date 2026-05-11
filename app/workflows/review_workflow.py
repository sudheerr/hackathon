"""End-to-end policy review workflow."""

from uuid import uuid4

from app.audit.repository import AuditRepository
from app.core.tracing import trace_span
from app.domain.audit import ReviewAuditRecord
from app.domain.policy import HomePolicy
from app.domain.review import ReviewResponse
from app.llm.claude_service import ClaudeUnderwritingService
from app.retrieval.interfaces import Retriever
from app.services.trigger_engine import TriggerEngine
from app.validators.review_validator import ReviewValidator


class ReviewWorkflow:
    """Coordinate trigger detection, retrieval, LLM generation, validation, and audit."""

    def __init__(
        self,
        trigger_engine: TriggerEngine,
        retriever: Retriever,
        llm_service: ClaudeUnderwritingService,
        validator: ReviewValidator,
        audit_repository: AuditRepository,
    ) -> None:
        self._trigger_engine = trigger_engine
        self._retriever = retriever
        self._llm_service = llm_service
        self._validator = validator
        self._audit_repository = audit_repository

    async def review_policy(self, policy: HomePolicy, correlation_id: str) -> ReviewResponse:
        """Run the review workflow for a normalized policy."""
        async with trace_span("review_policy", correlation_id):
            triggers = await self._trigger_engine.evaluate(policy)
            trigger_queries = [
                query for trigger in triggers for query in trigger.retrieval_queries
            ]
            retrieval_results = await self._retriever.retrieve_for_policy(
                policy=policy,
                trigger_queries=trigger_queries,
            )
            output = await self._llm_service.generate_review(
                policy=policy,
                triggers=triggers,
                retrieval_results=retrieval_results,
            )
            output = await self._validator.validate(output, retrieval_results)

            audit_record = ReviewAuditRecord(
                audit_id=str(uuid4()),
                policy_id=policy.policy_id,
                correlation_id=correlation_id,
                triggers_fired=triggers,
                retrieved_chunks=retrieval_results,
                prompt_version=self._llm_service.prompt_version,
                model_version=self._llm_service.model_version,
                output_json=output,
            )
            await self._audit_repository.save(audit_record)

            return ReviewResponse(
                policy_id=policy.policy_id,
                correlation_id=correlation_id,
                manual_review_required=output.manual_review_required,
                triggers=triggers,
                retrieval_results=retrieval_results,
                review=output,
            )
