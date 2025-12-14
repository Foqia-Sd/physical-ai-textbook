from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
    function_tool
)
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
# from agents import enable_verbose_stdout_logging

# enable_verbose_stdout_logging()


# -----------------------------------------
# Setup
# -----------------------------------------
load_dotenv()
set_tracing_disabled(True)


# Gemini (OpenAI-Compatible) Client
client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Model (Gemini)
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",     # Model name you are using
    openai_client=client
)

import cohere
from qdrant_client import QdrantClient

cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))

# Connect to Qdrant
qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

def get_embedding(text):
    """Get embedding vector from Cohere Embed v3"""
    response = cohere_client.embed(
        model="embed-english-v3.0",
        input_type="search_query",  # Use search_query for queries
        texts=[text],
    )
    return response.embeddings[0]  # Return the first embedding

@function_tool
def retrieve(query):
    embedding = get_embedding(query)
    result = qdrant.query_points(
        collection_name="humanoid_ai_book",
        query=embedding,
        limit=5
    )
    return [point.payload["text"] for point in result.points]


# -----------------------------------------
# MAIN AI AGENT (Project-Specific)
# -----------------------------------------
agent = Agent(
    name="AI Tutor",
    instructions="""
You are an AI tutor for the Physical AI & Humanoid Robotics textbook.
To answer the user question, first call the tool `retrieve` with the user query.
Use ONLY the returned content from `retrieve` to answer.
If the answer is not in the retrieved content, say "I am unable to find the answer in the provided context.".
""",
    model=model,
    tools=[retrieve]  # Tools added
)
