# Main FastAPI Application for RAG Chatbot
# Implements the API endpoints for the Humanoid Robotics textbook RAG system

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from backend.database.qdrant_service import qdrant_service
from backend.utils.content_extraction import ContentExtractor
from backend.utils.chunking import ContentChunker
from backend.api.gemini_service import gemini_service
import logging
import os

# Initialize FastAPI app
app = FastAPI(
    title="Humanoid Robotics Textbook RAG API",
    description="API for retrieving and searching textbook content using RAG",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define Pydantic models for request/response
class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5
    chapter_filter: Optional[str] = None

class QueryResponse(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    execution_time: float

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, str]]] = []
    top_k: Optional[int] = 5
    temperature: Optional[float] = 0.7

class ChatResponse(BaseModel):
    response: str
    sources: List[Dict[str, Any]]
    execution_time: float

class ContentChunkModel(BaseModel):
    id: str
    text: str
    chapter_id: str
    metadata: Dict[str, Any]

# Include the API routes
@app.get("/")
async def root():
    return {"message": "Humanoid Robotics Textbook RAG API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/v1/query", response_model=QueryResponse)
async def query_content(request: QueryRequest):
    """
    Query the textbook content using vector search
    """
    import time
    start_time = time.time()

    try:
        # 1. Generate embedding for the query using Gemini service
        query_embedding = gemini_service.generate_embedding(request.query)

        # 2. Search in Qdrant using qdrant_service
        search_results = qdrant_service.search_similar(
            query_embedding=query_embedding,
            chapter_filter=request.chapter_filter,
            top_k=request.top_k
        )

        execution_time = time.time() - start_time
        response = QueryResponse(
            query=request.query,
            results=search_results,
            execution_time=execution_time
        )

        logger.info(f"Query completed in {execution_time:.2f}s: {request.query}")
        return response

    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat_with_textbook(request: ChatRequest):
    """
    Chat with the textbook content using RAG
    """
    import time
    start_time = time.time()

    try:
        # 1. Generate embedding for the user's message using Gemini service
        query_embedding = gemini_service.generate_embedding(request.message)

        # 2. Search in the vector database for relevant content
        search_results = qdrant_service.search_similar(
            query_embedding=query_embedding,
            top_k=request.top_k
        )

        # 3. Use Gemini API to generate a response based on retrieved content
        if search_results:
            # Combine the relevant content for context
            context = " ".join([result['text'] for result in search_results])
            response_text = gemini_service.generate_response(
                prompt=request.message,
                context=context,
                temperature=request.temperature
            )
        else:
            # If no relevant content is found, respond with a default message
            response_text = f"I couldn't find specific information about '{request.message}' in the textbook. Please check the relevant chapters or ask about a different topic."

        execution_time = time.time() - start_time
        response = ChatResponse(
            response=response_text,
            sources=search_results,
            execution_time=execution_time
        )

        logger.info(f"Chat query completed in {execution_time:.2f}s: {request.message}")
        return response

    except Exception as e:
        logger.error(f"Error processing chat query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/chapters")
async def get_chapters():
    """
    Get a list of all available chapters
    """
    try:
        # This would connect to the database to get chapter information
        # For now, return a mock list based on the actual chapters in the frontend
        extractor = ContentExtractor()
        chapters = extractor.extract_all_chapters()
        
        chapter_list = []
        for chapter in chapters:
            chapter_list.append({
                "id": chapter.id,
                "title": chapter.title,
                "description": chapter.description,
                "learning_objectives": chapter.learning_objectives,
                "sidebar_position": chapter.sidebar_position
            })
        
        return {"chapters": chapter_list}
        
    except Exception as e:
        logger.error(f"Error getting chapters: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/chapters/{chapter_id}")
async def get_chapter(chapter_id: str):
    """
    Get details of a specific chapter
    """
    try:
        extractor = ContentExtractor()
        chapters = extractor.extract_all_chapters()
        
        for chapter in chapters:
            if chapter.id == chapter_id:
                return {
                    "id": chapter.id,
                    "title": chapter.title,
                    "description": chapter.description,
                    "learning_objectives": chapter.learning_objectives,
                    "sections": chapter.sections,
                    "exercises": chapter.exercises,
                    "summary": chapter.summary,
                    "references": chapter.references
                }
        
        raise HTTPException(status_code=404, detail="Chapter not found")
        
    except Exception as e:
        logger.error(f"Error getting chapter {chapter_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/index-content")
async def index_content():
    """
    Index textbook content into the vector database
    This endpoint processes all textbook content and stores embeddings
    """
    try:
        logger.info("Starting content indexing process")

        # Extract chapters
        extractor = ContentExtractor()
        chapters = extractor.extract_all_chapters()
        logger.info(f"Extracted {len(chapters)} chapters")

        # Chunk content
        chunker = ContentChunker()
        total_chunks = 0

        for chapter in chapters:
            chunks = chunker.chunk_chapter(chapter.id, chapter.content)
            total_chunks += len(chunks)

            # Generate embeddings for each chunk and store in Qdrant
            text_chunks = [chunk.text for chunk in chunks]
            embeddings = []

            for chunk_text in text_chunks:
                # Generate embedding using Gemini service
                embedding = gemini_service.generate_embedding(chunk_text)
                embeddings.append(embedding)

            # Store embeddings in Qdrant
            metadata_list = [{'section': chunk.section, 'position': chunk.position, 'chunk_type': chunk.chunk_type}
                           for chunk in chunks]

            qdrant_service.store_embeddings(
                chapter_id=chapter.id,
                text_chunks=text_chunks,
                embeddings=embeddings,
                metadata_list=metadata_list
            )

            logger.info(f"Chapter {chapter.id}: indexed {len(chunks)} chunks")

        logger.info(f"Indexing complete: {total_chunks} total chunks")

        return {
            "status": "success",
            "indexed_chapters": len(chapters),
            "total_chunks": total_chunks
        }

    except Exception as e:
        logger.error(f"Error indexing content: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)