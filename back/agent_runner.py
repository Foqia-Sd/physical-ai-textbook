#!/usr/bin/env python3
"""
Separate script to run the agent without event loop conflicts
"""
import sys
import os
import json
import importlib.util

# Add the back directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_agent_query(query):
    """Run the agent query in an isolated environment"""
    # Import only after path is set
    from agent import agent, Runner

    try:
        result = Runner.run_sync(agent, input=query)
        return {"answer": result.final_output}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(json.dumps({"error": "Usage: python agent_runner.py '<query>'"}))
        sys.exit(1)

    query = sys.argv[1]
    result = run_agent_query(query)
    print(json.dumps(result))