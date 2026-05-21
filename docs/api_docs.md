# API Documentation

## GET /health
Returns service health status.

## POST /upload
Uploads a knowledge base file to configured storage.

## POST /chat
Accepts a user question and returns answer plus citations.

## POST /analyze-ticket
Analyze a support ticket message for classification, sentiment, urgency, and escalation.

### Request Body
```json
{
  "message": "string",
  "customer_tier": "standard | premium | enterprise",
  "previous_failed_answers": 0,
  "rag_confidence": 0.85
}
```

### Response Body
```json
{
  "category": "Billing | Technical Support | Refund | Delivery | Product Question | Complaint | General Query",
  "sentiment": "Positive | Neutral | Negative | Angry",
  "urgency": "Low | Medium | High | Critical",
  "escalate": true,
  "escalation_reason": "string",
  "recommended_action": "string",
  "confidence": 0.0
}
```

### Escalation Rules
Escalation is set to `true` when any of the following are detected:
- angry customer
- refund request
- legal threat
- repeated failed answer
- low confidence answer (`rag_confidence < 0.6`)
- high-value customer issue

### Notes
- If `OPENAI_API_KEY` exists, the service uses OpenAI structured JSON output.
- If OpenAI is not configured/available, deterministic fallback rules are used.
