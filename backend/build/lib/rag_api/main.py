from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from .services import get_rag_response, ingest_book_data

app = FastAPI(
    title="Physical AI Textbook RAG API",
    description="API for the AI-Native Physical AI Textbook chatbot.",
    version="0.1.0",
)

# --- CORS Middleware ---
# Allow requests from any origin for development purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Pydantic Models ---

class ChatQuery(BaseModel):
    query: str
    selected_text: str | None = None

class IngestRequest(BaseModel):
    sitemap_url: HttpUrl

# --- API Endpoints ---

@app.get("/health")
async def health():
    """Check if the server is running."""
    return {"status": "ok"}

@app.post("/chat")
async def chat(chat_query: ChatQuery):
    """
    Receive a query, stream the RAG agent's response.
    """
    return StreamingResponse(
        get_rag_response(
            query=chat_query.query,
            selected_text=chat_query.selected_text
        ),
        media_type="text/event-stream"
    )

@app.post("/ingest")
async def ingest(request: IngestRequest, background_tasks: BackgroundTasks):
    """
    Trigger the ingestion process for a given sitemap URL.
    This runs as a background task.
    """
    background_tasks.add_task(ingest_book_data, str(request.sitemap_url))
    return {
        "status": "success",
        "message": f"Ingestion process started in the background for {request.sitemap_url}."
    }
