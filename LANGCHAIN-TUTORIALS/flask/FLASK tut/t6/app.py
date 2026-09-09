from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import random
import time
import threading

# 1. Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

# 2. Initialize SocketIO with the Flask app
# The 'cors_allowed_origins="*"' allows connections from any origin (useful for testing)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    """Route to serve the main dashboard page."""
    return render_template('index.html')

# -------------------------------------------------------------------------
# SOCKET.IO EVENT HANDLERS
# -------------------------------------------------------------------------

@socketio.on('connect')
def handle_connect():
    """Triggered when a new client connects."""
    print("Client connected")
    # Send a welcome message to the newly connected client
    emit('server_response', {'data': 'Connected to Server via WebSockets!'})

@socketio.on('disconnect')
def handle_disconnect():
    """Triggered when a client disconnects."""
    print("Client disconnected")

@socketio.on('client_message')
def handle_client_message(json):
    """
    Triggered when the client sends a message with the event name 'client_message'.
    'json' contains the data sent by the client.
    """
    print(f"Received message from client: {json}")
    
    # Broadcast the received message to ALL connected clients (including the sender)
    # The 'broadcast=True' parameter makes this possible.
    emit('server_response', {
        'data': f"Broadcast from {json['user']}: {json['message']}"
    }, broadcast=True)

# -------------------------------------------------------------------------
# BACKGROUND TASK (SIMULATING LIVE UPDATES)
# -------------------------------------------------------------------------

def background_thread():
    """
    A separate thread that sends random data to all clients every 5 seconds.
    This simulates live server-side data (like stock prices or sensor readings).
    """
    while True:
        socketio.sleep(5)  # Use socketio.sleep instead of time.sleep
        random_value = random.randint(1, 100)
        print(f"Sending background update: {random_value}")
        
        # Emit a 'live_update' event to all clients
        socketio.emit('live_update', {'value': random_value})

# Start the background thread when the script runs
# We use a daemon thread so it dies when the main program stops
thread = threading.Thread(target=background_thread, daemon=True)
thread.start()

if __name__ == '__main__':
    # Use socketio.run instead of app.run for WebSocket support
    print("Starting WebSocket Server on http://127.0.0.1:5000")
    socketio.run(app, debug=True)
