# AI Tutor API Server

This FastAPI server exposes the AI Tutor backend as an API endpoint.

## Setup

1. Navigate to the `back` directory:
```bash
cd back
```

2. Install required dependencies (if not already installed):
```bash
pip install fastapi uvicorn python-multipart
```

3. Make sure your `.env` file contains all the required environment variables for the agent to work:
   - `GEMINI_API_KEY`
   - `COHERE_API_KEY`
   - `QDRANT_URL`
   - `QDRANT_API_KEY`

## Running the Server

Run the server with uvicorn:
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `POST /ask` - Submit a query to the AI tutor
- `GET /health` - Health check endpoint

### Example Request:
```json
{
  "query": "What is physical AI?"
}
```

### Example Response:
```json
{
  "answer": "Physical AI refers to the integration of artificial intelligence with physical systems..."
}
```