import os

from qdrant_client import QdrantClient
import cohere
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

cohere_client = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))
EMBED_MODEL = "embed-english-v3.0"

qdrant = QdrantClient(
    url=os.getenv("QDRANT_HOST"),
    api_key=os.getenv("QDRANT_API_KEY"),

)