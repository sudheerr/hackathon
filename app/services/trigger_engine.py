"""Deterministic metadata-driven trigger engine."""

import json
from decimal import Decimal
from pathlib import Path
from typing import Any

from app.domain.policy import HomePolicy
from app.domain.triggers import RuleTrigger, TriggerResult


class TriggerEngine:
    """Evaluate configured trigger rules against normalized policy data."""

    def __init__(self, rules: list[RuleTrigger]) -> None:
        self._rules = rules

    @classmethod
    def from_file(cls, path: Path) -> "TriggerEngine":
        """Load trigger rules from JSON configuration."""
        with path.open(encoding="utf-8") as handle:
            raw_rules = json.load(handle)
        return cls([RuleTrigger.model_validate(rule) for rule in raw_rules])

    async def evaluate(self, policy: HomePolicy) -> list[TriggerResult]:
        """Evaluate all configured rules against a policy."""
        results: list[TriggerResult] = []
        policy_data = policy.model_dump(mode="json")
        for rule in self._rules:
            observed_value = self._resolve_path(policy_data, rule.field_path)
            if self._matches(observed_value, rule.operator, rule.value):
                results.append(
                    TriggerResult(
                        rule_id=rule.rule_id,
                        trigger_code=rule.trigger_code,
                        severity=rule.severity,
                        category=rule.category,
                        description=rule.description,
                        observed_value=observed_value,
                        retrieval_queries=rule.retrieval_queries,
                    )
                )
        return results

    def _resolve_path(self, payload: dict[str, Any], field_path: str) -> Any:
        current: Any = payload
        for part in field_path.split("."):
            if not isinstance(current, dict):
                return None
            current = current.get(part)
        return current

    def _matches(self, observed_value: Any, operator: str, expected_value: Any) -> bool:
        if observed_value is None:
            return False
        observed = self._normalize_number(observed_value)
        expected = self._normalize_number(expected_value)
        if operator == "equals":
            return observed == expected
        if operator == "in":
            return str(observed).lower() in {str(item).lower() for item in expected_value}
        if operator == "greater_than_or_equal":
            return Decimal(str(observed)) >= Decimal(str(expected))
        if operator == "less_than_or_equal":
            return Decimal(str(observed)) <= Decimal(str(expected))
        raise ValueError(f"Unsupported trigger operator: {operator}")

    def _normalize_number(self, value: Any) -> Any:
        if isinstance(value, bool):
            return value
        if isinstance(value, float | int | Decimal):
            return Decimal(str(value))
        return value
