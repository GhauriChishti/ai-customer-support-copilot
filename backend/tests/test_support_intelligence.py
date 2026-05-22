from backend.app.agents.support_intelligence import analyze_ticket
from backend.app.models.schemas import TicketAnalysisRequest


def test_angry_refund_escalates() -> None:
    result = analyze_ticket(
        TicketAnalysisRequest(
            message="I am furious, this is the worst, and I want a refund now.",
            customer_tier="standard",
            previous_failed_answers=0,
            rag_confidence=0.9,
        )
    )
    assert result.category == "Refund"
    assert result.escalate is True
    assert "refund request" in result.escalation_reason


def test_angry_keywords_escalate() -> None:
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




def test_technical_issue_classified() -> None:
    result = analyze_ticket(
        TicketAnalysisRequest(
            message="File upload failed with an error and the app crash persists.",
            customer_tier="standard",
            previous_failed_answers=0,
            rag_confidence=0.92,
        )
    )
    assert result.category == "Technical Support"

def test_product_integration_question_classified() -> None:
    result = analyze_ticket(
        TicketAnalysisRequest(
            message="Does your platform support integration with Slack?",
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
    assert "enterprise low rag confidence" in result.escalation_reason
