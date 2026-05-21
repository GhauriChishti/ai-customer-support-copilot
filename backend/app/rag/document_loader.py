from pathlib import Path


def load_documents(upload_dir: Path) -> list[dict]:
    """Placeholder document loading logic for future LangChain loaders."""
    documents: list[dict] = []
    for file_path in upload_dir.glob("**/*"):
        if file_path.is_file():
            documents.append({"path": str(file_path), "content": ""})
    return documents
