from backend.app.agents.support_intelligence import analyze_ticket
from backend.app.models.schemas import TicketAnalysisRequest


def test_refund_request_escalates() -> None:
    result = analyze_ticket(
        TicketAnalysisRequest(
            message="I want a refund for this order immediately.",
            customer_tier="standard",
            previous_failed_answers=0,
            rag_confidence=0.9,
        )
    )
    assert result.category == "Refund"
    assert result.escalate is True
    assert "refund request" in result.escalation_reason


def test_angry_complaint_escalates() -> None:
    result = analyze_ticket(
        TicketAnalysisRequest(
            message="I am furious and this service is unacceptable.",
            customer_tier="standard",
            previous_failed_answers=0,
            rag_confidence=0.9,
        )
    )
    assert result.sentiment == "Angry"
    assert result.escalate is True
    assert "angry customer" in result.escalation_reason


def test_legal_threat_escalates() -> None:
    result = analyze_ticket(
        TicketAnalysisRequest(
            message="If this is not fixed, my attorney will sue your company.",
            customer_tier="standard",
            previous_failed_answers=0,
            rag_confidence=0.9,
        )
    )
    assert result.escalate is True
    assert "legal threat" in result.escalation_reason


def test_normal_product_question_does_not_escalate() -> None:
    result = analyze_ticket(
        TicketAnalysisRequest(
            message="Can I integrate this with Slack and Microsoft Teams?",
            customer_tier="standard",
            previous_failed_answers=0,
            rag_confidence=0.93,
        )
    )
    assert result.category == "Product Question"
    assert result.escalate is False


def test_enterprise_customer_low_confidence_escalates() -> None:
    result = analyze_ticket(
        TicketAnalysisRequest(
            message="We need help understanding this feature rollout.",
            customer_tier="enterprise",
            previous_failed_answers=0,
            rag_confidence=0.45,
        )
    )
    assert result.escalate is True
    assert "low confidence answer" in result.escalation_reason
