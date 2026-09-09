from flask import Flask, render_template, Response
import time
import random

app = Flask(__name__)

# -------------------------------------------------------------------------
# GENERATOR FUNCTION (The Core of Streaming)
# -------------------------------------------------------------------------

def generate_ai_response(prompt):
    """
    Simulates an LLM (like GPT-4) generating text word by word.
    In a real app, this would be your model.generate() loop.
    """
    full_text = f"As an AI, I have analyzed your prompt: '{prompt}'. Here is a detailed response generated token-by-token to demonstrate streaming efficiency..."
    
    words = full_text.split()
    
    for word in words:
        # We yield each word as it is 'generated'
        # The 'data: ' prefix and '\n\n' suffix are standard for Server-Sent Events (SSE)
        yield f"data: {word} \n\n"
        
        # Simulate the time it takes for a model to think/generate
        time.sleep(random.uniform(0.1, 0.3))

# -------------------------------------------------------------------------
# FLASK ROUTES
# -------------------------------------------------------------------------

@app.route('/')
def index():
    """Serves the main chat-like interface."""
    return render_template('index.html')

@app.route('/stream')
def stream():
    """
    The endpoint that returns a Streaming Response.
    mimetype='text/event-stream' tells the browser to keep the connection open.
    """
    prompt = "Tell me about Web Streaming"
    
    # We return a Response object initialized with our generator
    return Response(generate_ai_response(prompt), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)
