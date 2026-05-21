from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = "AI Customer Support Copilot API"
    app_version: str = "0.1.0"
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    vector_db_path: Path = Field(default=Path("./data/chroma"), alias="VECTOR_DB_PATH")
    upload_dir: Path = Field(default=Path("./data/knowledgebase"), alias="UPLOAD_DIR")

    class Config:
        populate_by_name = True


settings = Settings()
