def split_documents(documents: list[dict], chunk_size: int = 500) -> list[dict]:
    """Placeholder text splitting logic for future semantic chunking."""
    chunks: list[dict] = []
    for document in documents:
        chunks.append(
            {
                "source": document.get("path", "unknown"),
                "chunk": document.get("content", "")[:chunk_size],
            }
        )
    return chunks
