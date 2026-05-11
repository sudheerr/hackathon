"""Deterministic underwriting trigger models."""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class TriggerSeverity(StrEnum):
    """Trigger severity."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class RuleTrigger(BaseModel):
    """Metadata-driven trigger rule."""

    rule_id: str
    description: str
    field_path: str
    operator: str
    value: Any
    trigger_code: str
    severity: TriggerSeverity
    category: str
    retrieval_queries: list[str] = Field(default_factory=list)


class TriggerResult(BaseModel):
    """Result of evaluating one triggered rule."""

    rule_id: str
    trigger_code: str
    severity: TriggerSeverity
    category: str
    description: str
    observed_value: Any
    retrieval_queries: list[str] = Field(default_factory=list)
