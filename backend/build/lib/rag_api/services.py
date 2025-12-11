import os
from dotenv import load_dotenv
import requests
import xml.etree.ElementTree as ET
import trafilatura
from uuid import uuid4

# Load environment variables from .env file
load_dotenv()

from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    AsyncOpenAI,
    function_tool,
    set_tracing_disabled,
)
import cohere
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

# Disable tracing for the agents library
set_tracing_disabled(disabled=True)

# --- Client Initialization ---

# Cohere client for embeddings
cohere_api_key = os.getenv("COHERE_API_KEY")
cohere_client = cohere.Client(cohere_api_key)

# Qdrant client for vector database
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

# OpenAI-compatible client pointing to Cohere for generation
provider = AsyncOpenAI(
    api_key=cohere_api_key,
    base_url="https://api.cohere.ai/compatibility/v1"
)

# --- Model Configuration ---

# Generation model using Cohere's command-r-plus via the OpenAI compatibility layer
generation_model = OpenAIChatCompletionsModel(
    model="command-r-plus",  # Using a known powerful model
    openai_client=provider
)

# Embedding model details
EMBED_MODEL_NAME = "embed-english-v3.0"
COLLECTION_NAME = "humanoid_ai_book"


# --- Core Functions ---

def get_embedding(text: str, input_type: str) -> list[float]:
    """Generates an embedding for the given text using Cohere."""
    resp = cohere_client.embed(
        model=EMBED_MODEL_NAME,
        input_type=input_type,
        texts=[text],
    )
    return resp.embeddings[0]

# --- Agent Tool Definition ---

@function_tool
def retrieve(query: str) -> str:
    """
    Retrieve relevant text chunks from the vector database based on the user's query.
    """
    query_embedding = get_embedding(query, "search_query")
    
    results = qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=5,
    )
    
    chunks = [point.payload.get("text", "") for point in results]
    if not chunks:
        return "No relevant content was found in the textbook for your query."
        
    return "\n---\n".join(chunks)

# --- Agent Definition ---

rag_agent = Agent(
    name="RAG Tutor",
    instructions=(
        "You are a helpful AI tutor for the Physical AI Textbook."
        "Your primary function is to answer questions based on the textbook's content. "
        "1. ALWAYS call the `retrieve` tool with the user's question to get relevant content from the textbook. "
        "2. Use ONLY the retrieved content to formulate your answer. "
        "3. If the retrieved content does not contain the answer, you MUST state 'I could not find an answer to that in the textbook.' "
        "4. Do not use any prior knowledge. Your knowledge is strictly limited to the information provided by the `retrieve` tool. "
        "5. Be concise and directly answer the question."
    ),
    model=generation_model,
    tools=[retrieve]
)

# --- Service Function ---

async def get_rag_response(query: str, selected_text: str | None = None) -> AsyncGenerator[str, None]:
    """
    Runs the RAG agent to get a response to a user's query and streams the output.
    
    Args:
        query: The user's question.
        selected_text: Optional text selected by the user in the UI to provide extra context.
        
    Yields:
        The partial responses from the agent as strings.
    """
    # If user has selected text, prepend it to the query as context
    if selected_text:
        prompt = f"Using the following context: '{selected_text}', answer this question: '{query}'"
    else:
        prompt = query

    # Run the agent asynchronously and stream the response
    result = await Runner.run(agent=rag_agent, input=prompt, stream=True)
    
    # Stream partial outputs
    async for partial_output in result.stream_partial_output():
        yield partial_output

    # Ensure there's a final output, though we prioritize the stream
    final_output = await result.get_final_output()
    if not final_output:
        # If the stream was empty and there's no final output
        yield "I am sorry, but I was unable to process your request."

# --- Ingestion Service ---

def _get_all_urls(sitemap_url: str) -> list[str]:
    """Extracts all URLs from a given sitemap.xml URL."""
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()
        root = ET.fromstring(response.text)
        urls = [
            child.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text
            for child in root
            if child.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc") is not None
        ]
        print(f"Found {len(urls)} URLs in sitemap.")
        return urls
    except requests.RequestException as e:
        print(f"Error fetching sitemap: {e}")
        return []

def _extract_text_from_url(url: str) -> str:
    """Extracts the main content from a URL."""
    html = trafilatura.fetch_url(url)
    text = trafilatura.extract(html)
    if not text:
        print(f"[Warning] No text extracted from: {url}")
    return text or ""

def _chunk_text(text: str, max_chars: int = 1200) -> list[str]:
    """Chunks text into smaller pieces."""
    chunks = []
    while len(text) > max_chars:
        split_pos = text[:max_chars].rfind(". ")
        if split_pos == -1:
            split_pos = max_chars
        chunks.append(text[:split_pos])
        text = text[split_pos:]
    if text.strip():
        chunks.append(text)
    return chunks

async def ingest_book_data(sitemap_url: str):
    """The main ingestion pipeline service function."""
    print("\n--- Starting Ingestion Process ---")
    
    # 1. Create collection
    print(f"Recreating Qdrant collection: '{COLLECTION_NAME}'")
    qdrant_client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
    )
    
    # 2. Get URLs
    urls = _get_all_urls(sitemap_url)
    if not urls:
        print("No URLs to process. Aborting ingestion.")
        return

    points_to_upsert = []
    for url in urls:
        print(f"Processing: {url}")
        text = _extract_text_from_url(url)
        if not text or not text.strip():
            continue
        
        chunks = _chunk_text(text)
        for chunk in chunks:
            vector = get_embedding(chunk, "search_document")
            point_id = str(uuid4())
            points_to_upsert.append(
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload={"url": url, "text": chunk, "chunk_id": point_id}
                )
            )
    
    # 3. Batch upsert to Qdrant
    if points_to_upsert:
        print(f"Upserting {len(points_to_upsert)} points to Qdrant...")
        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=points_to_upsert,
            wait=True
        )
        print("✔️ Batch upsert completed!")
    
    print(f"\n✔️ Ingestion finished. Total chunks stored: {len(points_to_upsert)}")

