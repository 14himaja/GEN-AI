"""
Entrypoint for AI Personal Tutor FastAPI application.
Allows running:
    uvicorn main:app --reload --port 8000
directly from the ai_tutor/ directory.
"""

import os
import sys

# Ensure both ai_tutor and parent directories are in python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

for path in [CURRENT_DIR, PARENT_DIR]:
    if path not in sys.path:
        sys.path.insert(0, path)

# Import the FastAPI application
from ai_tutor.api.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
