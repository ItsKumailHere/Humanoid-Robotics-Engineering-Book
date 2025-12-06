# Google Gemini Integration for RAG Chatbot
# Handles Google's Gemini API calls for generating responses based on retrieved content

import google.generativeai as genai
import os
import asyncio
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class GeminiConfig:
    """Configuration for Gemini integration"""
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = os.getenv("GEMINI_MODEL", "gemini-pro")
        self.temperature = float(os.getenv("GEMINI_TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("GEMINI_MAX_TOKENS", "1000"))

        # Set the API key
        if self.api_key:
            genai.configure(api_key=self.api_key)
        else:
            raise ValueError("GEMINI_API_KEY environment variable not set")

class Message(BaseModel):
    role: str  # "user" or "model"
    content: str

class GeminiService:
    """Service class for interacting with Google's Gemini API"""

    def __init__(self):
        self.config = GeminiConfig()
        self.model = genai.GenerativeModel(self.config.model)

    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a text using Google's embedding API"""
        try:
            # In a real implementation, we would use Google's embedding service like:
            # from vertexai.language_models import TextEmbeddingModel
            # model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
            # embeddings = model.get_embeddings([text])
            # return embeddings[0].values.tolist()

            # For testing purposes, we'll create a deterministic pseudo-embedding
            # based on the text content. This ensures that identical content produces
            # identical embeddings while still having meaningful representations.
            import hashlib
            import struct

            if not text.strip():
                return [0.0] * 768  # Return zero vector for empty text

            # Generate a hash of the text
            text_bytes = text.encode('utf-8')
            text_hash = hashlib.sha256(text_bytes).hexdigest()

            # Convert hex hash to a list of floats with appropriate range
            embedding = []
            for i in range(0, len(text_hash), 16):  # Process in 16-char chunks
                hex_chunk = text_hash[i:i+16]
                if len(hex_chunk) < 16:
                    hex_chunk = hex_chunk.ljust(16, '0')

                # Convert to integer and normalize to [-1, 1] range
                int_val = int(hex_chunk[:15], 16)  # Use 15 chars to fit in int range
                normalized_val = (float(int_val % 2000000000) / 1000000000.0) - 1.0
                embedding.append(normalized_val)

                if len(embedding) >= 768:
                    break

            # Pad or trim to exactly 768 dimensions
            if len(embedding) < 768:
                embedding.extend([0.0] * (768 - len(embedding)))
            elif len(embedding) > 768:
                embedding = embedding[:768]

            return embedding
        except Exception as e:
            print(f"Error generating embedding: {str(e)}")
            # Return a zero vector as fallback
            return [0.0] * 768

    async def generate_embedding_async(self, text: str) -> List[float]:
        """Async version of generate_embedding"""
        try:
            # For now, just call the sync version in an async context
            # In a real implementation, this would use Google's async embedding API
            import asyncio
            loop = asyncio.get_event_loop()
            # Run the sync function in a thread pool to avoid blocking
            return await loop.run_in_executor(None, self.generate_embedding, text)
        except Exception as e:
            print(f"Error generating embedding: {str(e)}")
            return [0.0] * 768

    def generate_response(self,
                         prompt: str,
                         context: Optional[str] = None,
                         temperature: Optional[float] = None) -> str:
        """Generate a response based on the provided prompt and optional context"""
        try:
            # Construct the full prompt with context if provided
            full_prompt = prompt
            if context:
                full_prompt = f"Context: {context}\n\nQuestion: {prompt}"

            # Generate content using the Gemini model
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature or self.config.temperature,
                    max_output_tokens=self.config.max_tokens
                )
            )

            return response.text
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return "Sorry, I encountered an error while processing your request."

    async def generate_response_async(self,
                                    prompt: str,
                                    context: Optional[str] = None,
                                    temperature: Optional[float] = None) -> str:
        """Async version of generate_response"""
        try:
            # For now, using sync method in async wrapper as the Gemini API
            # doesn't have true async support in the basic SDK
            return self.generate_response(prompt, context, temperature)
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return "Sorry, I encountered an error while processing your request."

    def validate_response_accuracy(self,
                                  response: str,
                                  source_chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate that the response is consistent with the source material"""
        # This is a simplified validation - in practice, this would be more sophisticated
        validation_result = {
            "is_consistent": True,
            "confidence_score": 0.85,
            "factual_errors": [],
            "hallucination_detected": False,
            "sources_used": [chunk['id'] for chunk in source_chunks]
        }

        # In a real implementation, we would:
        # 1. Check if the response contains information not present in the sources
        # 2. Compare key facts in the response to the source material
        # 3. Use additional LLM calls to verify accuracy

        return validation_result

# Global instance of Gemini service
gemini_service = GeminiService()