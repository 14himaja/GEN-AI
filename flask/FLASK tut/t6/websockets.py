"""
WEB SOCKETS CONCEPT EXPLAINED
==============================

WebSockets provide a persistent connection between a client and a server 
that both parties can use to start sending data at any time.

1. HOW IT DIFFERS FROM HTTP:
   - HTTP: Client asks -> Server answers -> Connection closes. (Like a letter)
   - WebSockets: Connection opens -> Both talk freely -> Connection closes later. (Like a phone call)

2. CORE CONCEPTS IN FLASK-SOCKETIO:
   - Event: A named message (e.g., 'connect', 'message', 'my_custom_event').
   - Emit: Sending a message to one or more clients.
   - Broadcast: Sending a message to EVERYONE currently connected.
   - Namespace: A way to separate logic within a single connection (like different rooms).

3. SERVER-SIDE CODE STRUCTURE (t6/app.py):
   - socketio.on('event_name'): Listens for messages from the client.
   - socketio.emit('event_name', data): Sends data to the client.

4. CLIENT-SIDE CODE STRUCTURE (t6/static/js/main.js):
   - socket.on('event_name', function): Listens for server messages.
   - socket.emit('event_name', data): Sends data to the server.

5. WHEN TO USE WEBSOCKETS:
   - Chat applications.
   - Real-time dashboards (stock prices, sensor data).
   - Multiplayer games.
   - Collaborative editing (like Google Docs).
"""

def get_websocket_summary():
    return "WebSockets enable real-time, bi-directional communication."
