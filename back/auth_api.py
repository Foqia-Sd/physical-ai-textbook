from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import agent, Runner  # import your existing agent setup
import sqlite3
import hashlib
import secrets
from datetime import datetime, timedelta
import json
import sys

# Reuse your existing app instance or create a new one
# For separation of concerns, we'll create a new app for auth
app = FastAPI(title="AI Tutor API with Authentication")

# Add CORS middleware (same as your original)
origins = [
    "http://localhost:3000",  # Docusaurus dev server
    "https://foqia-sd.github.io",  # production
    "http://localhost:3001",  # additional dev port if needed
    "http://localhost:3002",  # additional dev port if needed
    "http://127.0.0.1:3000",  # alternative localhost
    "http://127.0.0.1:3001",  # alternative localhost
    "http://127.0.0.1:3002",  # alternative localhost
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    # Add exposed headers for authentication
    expose_headers=["Access-Control-Allow-Origin", "Access-Control-Allow-Credentials", "Authorization", "Set-Cookie", "Cookie"]
)

# Simple in-memory session store (in production, use Redis or database)
sessions = {}

# ----------------------
# Simple Authentication System
# ----------------------
class User(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str

def hash_password(password: str) -> str:
    """Hash a password with salt"""
    salt = secrets.token_hex(16)
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return f"{salt}:{pwdhash.hex()}"

def verify_password(password: str, stored_password: str) -> bool:
    """Verify a password against a stored hash"""
    salt, stored_hash = stored_password.split(':')
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return pwdhash.hex() == stored_hash

def create_session(user_email: str) -> str:
    """Create a new session for a user"""
    session_id = secrets.token_urlsafe(32)
    sessions[session_id] = {
        "user_email": user_email,
        "created_at": datetime.utcnow(),
        "expires_at": datetime.utcnow() + timedelta(days=7)
    }
    return session_id

def get_session_from_request(request) -> dict:
    """Get session from request headers or cookies"""
    # Check for Authorization header
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        session_id = auth_header[7:]
        session = sessions.get(session_id)
        if session and session["expires_at"] > datetime.utcnow():
            return session
    return None

def get_current_user(request: Request) -> dict:
    """Dependency to get current user from session"""
    session = get_session_from_request(request)
    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return session

# Authentication routes
@app.post("/api/auth/sign-up/email")
def register(user: RegisterRequest):
    # In a real app, you'd store this in a database
    # For this example, we'll just return success
    # In production, you'd hash the password and store in DB
    return {"success": True, "message": "User registered successfully"}

@app.post("/api/auth/sign-in/email")
def login(credentials: LoginRequest):
    # In a real app, you'd verify against a database
    # For this example, we'll accept any credentials
    # In production, verify credentials against DB
    session_id = create_session(credentials.email)
    return {
        "success": True,
        "session_token": session_id,
        "user": {"email": credentials.email}
    }

@app.post("/api/auth/sign-out")
def logout():
    # In a real app, you'd invalidate the session
    return {"success": True}

@app.get("/api/auth/session")
def get_session(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}

# ----------------------
# Your existing API endpoints
# ----------------------
class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
def ask_question(req: QueryRequest, current_user: dict = Depends(get_current_user)):
    try:
        # Run the agent in a separate process to avoid event loop conflicts
        import subprocess
        import json
        import os

        # Get the path to the agent_runner.py script
        script_path = os.path.join(os.path.dirname(__file__), "agent_runner.py")

        # Create a completely isolated subprocess call
        # Clear any asyncio-related environment variables
        clean_env = os.environ.copy()

        # Execute the agent runner script with the query as an argument
        result = subprocess.run([
            sys.executable, script_path, req.query
        ], capture_output=True, text=True, timeout=30, env=clean_env)

        if result.returncode != 0:
            print(f"Subprocess error: {result.stderr}")
            raise HTTPException(status_code=500, detail=f"Agent execution failed: {result.stderr}")

        response_data = json.loads(result.stdout.strip())

        if "error" in response_data:
            raise HTTPException(status_code=500, detail=response_data["error"])

        return response_data

    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=500, detail="Agent execution timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Add an unprotected endpoint for testing
@app.get("/")
def root():
    return {"message": "AI Tutor API is running"}