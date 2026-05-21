from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, description="User question")


class ChatResponse(BaseModel):
    answer: str
    sources: list[str] = []


class HealthResponse(BaseModel):
    status: str
    message: str
