"""Policy domain models."""

from datetime import date
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, Field


class StateCode(StrEnum):
    """Supported sample state codes."""

    FL = "FL"
    NY = "NY"
    NJ = "NJ"
    TX = "TX"
    CA = "CA"
    OTHER = "OTHER"


class Applicant(BaseModel):
    """Policy applicant."""

    applicant_id: str
    first_name: str
    last_name: str
    email: str | None = None
    ownership_type: str = Field(default="individual", examples=["individual", "llc", "trust"])


class Coverage(BaseModel):
    """Homeowners coverage details."""

    dwelling_limit: Decimal = Field(ge=0)
    personal_property_limit: Decimal | None = Field(default=None, ge=0)
    liability_limit: Decimal | None = Field(default=None, ge=0)
    deductible: Decimal | None = Field(default=None, ge=0)


class Property(BaseModel):
    """Insured property attributes."""

    address_line1: str
    city: str
    state: StateCode
    postal_code: str
    year_built: int | None = Field(default=None, ge=1600)
    distance_to_coast_miles: float | None = Field(default=None, ge=0)
    rented_to_others: bool = False
    occupancy_type: str = Field(default="primary", examples=["primary", "secondary", "rental"])


class ClaimsHistory(BaseModel):
    """Policy claims history summary."""

    prior_claim_count: int = Field(default=0, ge=0)
    prior_claims_total_amount: Decimal = Field(default=Decimal("0"), ge=0)
    lookback_years: int = Field(default=5, ge=0)


class HomePolicy(BaseModel):
    """Normalized internal homeowners policy model."""

    policy_id: str
    effective_date: date
    applicant: Applicant
    coverage: Coverage
    property: Property
    claims_history: ClaimsHistory = Field(default_factory=ClaimsHistory)
