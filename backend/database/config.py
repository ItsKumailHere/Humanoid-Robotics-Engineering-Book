# Database Configuration
# Configuration for Neon PostgreSQL with vector extension

# Database connection settings
DATABASE_URL: str = "postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require"

# Vector database settings (for embeddings)
VECTOR_STORE_TYPE: str = "postgres"  # or "qdrant"
POSTGRES_EMBEDDING_DIM: int = 1536  # OpenAI ada-002 embedding dimension

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
EMBEDDING_MODEL: str = "text-embedding-ada-002"
EMBEDDING_BATCH_SIZE: int = 100  # Number of texts to embed at once