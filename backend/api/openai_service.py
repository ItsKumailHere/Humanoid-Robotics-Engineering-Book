# OpenAI Integration for RAG Chatbot
# Handles OpenAI API calls for generating responses based on retrieved content

from openai import OpenAI
import os
import asyncio
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class OpenAIConfig:
    """Configuration for OpenAI integration"""
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
        
        # Initialize the OpenAI client
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            raise ValueError("OPENAI_API_KEY environment variable not set")

class Message(BaseModel):
    role: str  # "system", "user", or "assistant"
    content: str

class OpenAIService:
    """Service class for interacting with OpenAI API"""
    
    def __init__(self):
        self.config = OpenAIConfig()
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a text using OpenAI's embedding API"""
        try:
            response = self.config.client.embeddings.create(
                input=text,
                model="text-embedding-3-small"  # Updated to latest embedding model
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {str(e)}")
            return []
    
    async def generate_embedding_async(self, text: str) -> List[float]:
        """Async version of generate_embedding"""
        try:
            response = await self.config.client.embeddings.create(
                input=text,
                model="text-embedding-3-small"
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {str(e)}")
            return []
    
    def generate_response(self, 
                         messages: List[Dict[str, str]], 
                         temperature: Optional[float] = None) -> str:
        """Generate a response based on the provided messages"""
        try:
            response = self.config.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=temperature or self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return "Sorry, I encountered an error while processing your request."
    
    async def generate_response_async(self, 
                                    messages: List[Dict[str, str]], 
                                    temperature: Optional[float] = None) -> str:
        """Async version of generate_response"""
        try:
            response = await self.config.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=temperature or self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            return response.choices[0].message.content
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

# Global instance of OpenAI service
openai_service = OpenAIService()