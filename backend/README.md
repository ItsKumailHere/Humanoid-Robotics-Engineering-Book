# Humanoid Robotics Textbook - Backend Services

This directory contains the backend infrastructure for the AI-powered RAG (Retrieval Augmented Generation) chatbot that works with the Humanoid Robotics textbook.

## Architecture Overview

The backend consists of several key components:

1. **Database Layer**: PostgreSQL (with Neon) and Qdrant vector database for content storage
2. **Content Processing**: Extraction, parsing, and chunking of textbook content
3. **API Layer**: FastAPI-based REST API for querying and chat functionality
4. **AI Integration**: Google's Gemini API integration for response generation
5. **Validation System**: Ensures response accuracy and prevents hallucinations

## Directory Structure

```
backend/
├── api/                    # FastAPI application and endpoints
│   ├── main.py            # Main application entry point
│   ├── gemini_service.py  # Google Gemini integration
│   ├── validation.py      # Response validation system
│   └── models/            # Pydantic models
├── database/              # Database schemas and configurations
│   ├── schema.sql         # PostgreSQL schema
│   ├── config.py          # Database configuration
│   ├── qdrant_config.py   # Qdrant configuration
│   └── qdrant_service.py  # Qdrant client service
├── utils/                 # Utility functions
│   ├── chunking.py        # Content chunking pipeline
│   └── content_extraction.py # Content extraction and parsing
├── config.py              # Main backend configuration
└── requirements.txt       # Python dependencies
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL with vector extension (for Neon)
- Qdrant Cloud account (optimized for free tier) or local instance for development
- Google Gemini API key

### Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export DATABASE_URL="postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require"
export QDRANT_HOST="https://your-cluster-url.qdrant.tech:6333"
export QDRANT_API_KEY="your-qdrant-api-key"
export GEMINI_API_KEY="your-gemini-api-key"
```

### Running the Application

1. Initialize the database and vector store with textbook content:
```bash
python -m backend.api.main /api/v1/index-content
```

2. Start the FastAPI server:
```bash
uvicorn backend.api.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /api/v1/query` - Query textbook content
- `POST /api/v1/chat` - Chat with textbook content
- `GET /api/v1/chapters` - Get all chapters
- `GET /api/v1/chapters/{id}` - Get specific chapter
- `POST /api/v1/index-content` - Index textbook content

## RAG Implementation

The RAG system works as follows:

1. **Content Indexing**: Textbook chapters are parsed, chunked, and vector embeddings are generated using Google's Gemini embedding model (768-dimensional vectors)
2. **Storage**: Embeddings and content chunks are stored in Qdrant vector database with free-tier optimizations
3. **Query Processing**: User queries are embedded and searched against the vector database
4. **Response Generation**: Relevant content is retrieved and passed to Google's Gemini model to generate responses
5. **Validation**: Responses are validated against source material to prevent hallucinations

## Configuration

The system can be configured via environment variables:

- `DATABASE_URL` - PostgreSQL connection string
- `QDRANT_HOST` - Qdrant Cloud URL
- `QDRANT_API_KEY` - Qdrant API key
- `GEMINI_API_KEY` - Google Gemini API key
- `GEMINI_MODEL` - Gemini model to use (default: gemini-pro)
- `GEMINI_TEMPERATURE` - Response randomness (default: 0.7)
- `APP_ENV` - Application environment (development/production)

## Security Considerations

- All API keys should be stored in environment variables
- In production, implement proper authentication and rate limiting
- Sanitize user input to prevent injection attacks
- Use HTTPS for all API communications

## Local Testing Guide

### Full Local Setup

1. **Setup Qdrant locally (Docker method):**
   ```bash
   docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
   ```

   Or use Docker Compose with this configuration:
   ```yaml
   version: '3.7'
   services:
     qdrant:
       image: qdrant/qdrant:latest
       ports:
         - "6333:6333"
         - "6334:6334"
       volumes:
         - ./qdrant_data:/qdrant/storage
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the backend directory:
   ```
   GEMINI_API_KEY=your-gemini-api-key
   QDRANT_HOST=http://localhost:6333
   QDRANT_API_KEY=  # Not needed for local instance
   DATABASE_URL=postgresql://username:password@localhost/dbname
   APP_ENV=development
   ```

4. **Initialize content:**
   ```bash
   # First, make sure your frontend content is available
   # Then run the indexing endpoint:
   python -c "
   import sys
   sys.path.append('.')
   from api.main import index_content
   import asyncio
   asyncio.run(index_content())
   "
   # Or by calling the API after starting the server
   ```

5. **Start the backend:**
   ```bash
   uvicorn backend.api.main:app --reload --port 8000
   ```

6. **Test the endpoints:**
   - Go to `http://localhost:8000/health` to verify the service is running
   - Use the `/api/v1/chapters` endpoint to see available chapters
   - Test the chat functionality with `/api/v1/chat`

### Using Google Colab for Testing (Alternative)

If you face issues running locally, you can use Google Colab:

1. Upload the backend code to Google Colab
2. Install dependencies: `!pip install -r requirements.txt`
3. Set your API keys in the Colab environment
4. Run the server using a tunnel like `pyngrok`

### Troubleshooting Common Issues

- **Qdrant Connection Issues**: Ensure Qdrant service is running and accessible
- **API Key Issues**: Verify that GEMINI_API_KEY is properly set
- **Embedding Issues**: The placeholder embedding function returns 768-dim vectors; ensure this matches your actual embedding service if you integrate one
- **Memory Issues**: The free tier optimizations help, but large datasets may still cause memory issues during indexing

## Future Enhancements

1. Personalization system based on user interactions
2. Advanced content validation and fact-checking
3. Multi-language support for Urdu translation
4. Enhanced caching mechanisms
5. More sophisticated content chunking strategies