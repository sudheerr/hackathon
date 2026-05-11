"""Review workflow smoke tests."""

from pathlib import Path

import pytest

from app.audit.repository import InMemoryAuditRepository
from app.core.config import Settings
from app.domain.policy import HomePolicy
from app.llm.claude_service import ClaudeUnderwritingService
from app.retrieval.in_memory import InMemoryRetriever
from app.services.trigger_engine import TriggerEngine
from app.validators.review_validator import ReviewValidator
from app.workflows.review_workflow import ReviewWorkflow


@pytest.mark.asyncio
async def test_review_workflow_returns_cited_concerns() -> None:
    policy = HomePolicy.model_validate_json(
        Path("sample_data/policies/high_risk_home_policy.json").read_text(encoding="utf-8")
    )
    workflow = ReviewWorkflow(
        trigger_engine=TriggerEngine.from_file(Path("config/trigger_rules.json")),
        retriever=InMemoryRetriever.from_sample_guidelines(),
        llm_service=ClaudeUnderwritingService(settings=Settings()),
        validator=ReviewValidator(min_retrieval_score=0.1),
        audit_repository=InMemoryAuditRepository(),
    )

    response = await workflow.review_policy(policy, correlation_id="test-correlation")

    assert response.manual_review_required is True
    assert response.review.concerns
    assert all(concern.citations for concern in response.review.concerns)
