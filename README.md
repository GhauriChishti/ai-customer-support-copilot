# AI Customer Support Copilot

## Project Summary
A commercial-ready project skeleton for an AI-powered customer support copilot using Retrieval-Augmented Generation (RAG), with planned voice support, sentiment analysis, and ticket automation.

## Business Problem
Support teams handle repetitive queries and context-switching across large knowledge bases, causing slower response times and inconsistent service quality.

## Solution
This project provides a modular backend + frontend baseline to ingest support knowledge, answer agent questions, and scale into advanced automation capabilities.

## Features
- FastAPI backend with health, upload, and chat endpoints.
- Streamlit frontend for file upload and Q&A.
- Modular RAG package for loader, splitter, vector store, and chain orchestration.
- Placeholder docs and portfolio-ready collateral.

## Architecture
See `docs/architecture.md` for system design and roadmap.

## Tech Stack
- Python
- FastAPI
- Streamlit
- LangChain
- ChromaDB
- OpenAI (planned integration)

## Setup
```bash
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload
streamlit run frontend/streamlit_app.py
```

## API Endpoints
- `GET /health`
- `POST /upload`
- `POST /chat`

## Demo Video Placeholder
_Add demo video link here._

## Future Roadmap
- Complete RAG implementation with embeddings and retrieval.
- Add voice interaction pipeline.
- Add sentiment detection in chat/tickets.
- Implement ticket triage and automation workflows.
