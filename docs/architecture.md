# Architecture Overview

## Phase 1 Foundation
- **Frontend**: Streamlit UI for document upload and Q&A.
- **Backend**: FastAPI service exposing `/health`, `/upload`, and `/chat`.
- **RAG Layer (Placeholder)**: Modular components for document loading, chunking, vector storage, and answer generation.
- **Data Layer**: Local knowledge base directory and sample support tickets.

## Planned Evolution
- Add production-grade vector indexing with Chroma.
- Integrate OpenAI models for retrieval-augmented responses.
- Add voice processing, sentiment analysis, and ticket automation workflows.
