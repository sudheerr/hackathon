"""FastAPI routes."""

from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status

from app.api.dependencies import get_audit_repository, get_review_workflow
from app.audit.repository import AuditRepository
from app.domain.audit import ReviewAuditRecord
from app.domain.policy import HomePolicy
from app.domain.review import ReviewResponse
from app.workflows.review_workflow import ReviewWorkflow

router = APIRouter(tags=["underwriting-review"])


@router.get("/health")
async def health() -> dict[str, str]:
    """Health probe endpoint."""
    return {"status": "ok"}


@router.post("/review-policy", response_model=ReviewResponse)
async def review_policy(
    policy: HomePolicy,
    workflow: ReviewWorkflow = Depends(get_review_workflow),
) -> ReviewResponse:
    """Run a first-pass underwriting review."""
    correlation_id = str(uuid4())
    return await workflow.review_policy(policy=policy, correlation_id=correlation_id)


@router.post("/ingest-guidelines", status_code=status.HTTP_202_ACCEPTED)
async def ingest_guidelines(file: UploadFile) -> dict[str, str]:
    """Accept guideline documents for future offline ingestion."""
    return {
        "status": "accepted",
        "filename": file.filename or "unknown",
        "message": "Ingestion pipeline placeholder accepted the document.",
    }


@router.get("/audit/{policy_id}", response_model=ReviewAuditRecord)
async def get_audit_record(
    policy_id: str,
    repository: AuditRepository = Depends(get_audit_repository),
) -> ReviewAuditRecord:
    """Fetch the latest audit record for a policy."""
    record = await repository.get_latest(policy_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Audit record not found")
    return record
