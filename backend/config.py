# Main Configuration for Backend Services
# Coordinates all components of the RAG system

import os
from typing import Optional
from backend.database.config import DBConfig
from backend.database.qdrant_config import qdrant_settings
from backend.api.gemini_service import GeminiConfig

class BackendConfig:
    """Main configuration class that coordinates all backend services"""

    def __init__(self):
        # Database configuration
        self.db_config = DBConfig()

        # Qdrant configuration (imported as qdrant_settings)
        self.qdrant_config = qdrant_settings

        # Gemini configuration
        self.gemini_config = GeminiConfig()

        # Application settings
        self.app_environment = os.getenv("APP_ENV", "development")
        self.debug = self.app_environment == "development"

        # Content processing settings
        self.content_chunk_size = self.db_config.MAX_CHUNK_SIZE
        self.content_overlap = self.db_config.CHUNK_OVERLAP

        # API settings
        self.api_version = "v1"
        self.api_prefix = f"/api/{self.api_version}"

    def validate_config(self) -> bool:
        """Validate that all required configurations are properly set"""
        errors = []

        # Check if Gemini API key is set
        if not os.getenv("GEMINI_API_KEY"):
            errors.append("GEMINI_API_KEY environment variable not set")

        # Check if Qdrant settings are valid
        if not qdrant_settings.QDRANT_HOST and self.app_environment != "development":
            errors.append("QDRANT_HOST not set for production environment")

        # Check if database settings are valid
        if not self.db_config.DATABASE_URL:
            errors.append("DATABASE_URL not set")

        if errors:
            print("Configuration validation failed:")
            for error in errors:
                print(f"  - {error}")
            return False

        return True

# Initialize the main configuration
backend_config = BackendConfig()

# Validate configuration on startup
if not backend_config.validate_config():
    print("Warning: Configuration validation failed. Some features may not work correctly.")