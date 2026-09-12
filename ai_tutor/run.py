"""
Single-command launcher for AI Personal Tutor.
==============================================
Runs the FastAPI server with the LangGraph state machine backend
and serves the modern web interface at http://localhost:8000.
"""

import os
import sys
import uvicorn

# Add current and parent directory to sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

for path in [CURRENT_DIR, PROJECT_ROOT]:
    if path not in sys.path:
        sys.path.insert(0, path)

if __name__ == "__main__":
    print("=" * 70)
    print("  AI PERSONAL TUTOR - POWERED BY LANGGRAPH & FASTAPI")
    print("=" * 70)
    print("  -> Web Interface: http://localhost:8000")
    print("  -> API Swagger Docs: http://localhost:8000/docs")
    print("  -> Architecture: LangGraph StateGraph with MemorySaver Checkpointing")
    print("=" * 70)
    
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
