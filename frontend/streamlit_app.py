import requests
import streamlit as st

API_BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Customer Support Copilot", layout="wide")
st.title("AI Customer Support Copilot")

st.subheader("1) Upload Knowledge Base Documents")
uploaded_file = st.file_uploader("Upload a PDF, TXT, or DOC file", type=["pdf", "txt", "doc", "docx"])

if uploaded_file and st.button("Upload File"):
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
    response = requests.post(f"{API_BASE_URL}/upload", files=files, timeout=30)
    if response.ok:
        st.success(f"Uploaded: {response.json().get('filename')}")
    else:
        st.error("Upload failed. Check backend logs.")

st.subheader("2) Ask a Question")
question = st.text_input("Ask about policies, tickets, or customer issues")

if st.button("Send") and question:
    response = requests.post(f"{API_BASE_URL}/chat", json={"question": question}, timeout=30)
    if response.ok:
        data = response.json()
        st.markdown("### Answer")
        st.write(data.get("answer", "No answer returned."))

        st.markdown("### Sources / Citations")
        for source in data.get("sources", []):
            st.write(f"- {source}")
    else:
        st.error("Chat request failed. Check backend logs.")

st.subheader("3) Ticket Intelligence")
ticket_message = st.text_area("Customer message", height=150)
customer_tier = st.selectbox("Customer tier", options=["standard", "premium", "enterprise"], index=0)
previous_failed_answers = st.number_input("Previous failed answers", min_value=0, step=1, value=0)
rag_confidence = st.slider("RAG confidence", min_value=0.0, max_value=1.0, value=0.85, step=0.01)

if st.button("Analyze Ticket"):
    if not ticket_message.strip():
        st.warning("Please provide a customer message before analysis.")
    else:
        payload = {
            "message": ticket_message,
            "customer_tier": customer_tier,
            "previous_failed_answers": int(previous_failed_answers),
            "rag_confidence": float(rag_confidence),
        }
        response = requests.post(f"{API_BASE_URL}/analyze-ticket", json=payload, timeout=30)
        if response.ok:
            data = response.json()
            st.markdown("### Analysis Result")
            st.write(f"**Category:** {data.get('category')}")
            st.write(f"**Sentiment:** {data.get('sentiment')}")
            st.write(f"**Urgency:** {data.get('urgency')}")
            st.write(f"**Escalate:** {data.get('escalate')}")
            st.write(f"**Escalation Reason:** {data.get('escalation_reason')}")
            st.write(f"**Recommended Action:** {data.get('recommended_action')}")
            st.write(f"**Confidence:** {data.get('confidence')}")
        else:
            st.error(f"Ticket analysis failed: {response.text}")
