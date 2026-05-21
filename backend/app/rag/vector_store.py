from pathlib import Path


class VectorStoreClient:
    """Placeholder vector store client for future Chroma integration."""

    def __init__(self, db_path: Path):
        self.db_path = db_path

    def upsert(self, chunks: list[dict]) -> int:
        _ = chunks
        return 0

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        _ = (query, top_k)
        return []
