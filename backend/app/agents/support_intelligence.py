from __future__ import annotations

import re
from dataclasses import dataclass

from backend.app.config import settings
from backend.app.models.schemas import TicketAnalysisRequest, TicketAnalysisResponse

try:
    from langchain_openai import ChatOpenAI
except Exception:  # pragma: no cover - dependency/import edge case
    ChatOpenAI = None


@dataclass
class RuleSignals:
    category: str
    sentiment: str
    urgency: str
    escalate: bool
    escalation_reason: str
    recommended_action: str
    confidence: float


CATEGORIES = [
    "Billing",
    "Technical Support",
    "Refund",
    "Delivery",
    "Product Question",
    "Complaint",
    "General Query",
]

SENTIMENTS = ["Positive", "Neutral", "Negative", "Angry"]
URGENCY_LEVELS = ["Low", "Medium", "High", "Critical"]


def analyze_ticket(request: TicketAnalysisRequest) -> TicketAnalysisResponse:
    if settings.openai_api_key and ChatOpenAI is not None:
        ai_result = _analyze_ticket_with_openai(request)
        if ai_result is not None:
            return ai_result
    return _analyze_ticket_with_rules(request)


def _analyze_ticket_with_openai(request: TicketAnalysisRequest) -> TicketAnalysisResponse | None:
    try:
        llm = ChatOpenAI(model="gpt-4o-mini", api_key=settings.openai_api_key, temperature=0)
        structured_llm = llm.with_structured_output(TicketAnalysisResponse)
        prompt = (
            "You are a customer support intelligence engine. Return only a valid JSON object that matches the schema. "
            f"Valid categories: {CATEGORIES}. "
            f"Valid sentiments: {SENTIMENTS}. "
            f"Valid urgency levels: {URGENCY_LEVELS}. "
            "Set escalate=true when customer is angry, refund request exists, legal threat is present, previous failed answers > 0, "
            "RAG confidence is below 0.6, or a high-value customer has a serious issue."
            f"\n\nTicket message: {request.message}\n"
            f"Customer tier: {request.customer_tier}\n"
            f"Previous failed answers: {request.previous_failed_answers}\n"
            f"RAG confidence: {request.rag_confidence}\n"
        )
        return structured_llm.invoke(prompt)
    except Exception:
        return None


def _analyze_ticket_with_rules(request: TicketAnalysisRequest) -> TicketAnalysisResponse:
    signals = _extract_rule_signals(request)
    return TicketAnalysisResponse(
        category=signals.category,
        sentiment=signals.sentiment,
        urgency=signals.urgency,
        escalate=signals.escalate,
        escalation_reason=signals.escalation_reason,
        recommended_action=signals.recommended_action,
        confidence=signals.confidence,
    )


def _extract_rule_signals(request: TicketAnalysisRequest) -> RuleSignals:
    message = request.message.lower()

    is_refund = _contains_any(message, ["refund", "money back", "chargeback", "return my money"])
    is_billing = _contains_any(message, ["invoice", "charged", "billing", "payment", "subscription", "price"])
    is_technical = _contains_any(message, ["bug", "error", "issue", "not working", "crash", "login", "reset password"])
    is_delivery = _contains_any(message, ["delivery", "shipping", "shipment", "tracking", "arrive", "late package"])
    is_product_question = _contains_any(message, ["how does", "feature", "can i", "does it", "what is", "integration"])
    is_complaint = _contains_any(message, ["complaint", "unacceptable", "disappointed", "terrible", "frustrated", "angry"])
    legal_threat = _contains_any(message, ["lawsuit", "legal", "attorney", "sue", "consumer protection", "report you"])

    if is_refund:
        category = "Refund"
    elif is_billing:
        category = "Billing"
    elif is_technical:
        category = "Technical Support"
    elif is_delivery:
        category = "Delivery"
    elif is_complaint:
        category = "Complaint"
    elif is_product_question:
        category = "Product Question"
    else:
        category = "General Query"

    angry_markers = ["angry", "furious", "outrage", "ridiculous", "unacceptable", "fed up", "terrible service"]
    negative_markers = ["frustrated", "disappointed", "bad", "not happy", "upset"]
    positive_markers = ["thanks", "great", "love", "awesome", "helpful"]

    if _contains_any(message, angry_markers):
        sentiment = "Angry"
    elif _contains_any(message, negative_markers) or is_complaint:
        sentiment = "Negative"
    elif _contains_any(message, positive_markers):
        sentiment = "Positive"
    else:
        sentiment = "Neutral"

    urgency = "Low"
    if _contains_any(message, ["asap", "urgent", "immediately", "today", "right now"]):
        urgency = "High"
    if legal_threat or _contains_any(message, ["cancel contract", "security breach", "data loss"]):
        urgency = "Critical"
    elif request.previous_failed_answers > 0 or sentiment in {"Angry", "Negative"}:
        urgency = "Medium" if urgency == "Low" else urgency

    escalation_reasons: list[str] = []
    if sentiment == "Angry":
        escalation_reasons.append("angry customer")
    if is_refund:
        escalation_reasons.append("refund request")
    if legal_threat:
        escalation_reasons.append("legal threat")
    if request.previous_failed_answers > 0:
        escalation_reasons.append("repeated failed answer")
    if request.rag_confidence < 0.6:
        escalation_reasons.append("low confidence answer")
    if request.customer_tier in {"premium", "enterprise"} and urgency in {"High", "Critical"}:
        escalation_reasons.append("high-value customer issue")

    escalate = len(escalation_reasons) > 0

    if escalate:
        recommended_action = "Escalate to a human specialist with full ticket context and customer history."
        escalation_reason = ", ".join(escalation_reasons)
    else:
        recommended_action = "Respond with standard support workflow and monitor follow-up."
        escalation_reason = "none"

    confidence = 0.9
    if request.rag_confidence < 0.6:
        confidence = 0.65
    if category == "General Query":
        confidence = min(confidence, 0.75)
    if legal_threat:
        confidence = min(confidence, 0.7)

    return RuleSignals(
        category=category,
        sentiment=sentiment,
        urgency=urgency,
        escalate=escalate,
        escalation_reason=escalation_reason,
        recommended_action=recommended_action,
        confidence=round(confidence, 2),
    )


def _contains_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(rf"\\b{re.escape(pattern)}\\b", text) for pattern in patterns)
