"""
STREAMING RESPONSES FOR AI/ML (t8)
==================================

WHY STREAMING IS CRITICAL FOR AI:
-------------------------------
Large Language Models (LLMs) take time to generate full responses.
- If you wait for the whole answer (e.g., 30 seconds), the user thinks the app is broken.
- If you STREAM the tokens word-by-word, the user starts reading IMMEDIATELY.

CONCEPTS IN THIS TUTORIAL:
--------------------------
1. GENERATOR FUNCTIONS:
   Python functions using the 'yield' keyword. They don't return one value; 
   they "produce" a sequence of values over time.

2. SERVER-SENT EVENTS (SSE):
   A standard that allows the server to push data to the web page over a 
   single HTTP connection.
   - Requirement 1: mimetype must be 'text/event-stream'.
   - Requirement 2: Data must follow the format 'data: your_message \n\n'.

3. BROWSER EVENTSOURCE:
   The built-in JavaScript API (`new EventSource('/url')`) that handles the 
   streaming connection automatically.

HOW TO RUN:
-----------
1. cd t8
2. python app.py
3. Open http://127.0.0.1:5000 in your browser.
4. Click the button and watch the "AI" generate text word-by-word.

NOTE FOR PRODUCTION:
--------------------
Standard Flask development server handles streaming well, but production servers 
like Gunicorn need specific configurations (e.g., --worker-class gevent) to 
prevent blocking other users while one user is streaming.
"""

def get_summary():
    return "Streaming uses generators and SSE to deliver AI output token-by-token."
