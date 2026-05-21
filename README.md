# AI Customer Support Copilot

## Project Summary
A commercial-ready project skeleton for an AI-powered customer support copilot using Retrieval-Augmented Generation (RAG), now with Phase 2 ticket intelligence for support triage and escalation.

## Business Problem
Support teams handle repetitive queries and context-switching across large knowledge bases, causing slower response times and inconsistent service quality.

## Solution
This project provides a modular backend + frontend baseline to ingest support knowledge, answer agent questions, classify support tickets, detect sentiment/urgency, and decide human escalation.

## Features
- FastAPI backend with health, upload, chat, and ticket intelligence endpoints.
- Streamlit frontend for file upload, Q&A, and ticket intelligence analysis.
- Ticket intelligence engine with:
  - category classification (Billing, Technical Support, Refund, Delivery, Product Question, Complaint, General Query)
  - sentiment detection (Positive, Neutral, Negative, Angry)
  - urgency detection (Low, Medium, High, Critical)
  - escalation decisions with reasons and recommended actions
- OpenAI structured JSON output when `OPENAI_API_KEY` exists.
- Deterministic fallback rules so local development and tests work without OpenAI.

## Architecture
See `docs/architecture.md` for system design and roadmap.

## Tech Stack
- Python
- FastAPI
- Streamlit
- LangChain
- ChromaDB
- OpenAI

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
- `POST /analyze-ticket`

## Phase 2: Ticket Intelligence Usage
Example request:
```json
{
  "message": "I want a refund, your service is unacceptable.",
  "customer_tier": "premium",
  "previous_failed_answers": 1,
  "rag_confidence": 0.52
}
```

Example response:
```json
{
  "category": "Refund",
  "sentiment": "Angry",
  "urgency": "High",
  "escalate": true,
  "escalation_reason": "angry customer, refund request, repeated failed answer, low confidence answer",
  "recommended_action": "Escalate to a human specialist with full ticket context and customer history.",
  "confidence": 0.65
}
```

## Testing
```bash
pytest backend/tests
```

## Demo Video Placeholder
_Add demo video link here._
