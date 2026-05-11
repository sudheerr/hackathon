"""In-memory retriever for local POC execution."""

from datetime import date

from app.domain.policy import HomePolicy
from app.domain.retrieval import GuidelineChunk, GuidelineMetadata, RetrievalResult
from app.retrieval.interfaces import Retriever


class InMemoryRetriever(Retriever):
    """Simple keyword retriever with deterministic scoring for the POC."""

    def __init__(self, chunks: list[GuidelineChunk]) -> None:
        self._chunks = chunks

    @classmethod
    def from_sample_guidelines(cls) -> "InMemoryRetriever":
        """Create retriever with embedded mock guideline chunks."""
        chunks = [
            GuidelineChunk(
                chunk_id="uw-home-001",
                text=(
                    "Properties rented to others require rental exposure review, confirmation "
                    "of occupancy, and underwriting approval before binding."
                ),
                metadata=GuidelineMetadata(
                    document_name="Homeowners Underwriting Guide",
                    version="2026.01",
                    section_heading="Rental Exposure",
                    page_number=12,
                    state_applicability=["FL", "NY", "NJ", "TX", "CA"],
                    line_of_business="homeowners",
                    effective_date=date(2026, 1, 1),
                    rule_category="occupancy",
                ),
            ),
            GuidelineChunk(
                chunk_id="uw-home-002",
                text=(
                    "Entity-owned risks such as LLCs or trusts must be reviewed for insurable "
                    "interest, named insured accuracy, and ownership documentation."
                ),
                metadata=GuidelineMetadata(
                    document_name="Homeowners Underwriting Guide",
                    version="2026.01",
                    section_heading="Ownership Requirements",
                    page_number=18,
                    state_applicability=["FL", "NY", "NJ", "TX", "CA"],
                    line_of_business="homeowners",
                    effective_date=date(2026, 1, 1),
                    rule_category="ownership",
                ),
            ),
            GuidelineChunk(
                chunk_id="uw-home-003",
                text=(
                    "Dwelling limits at or above 1,000,000 require high value home review, "
                    "replacement cost support, and senior underwriter sign-off."
                ),
                metadata=GuidelineMetadata(
                    document_name="High Value Home Guidelines",
                    version="2026.01",
                    section_heading="Dwelling Limit Thresholds",
                    page_number=4,
                    state_applicability=["FL", "NY", "NJ", "TX", "CA"],
                    line_of_business="homeowners",
                    effective_date=date(2026, 1, 1),
                    rule_category="coverage",
                ),
            ),
            GuidelineChunk(
                chunk_id="uw-home-004",
                text=(
                    "Homes within 5 miles of the coastline require coastal exposure review, "
                    "wind eligibility confirmation, and catastrophe modeling where applicable."
                ),
                metadata=GuidelineMetadata(
                    document_name="Coastal Property Guidelines",
                    version="2026.01",
                    section_heading="Coastal Exposure",
                    page_number=7,
                    state_applicability=["FL", "NJ", "TX", "CA"],
                    line_of_business="homeowners",
                    effective_date=date(2026, 1, 1),
                    rule_category="catastrophe",
                ),
            ),
            GuidelineChunk(
                chunk_id="uw-home-005",
                text=(
                    "Two or more prior claims in the lookback period require claims history "
                    "review, loss details, and evidence of mitigation."
                ),
                metadata=GuidelineMetadata(
                    document_name="Claims Review Guidelines",
                    version="2026.01",
                    section_heading="Prior Claims",
                    page_number=9,
                    state_applicability=["FL", "NY", "NJ", "TX", "CA"],
                    line_of_business="homeowners",
                    effective_date=date(2026, 1, 1),
                    rule_category="claims",
                ),
            ),
        ]
        return cls(chunks)

    async def retrieve_for_policy(
        self,
        policy: HomePolicy,
        trigger_queries: list[str],
        limit: int = 5,
    ) -> list[RetrievalResult]:
        """Retrieve chunks using state filtering and keyword overlap."""
        query_text = " ".join(trigger_queries).lower()
        results: list[RetrievalResult] = []
        for chunk in self._chunks:
            if not self._is_applicable_to_state(chunk, policy.property.state.value):
                continue
            score = self._score(query_text, chunk)
            if score > 0:
                results.append(
                    RetrievalResult(
                        chunk=chunk,
                        score=min(score, 1.0),
                        match_reason="keyword_overlap",
                    )
                )
        return sorted(results, key=lambda item: item.score, reverse=True)[:limit]

    def _is_applicable_to_state(self, chunk: GuidelineChunk, state: str) -> bool:
        return not chunk.metadata.state_applicability or state in chunk.metadata.state_applicability

    def _score(self, query_text: str, chunk: GuidelineChunk) -> float:
        terms = {term for term in query_text.replace(",", " ").split() if len(term) > 3}
        if not terms:
            return 0
        chunk_text = f"{chunk.metadata.rule_category} {chunk.metadata.section_heading} {chunk.text}".lower()
        matches = sum(1 for term in terms if term in chunk_text)
        return matches / max(len(terms), 1)
