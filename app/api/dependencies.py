"""FastAPI dependency providers."""

from functools import lru_cache

from app.audit.repository import InMemoryAuditRepository
from app.core.config import get_settings
from app.llm.claude_service import ClaudeUnderwritingService
from app.retrieval.in_memory import InMemoryRetriever
from app.services.trigger_engine import TriggerEngine
from app.validators.review_validator import ReviewValidator
from app.workflows.review_workflow import ReviewWorkflow


@lru_cache
def get_trigger_engine() -> TriggerEngine:
    return TriggerEngine.from_file(get_settings().trigger_rules_path)


@lru_cache
def get_retriever() -> InMemoryRetriever:
    return InMemoryRetriever.from_sample_guidelines()


@lru_cache
def get_llm_service() -> ClaudeUnderwritingService:
    return ClaudeUnderwritingService(settings=get_settings())


@lru_cache
def get_audit_repository() -> InMemoryAuditRepository:
    return InMemoryAuditRepository()


def get_review_workflow() -> ReviewWorkflow:
    return ReviewWorkflow(
        trigger_engine=get_trigger_engine(),
        retriever=get_retriever(),
        llm_service=get_llm_service(),
        validator=ReviewValidator(min_retrieval_score=get_settings().retrieval_min_score),
        audit_repository=get_audit_repository(),
    )
