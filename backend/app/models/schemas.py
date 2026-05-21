from typing import Literal

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, description="User question")


class ChatResponse(BaseModel):
    answer: str
    sources: list[str] = []


class HealthResponse(BaseModel):
    status: str
    message: str


class TicketAnalysisRequest(BaseModel):
    message: str = Field(..., min_length=1)
    customer_tier: Literal["standard", "premium", "enterprise"] = "standard"
    previous_failed_answers: int = Field(default=0, ge=0)
    rag_confidence: float = Field(default=0.85, ge=0.0, le=1.0)


class TicketAnalysisResponse(BaseModel):
    category: Literal[
        "Billing",
        "Technical Support",
        "Refund",
        "Delivery",
        "Product Question",
        "Complaint",
        "General Query",
    ]
    sentiment: Literal["Positive", "Neutral", "Negative", "Angry"]
    urgency: Literal["Low", "Medium", "High", "Critical"]
    escalate: bool
    escalation_reason: str
    recommended_action: str
    confidence: float = Field(..., ge=0.0, le=1.0)
