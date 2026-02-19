"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralised settings using pydantic-settings."""

    google_api_key: str = ""
    groq_api_key: str
    faiss_index_path: str = "./faiss_store"
    faiss_feedback_path: str = "./faiss_feedback_store"
    faiss_pedagogy_path: str = "./faiss_pedagogy_store"
    chunk_size: int = 1000
    chunk_overlap: int = 200

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
