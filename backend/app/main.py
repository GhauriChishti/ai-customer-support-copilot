from fastapi import FastAPI, File, UploadFile

from backend.app.agents.support_intelligence import analyze_ticket
from backend.app.config import settings
from backend.app.models.schemas import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
    TicketAnalysisRequest,
    TicketAnalysisResponse,
)
from backend.app.rag.rag_chain import generate_answer
from backend.app.rag.vector_store import VectorStoreClient
from backend.app.services.file_service import save_uploaded_file

app = FastAPI(title=settings.app_name, version=settings.app_version)
vector_store = VectorStoreClient(settings.vector_db_path)


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok", message="AI Customer Support Copilot API is running")


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)) -> dict:
    saved_path = await save_uploaded_file(settings.upload_dir, file)
    return {"filename": file.filename, "saved_to": str(saved_path), "status": "uploaded"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    result = generate_answer(request.question, vector_store)
    return ChatResponse(answer=result["answer"], sources=result.get("sources", []))


@app.post("/analyze-ticket", response_model=TicketAnalysisResponse)
def analyze_support_ticket(request: TicketAnalysisRequest) -> TicketAnalysisResponse:
    return analyze_ticket(request)
