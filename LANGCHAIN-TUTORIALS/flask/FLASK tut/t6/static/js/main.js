// 1. Initialize the Socket.IO connection
// By default, it connects to the same host and port as the web page
const socket = io();

// Get UI elements
const statusLabel = document.getElementById('status');
const liveValueLabel = document.getElementById('live-value');
const messageBox = document.getElementById('messages');
const messageInput = document.getElementById('message-input');
const usernameInput = document.getElementById('username');

// -------------------------------------------------------------------------
// SOCKET EVENT LISTENERS (Receiving from Server)
// -------------------------------------------------------------------------

// Triggered when connection is established
socket.on('connect', () => {
    statusLabel.innerText = "Connected";
    statusLabel.className = "connected";
    addMessage("System", "You are now connected to the server!");
});

// Triggered when disconnected
socket.on('disconnect', () => {
    statusLabel.innerText = "Disconnected";
    statusLabel.className = "disconnected";
});

// Listening for 'server_response' event
socket.on('server_response', (msg) => {
    addMessage("Server", msg.data);
});

// Listening for 'live_update' event (periodic server background updates)
socket.on('live_update', (data) => {
    liveValueLabel.innerText = data.value;
    // Highlight effect
    liveValueLabel.style.color = '#ff0000';
    setTimeout(() => { liveValueLabel.style.color = '#fbbc05'; }, 500);
});

// -------------------------------------------------------------------------
// HELPER FUNCTIONS (Sending to Server)
// -------------------------------------------------------------------------

function sendMessage() {
    const message = messageInput.value;
    const user = usernameInput.value;

    if (message.trim() !== "") {
        // Emit a 'client_message' event to the server
        socket.emit('client_message', {
            'user': user,
            'message': message
        });
        messageInput.value = ""; // Clear input
    }
}

function addMessage(user, text) {
    const div = document.createElement('div');
    div.className = 'message';
    div.innerHTML = `<strong>${user}:</strong> ${text}`;
    messageBox.appendChild(div);
    
    // Auto-scroll to bottom
    messageBox.scrollTop = messageBox.scrollHeight;
}

// Allow pressing "Enter" to send
messageInput.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
        sendMessage();
    }
});
