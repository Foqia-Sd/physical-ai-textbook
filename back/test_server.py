#!/usr/bin/env python3
"""
Test script to start the authentication server and test the API endpoints
"""
import subprocess
import time
import requests
import threading
from auth_api import app

def start_server():
    """Start the FastAPI server in a separate thread"""
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)

def test_endpoints():
    """Test the API endpoints after server starts"""
    time.sleep(3)  # Wait for server to start

    print("Testing endpoints...")

    # Test health check
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")

    # Test root endpoint
    try:
        response = requests.get("http://localhost:8000/")
        print(f"Root endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Root endpoint failed: {e}")

    # Test OPTIONS request to /ask (preflight)
    try:
        response = requests.options("http://localhost:8000/ask",
                                   headers={
                                       "Origin": "http://localhost:3000",
                                       "Access-Control-Request-Method": "POST",
                                       "Access-Control-Request-Headers": "Content-Type"
                                   })
        print(f"OPTIONS /ask: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
    except Exception as e:
        print(f"OPTIONS /ask failed: {e}")

    # Test POST request to /ask (without authentication)
    try:
        response = requests.post("http://localhost:8000/ask",
                                json={"query": "test query"},
                                headers={"Content-Type": "application/json"})
        print(f"POST /ask: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"POST /ask failed: {e}")

if __name__ == "__main__":
    # Start server in background thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Test endpoints
    test_endpoints()

    print("Tests completed. Server is still running...")
    print("You can test authentication by registering/logging in at http://localhost:8000/api/auth/register")
    print("Or test with curl commands like:")
    print("curl -X POST http://localhost:8000/api/auth/register -H 'Content-Type: application/json' -d '{\"email\":\"test@example.com\", \"password\":\"password123\"}'")