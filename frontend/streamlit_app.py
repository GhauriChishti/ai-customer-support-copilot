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
