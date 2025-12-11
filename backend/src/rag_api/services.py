# src/rag_api/services.py
import os
import logging
from typing import AsyncGenerator, List, Optional, Dict, Any
from uuid import uuid4
from dotenv import load_dotenv

import cohere
import trafilatura
import requests
import xml.etree.ElementTree as ET
from qdrant_client import QdrantClient, models
from fastapi.concurrency import run_in_threadpool


from .database.config import get_db
from .database.crud import create_document, get_document_by_url

# Import the existing agent
from .agent import main_agent, Runner

# --- Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()

# --- Environment & API Clients ---
def get_env_variable(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Environment variable '{key}' is not set.")
    return value

try:
    COHERE_API_KEY = get_env_variable("COHERE_API_KEY")
    QDRANT_URL = get_env_variable("QDRANT_URL")
    QDRANT_API_KEY = get_env_variable("QDRANT_API_KEY")

    cohere_client = cohere.Client(COHERE_API_KEY)
    qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    logging.info("Successfully connected to Cohere and Qdrant.")
except (ValueError, Exception) as e:
    logging.critical(f"Configuration error: {e}")
    raise

# --- Constants ---
COLLECTION_NAME = "humanoid_ai_book"
EMBED_MODEL_NAME = "embed-english-v3.0"
CHAT_MODEL_NAME = "command-r"
EMBED_VECTOR_SIZE = 1024
MAX_CHUNK_SIZE = 1800
CHUNK_OVERLAP = 200

# --- Qdrant Retrieval Functions ---

def get_embedding(text: str, input_type: str) -> Optional[List[float]]:
    """Generate embedding for text using Cohere."""
    try:
        resp = cohere_client.embed(
            model=EMBED_MODEL_NAME,
            input_type=input_type,
            texts=[text]
        )
        return resp.embeddings[0]
    except Exception as e:
        logging.error(f"Cohere embedding failed: {e}")
        return None


def retrieve_from_qdrant_sync(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """Retrieve relevant text from Qdrant (synchronous version)."""
    logging.info("--- Starting Qdrant Retrieval ---")

    query_vector = get_embedding(query, "search_query")
    if not query_vector:
        logging.error("Retrieval failed: Could not generate query embedding.")
        return []

    try:
        # Try different Qdrant client API approaches
        search_results = None

        # First, let's see what methods are actually available and working
        available_methods = [method for method in dir(qdrant_client) if 'search' in method.lower()]
        logging.info(f"Available search methods: {available_methods}")

        # Try different search methods
        if 'search' in available_methods:
            try:
                search_results = qdrant_client.search(
                    collection_name=COLLECTION_NAME,
                    query_vector=query_vector,
                    limit=top_k,
                    with_payload=True,
                )
                logging.info("Using search() method")
            except AttributeError:
                logging.info("search() method failed, trying alternative")

        if search_results is None and 'search_points' in available_methods:
            try:
                search_results = qdrant_client.search_points(
                    collection_name=COLLECTION_NAME,
                    vector=query_vector,
                    limit=top_k,
                    with_payload=True,
                )
                logging.info("Using search_points() method")
            except AttributeError:
                logging.info("search_points() method failed")

        # If still no results, try the async version if it exists
        if search_results is None and 'asearch' in available_methods:
            try:
                import asyncio
                search_results = asyncio.run(qdrant_client.asearch(
                    collection_name=COLLECTION_NAME,
                    query_vector=query_vector,
                    limit=top_k,
                    with_payload=True,
                ))
                logging.info("Using asearch() method")
            except (AttributeError, RuntimeError):
                logging.info("asearch() method failed")

        # If none of the above worked, log error and raise
        if search_results is None:
            raise AttributeError(f"No working search method found. Available: {available_methods}")

        logging.info(f"Length of retrieved results: {len(search_results)}")

        if not search_results:
            logging.warning("Qdrant search returned no documents.")
            return []

        results = []
        for res in search_results:
            if res.payload and "text" in res.payload:
                result = {
                    "id": res.id,
                    "score": res.score,
                    "text": res.payload["text"],
                    "url": res.payload.get("url", ""),
                    "metadata": res.payload
                }
                results.append(result)

        logging.info("--- Qdrant Retrieval Finished ---")
        return results

    except Exception as e:
        logging.error(f"Qdrant search failed: {e}")
        return []


async def retrieve_from_qdrant(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """Retrieve relevant text from Qdrant (async wrapper)."""
    return await run_in_threadpool(retrieve_from_qdrant_sync, query, top_k)


async def query_gemini_agent(query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
    """Query the existing agent with context retrieved from Qdrant."""
    logging.info("--- Starting Agent Query with Qdrant Retrieval ---")

    # Retrieve relevant context from Qdrant
    retrieval_results = await retrieve_from_qdrant(query, top_k=5)
    retrieved_context = "\n---\n".join([res["text"] for res in retrieval_results])

    # Prepare the query for the agent with retrieved context
    if retrieved_context:
        full_query = f"Context:\n{retrieved_context}\n\nQuestion: {query}\n\nPlease answer based only on the provided context."
    else:
        full_query = f"Context:\n[No relevant content found in the textbook]\n\nQuestion: {query}\n\nPlease state that you could not find relevant information in the provided textbook content to answer this question."
        logging.warning("No context retrieved from Qdrant, informing user that information is not available.")

    try:
        # Run the existing agent with the query (using async execution to avoid event loop issues)
        import asyncio
        if asyncio.is_event_loop_running():
            # If we're already in an event loop, run in a separate thread
            import concurrent.futures
            import threading
            loop = asyncio.get_event_loop()

            def run_agent():
                return Runner.run_sync(main_agent, full_query)

            result = await loop.run_in_executor(None, run_agent)
        else:
            # If no event loop is running, we can call sync normally
            result = Runner.run_sync(main_agent, full_query)

        response = result.final_output if result.final_output else "I couldn't generate a response for your query."

        logging.info("--- Agent Query with Qdrant Retrieval Finished ---")

        return {
            "response": response,
            "sources": retrieval_results,  # Return the source documents
            "context": context or {}
        }
    except Exception as e:
        logging.error(f"Agent query with Qdrant retrieval failed: {e}")
        return {
            "response": "Error: The AI agent failed to process your query.",
            "sources": [],
            "context": context or {}
        }


def retrieve(query: str) -> Optional[str]:
    """Retrieve relevant text from Qdrant (legacy function for compatibility)."""
    logging.info("--- Starting Legacy Retrieval ---")

    query_vector = get_embedding(query, "search_query")
    if not query_vector:
        logging.error("Retrieval failed: Could not generate query embedding.")
        return None

    try:
        # Try different Qdrant client API approaches
        search_results = None

        # First, let's see what methods are actually available and working
        available_methods = [method for method in dir(qdrant_client) if 'search' in method.lower()]
        logging.info(f"Available search methods: {available_methods}")

        # Try different search methods
        if 'search' in available_methods:
            try:
                search_results = qdrant_client.search(
                    collection_name=COLLECTION_NAME,
                    query_vector=query_vector,
                    limit=5,
                    with_payload=True,
                )
                logging.info("Using search() method")
            except AttributeError:
                logging.info("search() method failed, trying alternative")

        if search_results is None and 'search_points' in available_methods:
            try:
                search_results = qdrant_client.search_points(
                    collection_name=COLLECTION_NAME,
                    vector=query_vector,
                    limit=5,
                    with_payload=True,
                )
                logging.info("Using search_points() method")
            except AttributeError:
                logging.info("search_points() method failed")

        # If still no results, try the async version if it exists
        if search_results is None and 'asearch' in available_methods:
            try:
                import asyncio
                search_results = asyncio.run(qdrant_client.asearch(
                    collection_name=COLLECTION_NAME,
                    query_vector=query_vector,
                    limit=5,
                    with_payload=True,
                ))
                logging.info("Using asearch() method")
            except (AttributeError, RuntimeError):
                logging.info("asearch() method failed")

        # If none of the above worked, log error and raise
        if search_results is None:
            raise AttributeError(f"No working search method found. Available: {available_methods}")

        logging.info(f"Length of retrieved results: {len(search_results)}")

        if not search_results:
            logging.warning("Qdrant search returned no documents.")
            return None

        chunks = [
            res.payload["text"]
            for res in search_results
            if res.payload and "text" in res.payload
        ]

        final_context = "\n---\n".join(chunks)
        logging.info("--- Legacy Retrieval Finished ---")

        return final_context if chunks else None

    except Exception as e:
        logging.error(f"Qdrant search failed: {e}")
        return None


# ============================
# ✅ FIXED FUNCTION - Streaming version using Cohere with Qdrant context
# ============================
async def get_rag_response(query: str) -> AsyncGenerator[str, None]:
    """Main RAG streaming logic using Cohere with Qdrant context."""
    # Retrieve relevant context from Qdrant
    retrieval_results = await retrieve_from_qdrant(query, top_k=5)
    retrieved_context = "\n---\n".join([res["text"] for res in retrieval_results])

    # Prepare the query with retrieved context
    if retrieved_context:
        message = f"Context:\n{retrieved_context}\n---\n\nQuestion: {query}\n\nPlease answer based only on the provided context."
    else:
        message = f"Context:\n[No relevant content found in the textbook]\n---\n\nQuestion: {query}\n\nPlease state that you could not find relevant information in the provided textbook content to answer this question."
        logging.warning("No context retrieved from Qdrant, informing user that information is not available.")

    system_prompt = (
        "You are an expert AI tutor for robotics and AI. Answer the user's question based only on the provided context. "
        "If the context doesn't contain the answer, say so."
    )

    logging.info(f"Final prompt contains retrieved text: {bool(retrieved_context)}")

    try:
        async for event in cohere_client.chat(
            message=message,
            model=CHAT_MODEL_NAME,
            preamble=system_prompt,
            stream=True
        ):
            if event.event_type == "text-generation":
                yield event.text

    except Exception as e:
        logging.error(f"Cohere chat stream with Qdrant context failed: {e}")
        yield "Error: The AI chat service failed."


# --- Ingestion Logic ---

def chunk_text(text: str) -> List[str]:
    """Chunk long text into overlapping blocks."""
    chunks = []

    while len(text) > MAX_CHUNK_SIZE:
        split_pos = text[:MAX_CHUNK_SIZE].rfind(". ")
        if split_pos == -1:
            split_pos = MAX_CHUNK_SIZE

        chunks.append(text[:split_pos + 1])
        text = text[max(0, split_pos + 1 - CHUNK_OVERLAP):]

    chunks.append(text)
    return [c for c in chunks if c.strip()]


def ingest_book_data(sitemap_url: str):
    """Ingest all pages from sitemap and upload to Qdrant, storing metadata in database."""
    logging.info("--- Starting Ingestion ---")

    try:
        qdrant_client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=EMBED_VECTOR_SIZE,
                distance=models.Distance.COSINE
            ),
        )
    except Exception as e:
        logging.error(f"Failed to create Qdrant collection: {e}")
        return

    try:
        resp = requests.get(sitemap_url, timeout=30)
        resp.raise_for_status()
        root = ET.fromstring(resp.content)
        urls = [
            child.findtext("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
            for child in root
            if child.findtext("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        ]
    except Exception as e:
        logging.error(f"Failed to fetch or parse sitemap: {e}")
        return

    points_to_upsert = []
    total_chunks = 0

    # Process each URL and store metadata in database
    for url in urls:
        html = trafilatura.fetch_url(url)
        text = trafilatura.extract(html, include_links=False) if html else ""

        if not text:
            logging.warning(f"Could not extract text from {url}")
            continue

        # Store document metadata in database
        with next(get_db()) as db:
            try:
                # Extract title from HTML if available
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(html, 'html.parser')
                title = soup.title.string if soup.title else url.split('/')[-1] or "Untitled"

                # Create document record
                doc = create_document(db, url=url, title=title, content=text[:1000] + "..." if len(text) > 1000 else text)  # Store truncated content
                logging.info(f"Stored document metadata for {url} with ID {doc.id}")
            except Exception as e:
                logging.error(f"Failed to store document metadata for {url}: {e}")
                # Continue processing even if database storage fails

        chunks = chunk_text(text)
        total_chunks += len(chunks)

        for chunk in chunks:
            vector = get_embedding(chunk, "search_document")
            if vector:
                points_to_upsert.append(
                    models.PointStruct(
                        id=str(uuid4()),
                        vector=vector,
                        payload={"url": url, "text": chunk}
                    )
                )

    if points_to_upsert:
        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=points_to_upsert,
            wait=True
        )

    logging.info(f"Upserted {len(points_to_upsert)} vectors from {len(urls)} URLs.")
    logging.info(f"Total chunks processed: {total_chunks}")

    try:
        final_count = qdrant_client.get_collection(collection_name=COLLECTION_NAME).points_count
        logging.info(f"Verification — Qdrant total points: {final_count}")
    except Exception as e:
        logging.error(f"Verification failed: {e}")
