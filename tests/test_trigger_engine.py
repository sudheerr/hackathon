"""Trigger engine tests."""

from pathlib import Path

import pytest

from app.domain.policy import Applicant, Coverage, HomePolicy, Property
from app.services.trigger_engine import TriggerEngine


@pytest.mark.asyncio
async def test_trigger_engine_detects_configured_rules() -> None:
    engine = TriggerEngine.from_file(Path("config/trigger_rules.json"))
    policy = HomePolicy(
        policy_id="test",
        effective_date="2026-06-01",
        applicant=Applicant(
            applicant_id="app",
            first_name="A",
            last_name="B",
            ownership_type="llc",
        ),
        coverage=Coverage(dwelling_limit=1_250_000),
        property=Property(
            address_line1="1 Main",
            city="Naples",
            state="FL",
            postal_code="34102",
            rented_to_others=True,
            distance_to_coast_miles=2.5,
        ),
    )

    results = await engine.evaluate(policy)

    assert {result.trigger_code for result in results} >= {
        "RENTAL_EXPOSURE",
        "ENTITY_OWNERSHIP",
        "DWELLING_LIMIT_THRESHOLD",
        "COASTAL_EXPOSURE",
    }
