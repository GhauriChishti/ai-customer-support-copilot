from backend.app.rag.vector_store import VectorStoreClient


def generate_answer(question: str, vector_store: VectorStoreClient) -> dict:
    """Placeholder RAG chain for future LLM + retrieval orchestration."""
    _ = vector_store.search(question)
    return {
        "answer": "This is a placeholder response. RAG answer generation will be implemented in Phase 1.",
        "sources": ["citation-placeholder"],
    }
