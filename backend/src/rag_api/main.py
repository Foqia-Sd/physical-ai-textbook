# src/rag_api/main.py
import logging
from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Any
from src.rag_api.services import get_rag_response, ingest_book_data, retrieve_from_qdrant, query_gemini_agent

from src.rag_api.database.config import get_db_dependency
from src.rag_api.database.crud import get_all_documents, get_highlights_by_document
from src.rag_api.database.models import Document as DocumentModel

# --- App Initialization & Logging ---
from src.rag_api.database.models import create_tables

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
app = FastAPI(
    title="Physical AI Textbook RAG API",
    description="A resilient, non-blocking RAG chatbot.",
    version="1.2.0",
)

@app.on_event("startup")
async def startup_event():
    """Create database tables on startup."""
    logging.info("Initializing database tables...")
    create_tables()
    logging.info("Database tables initialized successfully.")

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Models ---
class ChatQuery(BaseModel):
    query: str

class QueryRequest(BaseModel):
    query: str
    context: Optional[Dict] = None

class QueryResponse(BaseModel):
    query: str
    response: str
    sources: List[Dict[str, Any]]
    context: Optional[Dict[str, Any]]

class RetrieveRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5

class RetrieveResponse(BaseModel):
    query: str
    results: List[Dict[str, Any]]

class IngestRequest(BaseModel):
    sitemap_url: HttpUrl

class DocumentResponse(BaseModel):
    id: int
    url: str
    title: str
    created_at: str

    class Config:
        from_attributes = True

class HighlightResponse(BaseModel):
    id: int
    document_id: int
    text: str
    start_char: int
    end_char: int
    metadata: Optional[str]
    created_at: str

    class Config:
        from_attributes = True

# --- API Endpoints ---
@app.get("/health", summary="Health Check")
async def health():
    """Provides a simple health check endpoint to confirm the service is running."""
    return {"status": "ok"}

@app.post("/retrieve", summary="Retrieve relevant documents from Qdrant")
async def retrieve(request: RetrieveRequest):
    """
    Retrieve relevant documents from Qdrant based on the query.
    """
    try:
        logging.info(f"Received retrieve request: '{request.query}'")
        results = await retrieve_from_qdrant(request.query, request.top_k)

        logging.info(f"Retrieved {len(results)} results from Qdrant")
        return RetrieveResponse(
            query=request.query,
            results=results
        )
    except Exception as e:
        logging.error(f"Critical error in /retrieve endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected server error occurred.")

@app.post("/query", summary="Query the Gemini agent with Qdrant retrieval")
async def query(request: QueryRequest):
    """
    Query the Gemini agent with context retrieved from Qdrant.
    """
    try:
        logging.info(f"Received query request: '{request.query}'")
        response = await query_gemini_agent(request.query, request.context)

        logging.info(f"Generated response with {len(response['sources'])} sources")
        return QueryResponse(
            query=request.query,
            response=response['response'],
            sources=response['sources'],
            context=response.get('context', {})
        )
    except Exception as e:
        logging.error(f"Critical error in /query endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected server error occurred.")

@app.post("/chat", summary="Get a RAG answer (non-streaming)")
async def chat(chat_query: ChatQuery):
    """
    Receives a query, retrieves context from Qdrant, and returns a single, complete answer using the agent.
    """
    try:
        logging.info(f"Received non-streaming chat query: '{chat_query.query}'")
        # Use the agent with Qdrant context for consistent behavior
        response = await query_gemini_agent(chat_query.query, context=None)
        final_answer = response['response']

        logging.info(f"Final assembled answer: '{final_answer[:200]}...'")
        return {"answer": final_answer, "sources": response['sources']}

    except Exception as e:
        logging.error(f"Critical error in /chat endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected server error occurred.")

@app.post("/chat/stream", summary="Get a streaming RAG answer")
async def chat_stream(chat_query: ChatQuery):
    """
    Receives a query and streams the response back token by token.
    This correctly returns a StreamingResponse with the async generator.
    """
    logging.info(f"Received streaming chat query: '{chat_query.query}'")
    try:
        # Note: For streaming, we return just the response tokens
        # Sources would need to be handled differently in a streaming context
        return StreamingResponse(
            get_rag_response(chat_query.query),
            media_type="text/event-stream"
        )
    except Exception as e:
        logging.error(f"Error starting stream for query '{chat_query.query}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to start the chat stream.")

@app.post("/ingest", summary="Start content ingestion")
async def ingest(request: IngestRequest, background_tasks: BackgroundTasks):
    """Triggers a background task to ingest and vectorize content from a sitemap."""
    background_tasks.add_task(ingest_book_data, str(request.sitemap_url))
    return {
        "status": "success",
        "message": f"Ingestion job started in the background for {request.sitemap_url}"
    }

# --- Database Endpoints ---
@app.get("/documents", response_model=List[DocumentResponse], summary="Get all documents")
async def get_documents(db=Depends(get_db_dependency)):
    """Retrieve all documents from the database."""
    try:
        documents = get_all_documents(db)
        # Convert datetime objects to strings for JSON serialization
        result = []
        for doc in documents:
            doc_dict = {
                "id": doc.id,
                "url": doc.url,
                "title": doc.title,
                "created_at": doc.created_at.isoformat(),
            }
            if hasattr(doc, 'updated_at') and doc.updated_at:
                doc_dict["updated_at"] = doc.updated_at.isoformat()
            result.append(DocumentResponse(**doc_dict))
        return result
    except Exception as e:
        logging.error(f"Error retrieving documents: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve documents")

@app.get("/documents/{document_id}/highlights", response_model=List[HighlightResponse], summary="Get highlights for a document")
async def get_document_highlights(document_id: int, db=Depends(get_db_dependency)):
    """Retrieve all highlights for a specific document."""
    try:
        highlights = get_highlights_by_document(db, document_id)
        # Convert datetime objects to strings for JSON serialization
        result = []
        for highlight in highlights:
            hl_dict = {
                "id": highlight.id,
                "document_id": highlight.document_id,
                "text": highlight.text,
                "start_char": highlight.start_char,
                "end_char": highlight.end_char,
                "metadata": highlight.metadata,
                "created_at": highlight.created_at.isoformat(),
            }
            result.append(HighlightResponse(**hl_dict))
        return result
    except Exception as e:
        logging.error(f"Error retrieving highlights for document {document_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve highlights for document {document_id}")

