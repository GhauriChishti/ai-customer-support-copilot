from pathlib import Path

from fastapi import UploadFile


async def save_uploaded_file(upload_dir: Path, file: UploadFile) -> Path:
    """Persist uploaded file to local storage."""
    upload_dir.mkdir(parents=True, exist_ok=True)
    target = upload_dir / file.filename
    content = await file.read()
    target.write_bytes(content)
    return target
