"""
Documentation RAG Chatbot for Docusaurus MDX files
Loads, processes, and indexes .mdx files for question answering
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import re
from pathlib import Path

from langchain_cohere import CohereEmbeddings
# from langchain_core.vectorstores import InMemoryVectorStore
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import cohere

from dotenv import load_dotenv

load_dotenv()

# Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
DOCS_DIRECTORY = "../frontend/docs/Chapters"  # Adjust this path to your docs folder
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Qdrant configuration
QDRANT_COLLECTION_NAME = "my_collection"
QDRANT_URL = os.getenv("QDRANT_URL")  # Use :memory: for testing, or set QDRANT_URL for production
# QDRANT_URL = ":memory:"  # In-memory Qdrant for now, change to actual URL for production

# Initialize FastAPI app
app = FastAPI(
    title="Documentation RAG Chatbot API",
    description="RAG chatbot for Docusaurus documentation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    include_sources: Optional[bool] = False

class RetrievedDocument(BaseModel):
    content: str
    source: str
    metadata: Optional[dict] = None

class ChatResponse(BaseModel):
    response: str
    sources: Optional[List[RetrievedDocument]] = None

# Global variables
rag_chain = None
retriever = None
vectorstore = None


def extract_frontmatter(content: str) -> tuple[dict, str]:
    """Extract frontmatter and content from MDX file"""
    frontmatter = {}
    main_content = content
    
    # Check for frontmatter (between --- delimiters)
    frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.match(frontmatter_pattern, content, re.DOTALL)
    
    if match:
        frontmatter_text = match.group(1)
        main_content = content[match.end():]
        
        # Parse frontmatter (simple key: value parsing)
        for line in frontmatter_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                frontmatter[key.strip()] = value.strip().strip('"').strip("'")
    
    return frontmatter, main_content


def clean_mdx_content(content: str) -> str:
    """Remove JSX components and clean MDX content"""
    
    # Remove import statements
    content = re.sub(r'^import\s+.*?from\s+[\'"].*?[\'"];?\s*$', '', content, flags=re.MULTILINE)
    
    # Remove JSX components (simple pattern, may need adjustment)
    content = re.sub(r'<[A-Z]\w*[^>]*>.*?</[A-Z]\w*>', '', content, flags=re.DOTALL)
    content = re.sub(r'<[A-Z]\w*[^>]*/>', '', content)
    
    # Remove HTML comments
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    
    # Clean up excessive whitespace
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    return content.strip()


def load_mdx_files(directory: str) -> List[Document]:
    """Load all .mdx and .md files from directory recursively"""
    documents = []
    docs_path = Path(directory)
    
    if not docs_path.exists():
        print(f"⚠️  Warning: Directory {directory} does not exist")
        return documents
    
    # Find all .mdx and .md files
    mdx_files = list(docs_path.rglob("*.mdx")) + list(docs_path.rglob("*.md"))
    
    print(f"Found {len(mdx_files)} documentation files")
    
    for file_path in mdx_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract frontmatter and content
            frontmatter, main_content = extract_frontmatter(content)
            
            # Clean MDX content
            cleaned_content = clean_mdx_content(main_content)
            
            if not cleaned_content.strip():
                continue
            
            # Get relative path for source tracking
            relative_path = file_path.relative_to(docs_path)
            
            # Create metadata
            metadata = {
                "source": str(relative_path),
                "file_path": str(file_path),
                "title": frontmatter.get("title", relative_path.stem),
                **frontmatter
            }
            
            # Create document
            doc = Document(
                page_content=cleaned_content,
                metadata=metadata
            )
            documents.append(doc)
            
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    
    print(f"Successfully loaded {len(documents)} documents")
    return documents


def chunk_documents(documents: List[Document]) -> List[Document]:
    """Split documents into smaller chunks"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n## ", "\n### ", "\n\n", "\n", " ", ""]
    )
    
    chunked_docs = text_splitter.split_documents(documents)
    print(f"Created {len(chunked_docs)} chunks from {len(documents)} documents")
    
    return chunked_docs


def setup_rag_chain(docs_directory: str):
    """Initialize the RAG chain with documentation files"""
    
    # Load and process documents
    print("Loading documentation files...")
    documents = load_mdx_files(docs_directory)
    
    if not documents:
        raise ValueError(f"No documents found in {docs_directory}")
    
    # Chunk documents
    print("Chunking documents...")
    chunks = chunk_documents(documents)
    
    # Initialize embeddings and LLM
    print("Initializing embeddings and LLM...")
    # Initialize Cohere client and async client with API key
    cohere_api_key = os.getenv("COHERE_API_KEY")
    cohere_client = cohere.ClientV2(api_key=cohere_api_key)
    cohere_async_client = cohere.AsyncClientV2(api_key=cohere_api_key)
    embeddings = CohereEmbeddings(client=cohere_client, async_client=cohere_async_client, model="embed-english-v3.0")
    # llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2)
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2)
    
    # Create Qdrant vector store
    print("Setting up Qdrant vector store...")
    # Initialize Qdrant client
    qdrant_client = QdrantClient(url=QDRANT_URL, api_key=os.getenv("QDRANT_API_KEY"))
    
    # Delete collection if it exists (for fresh start)
    if qdrant_client.collection_exists(QDRANT_COLLECTION_NAME):
        print(f"Deleting existing collection: {QDRANT_COLLECTION_NAME}")
        qdrant_client.delete_collection(QDRANT_COLLECTION_NAME)
    
    # Get embedding dimension
    print("Calculating embedding dimensions...")
    embedding_dim = len(embeddings.embed_query("sample text"))
    
    # Create collection with proper vector configuration
    print(f"Creating Qdrant collection: {QDRANT_COLLECTION_NAME}")
    qdrant_client.create_collection(
        collection_name=QDRANT_COLLECTION_NAME,
        vectors_config=VectorParams(size=embedding_dim, distance=Distance.COSINE)
    )
    
    # Create vector store and add documents
    print("Adding documents to Qdrant vector store...")
    vectorstore = QdrantVectorStore(
        client=qdrant_client,
        collection_name=QDRANT_COLLECTION_NAME,
        embedding=embeddings
    )
    vectorstore.add_documents(chunks)
    
    # # OLD: InMemoryVectorStore approach
    # # vectorstore = InMemoryVectorStore.from_documents(
    # #     chunks,
    # #     embedding=embeddings
    # # )
    
    # Create retriever
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 4}
    )
    
    # Define prompt template
    template = """You are a helpful documentation assistant. Answer the user's question based on the provided documentation context.
If the answer is not in the context, say you don't have that information in the documentation.

Documentation Context:
{context}

Question: {question}

Answer:"""
    
    prompt = ChatPromptTemplate.from_template(template)
    
    # Create RAG chain
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    print("✓ RAG system initialized successfully!")
    return rag_chain, retriever, vectorstore


@app.on_event("startup")
async def startup_event():
    """Initialize RAG system on startup"""
    global rag_chain, retriever, vectorstore
    
    try:
        print("Initializing Documentation RAG system...")
        rag_chain, retriever, vectorstore = setup_rag_chain(DOCS_DIRECTORY)
    except Exception as e:
        print(f"❌ Error initializing RAG system: {e}")
        print(f"Make sure the docs directory exists at: {DOCS_DIRECTORY}")
        raise


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Documentation RAG Chatbot API",
        "version": "1.0.0",
        "docs_directory": DOCS_DIRECTORY,
        "endpoints": {
            "chat": "/chat",
            "retrieve": "/retrieve",
            "health": "/health",
            "reload": "/reload"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "rag_initialized": rag_chain is not None,
        "docs_directory": DOCS_DIRECTORY
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint for documentation questions
    """
    
    if not rag_chain or not retriever:
        raise HTTPException(
            status_code=503,
            detail="RAG system not initialized"
        )
    
    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )
    
    try:
        # Get retrieved documents if requested
        sources = None
        if request.include_sources:
            docs = retriever.invoke(request.message)
            sources = [
                RetrievedDocument(
                    content=doc.page_content[:200] + "...",  # Truncate for response
                    source=doc.metadata.get("source", "unknown"),
                    metadata=doc.metadata
                )
                for doc in docs
            ]
        
        # Get response from RAG chain
        response = rag_chain.invoke(request.message)
        
        return ChatResponse(
            response=response,
            sources=sources
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )


@app.post("/retrieve")
async def retrieve_documents(request: ChatRequest):
    """Retrieve relevant documentation chunks"""
    
    if not retriever:
        raise HTTPException(
            status_code=503,
            detail="Retriever not initialized"
        )
    
    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )
    
    try:
        docs = retriever.invoke(request.message)
        return {
            "query": request.message,
            "documents": [
                {
                    "content": doc.page_content,
                    "source": doc.metadata.get("source", "unknown"),
                    "metadata": doc.metadata
                }
                for doc in docs
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving documents: {str(e)}"
        )


@app.post("/reload")
async def reload_documentation():
    """Reload documentation files and rebuild vector store"""
    global rag_chain, retriever, vectorstore
    
    try:
        print("Reloading documentation...")
        rag_chain, retriever, vectorstore = setup_rag_chain(DOCS_DIRECTORY)
        return {"status": "success", "message": "Documentation reloaded successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error reloading documentation: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)