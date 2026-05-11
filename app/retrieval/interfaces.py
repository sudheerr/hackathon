"""Retrieval abstraction interfaces."""

from abc import ABC, abstractmethod

from app.domain.policy import HomePolicy
from app.domain.retrieval import GuidelineChunk, RetrievalResult


class EmbeddingProvider(ABC):
    """Provider abstraction for embedding generation."""

    @abstractmethod
    async def embed(self, texts: list[str]) -> list[list[float]]:
        """Return embeddings for text inputs."""


class VectorStore(ABC):
    """Vector store abstraction to avoid coupling to CosmosDB."""

    @abstractmethod
    async def upsert_chunks(self, chunks: list[GuidelineChunk], vectors: list[list[float]]) -> None:
        """Store guideline chunks and vectors."""

    @abstractmethod
    async def similarity_search(
        self,
        query_vector: list[float],
        filters: dict[str, str] | None = None,
        limit: int = 5,
    ) -> list[RetrievalResult]:
        """Search for semantically similar guideline chunks."""


class Retriever(ABC):
    """High-level hybrid retrieval interface."""

    @abstractmethod
    async def retrieve_for_policy(
        self,
        policy: HomePolicy,
        trigger_queries: list[str],
        limit: int = 5,
    ) -> list[RetrievalResult]:
        """Retrieve guideline chunks relevant to policy triggers."""
