from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables or .env."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    deepseek_api_key: str = Field(default="", alias="DEEPSEEK_API_KEY")
    deepseek_model: str = Field(default="deepseek-chat", alias="DEEPSEEK_MODEL")
    deepseek_temperature: float = Field(default=0.0, alias="DEEPSEEK_TEMPERATURE")
    rag_persist_directory: str = Field(
        default="workspace/index/chroma",
        alias="RAG_PERSIST_DIRECTORY",
    )
    rag_collection_name: str = Field(default="agent_documents", alias="RAG_COLLECTION_NAME")
    rag_embedding_model: str = Field(
        default="BAAI/bge-small-zh-v1.5",
        alias="RAG_EMBEDDING_MODEL",
    )
    rag_chunk_size: int = Field(default=800, alias="RAG_CHUNK_SIZE")
    rag_chunk_overlap: int = Field(default=120, alias="RAG_CHUNK_OVERLAP")
    rag_top_k: int = Field(default=4, alias="RAG_TOP_K")


def load_settings() -> Settings:
    return Settings()
