from typing import Optional
from pydantic_settings import BaseSettings


class DBConfig(BaseSettings):
    """Database Configuration for Neon PostgreSQL with vector extension"""

    # Database connection settings
    DATABASE_URL: str = "postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require"

    # Vector database settings (for embeddings)
    VECTOR_STORE_TYPE: str = "qdrant"  # Changed to qdrant since we're using Qdrant
    POSTGRES_EMBEDDING_DIM: int = 768  # Changed to 768 for Google Gemini embeddings

    # Connection pool settings
    DB_POOL_SIZE: int = 20
    DB_POOL_OVERFLOW: int = 0
    DB_POOL_RECYCLE: int = 3600  # 1 hour

    # Database operation timeouts
    DB_TIMEOUT: int = 30  # seconds
    QUERY_TIMEOUT: int = 10  # seconds

    # Settings for content chunking
    MAX_CHUNK_SIZE: int = 1000  # tokens/words
    MIN_CHUNK_SIZE: int = 100   # tokens/words
    CHUNK_OVERLAP: int = 20    # tokens/words overlap between chunks

    # Embedding settings
    EMBEDDING_MODEL: str = "text-embedding-004"  # Updated for Google embeddings
    EMBEDDING_BATCH_SIZE: int = 100  # Number of texts to embed at once

    class Config:
        env_file = ".env"
        extra="allow"


# Create global instance
db_config = DBConfig()