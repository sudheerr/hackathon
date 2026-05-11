"""Sample ingestion CLI placeholder."""

import argparse
import asyncio
from pathlib import Path


async def ingest_document(path: Path) -> None:
    """Placeholder for extraction, chunking, embedding, and vector indexing."""
    if not path.exists():
        raise FileNotFoundError(path)
    print(f"Accepted guideline document for ingestion: {path}")
    print("Next steps: extract text, chunk with metadata, embed, and upsert to vector store.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest underwriting guideline documents.")
    parser.add_argument("path", type=Path, help="Path to a PDF or DOCX guideline document.")
    args = parser.parse_args()
    asyncio.run(ingest_document(args.path))


if __name__ == "__main__":
    main()
