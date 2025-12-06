# Qdrant Vector Database Configuration
# Configuration for Qdrant Cloud vector storage

from typing import Optional
from pydantic_settings import BaseSettings

class QdrantSettings(BaseSettings):
    # Qdrant connection settings
    QDRANT_HOST: Optional[str] = None  # Qdrant Cloud URL or local host
    QDRANT_API_KEY: Optional[str] = None  # Qdrant Cloud API key
    QDRANT_PORT: int = 6333  # Default Qdrant port
    QDRANT_GRPC_PORT: int = 6334  # Default Qdrant gRPC port
    GEMINI_API_KEY: Optional[str] = None  # Google Gemini API key
    
    # Collection settings
    COLLECTION_NAME: str = "humanoid_robotics_content"
    EMBEDDING_DIM: int = 768  # Google Gemini embedding dimension
    
    # Vector storage settings
    DISTANCE_METRIC: str = "Cosine"  # Cosine, Euclid, Manhattan, Dot
    ON_DISK: bool = False  # Free tier optimization: keep vectors in memory

    # Index and performance settings for free tier
    REPLICATE_ON_WRITE: bool = False  # Free tier optimization
    WRITE_CONSISTENCY_FACTOR: int = 1  # Minimum for free tier
    
    class Config:
        env_file = ".env"

# Initialize settings
qdrant_settings = QdrantSettings()

# Collection configuration for content (optimized for Qdrant Cloud free tier)
COLLECTION_CONFIG = {
    "vector_size": qdrant_settings.EMBEDDING_DIM,
    "distance": qdrant_settings.DISTANCE_METRIC,
    "on_disk_payload": qdrant_settings.ON_DISK,
    # Additional free tier optimizations
    "hnsw_config": {
        "m": 16,  # Lower value for free tier
        "ef_construct": 100,  # Lower value for free tier
    },
    "optimizer_config": {
        "max_segment_size": 50000,  # Reduced for free tier
        "default_segment_number": 2,  # Reduced for free tier
        "indexing_threshold": 20000,  # Reduced for free tier
    }
}