"""Audit repository abstractions."""

from abc import ABC, abstractmethod

from app.domain.audit import ReviewAuditRecord


class AuditRepository(ABC):
    """Audit persistence abstraction."""

    @abstractmethod
    async def save(self, record: ReviewAuditRecord) -> None:
        """Persist an audit record."""

    @abstractmethod
    async def get_latest(self, policy_id: str) -> ReviewAuditRecord | None:
        """Fetch latest audit record for a policy."""


class InMemoryAuditRepository(AuditRepository):
    """In-memory audit repository for local POC use."""

    def __init__(self) -> None:
        self._records: dict[str, list[ReviewAuditRecord]] = {}

    async def save(self, record: ReviewAuditRecord) -> None:
        self._records.setdefault(record.policy_id, []).append(record)

    async def get_latest(self, policy_id: str) -> ReviewAuditRecord | None:
        records = self._records.get(policy_id, [])
        return records[-1] if records else None
