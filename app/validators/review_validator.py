"""Post-generation review validation."""

from app.domain.llm_outputs import UnderwritingReviewOutput
from app.domain.retrieval import RetrievalResult


class ReviewValidator:
    """Validate generated underwriting review artifacts."""

    def __init__(self, min_retrieval_score: float) -> None:
        self._min_retrieval_score = min_retrieval_score

    async def validate(
        self,
        output: UnderwritingReviewOutput,
        retrieval_results: list[RetrievalResult],
    ) -> UnderwritingReviewOutput:
        """Enforce citation and retrieval confidence requirements."""
        if not retrieval_results or all(
            result.score < self._min_retrieval_score for result in retrieval_results
        ):
            return output.model_copy(
                update={
                    "manual_review_required": True,
                    "uncertainty": "Manual review required: guideline retrieval confidence is low.",
                }
            )

        allowed_chunk_ids = {result.chunk.chunk_id for result in retrieval_results}
        for concern in output.concerns:
            if not concern.citations:
                raise ValueError(f"Concern {concern.concern_id} is missing citations.")
            unsupported = [
                citation.chunk_id
                for citation in concern.citations
                if citation.chunk_id not in allowed_chunk_ids
            ]
            if unsupported:
                raise ValueError(
                    f"Concern {concern.concern_id} cites unsupported chunks: {unsupported}"
                )
        return output
