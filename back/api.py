from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import agent, Runner  # import your existing agent setup

# ----------------------
# FastAPI Setup
# ----------------------
app = FastAPI(title="AI Tutor API")

# Allow requests from your frontend
origins = [
    "http://localhost:3000",  # Docusaurus dev server
    "https://your-docusaurus-site.com",  # production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------
# Request Model
# ----------------------
class QueryRequest(BaseModel):
    query: str

# ----------------------
# Endpoint
# ----------------------
@app.post("/ask")
def ask_question(req: QueryRequest):
    try:
        result = Runner.run_sync(agent, input=req.query)
        return {"answer": result.final_output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
