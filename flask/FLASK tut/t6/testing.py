import socketio
import threading
import time

# =====================================================
# Configuration
# =====================================================
URL = "http://127.0.0.1:5000"
TOTAL_CLIENTS = 500
passed_count = 0
failed_count = 0
lock = threading.Lock()

def start_client(client_id):
    global passed_count, failed_count
    sio = socketio.Client()

    # Define event handlers for the client
    @sio.on('connect')
    def on_connect():
        # Once connected, send a test message
        sio.emit('client_message', {
            'user': f'Bot_{client_id}',
            'message': 'Hello from automated test!'
        })

    @sio.on('server_response')
    def on_response(data):
        nonlocal success
        if f'Bot_{client_id}' in data['data']:
            success = True
            sio.disconnect()

    success = False
    try:
        sio.connect(URL, wait_timeout=10)
        # Wait a bit for the response to come back
        timeout = time.time() + 5
        while not success and time.time() < timeout:
            time.sleep(0.1)
        
        with lock:
            if success:
                passed_count += 1
            else:
                failed_count += 1
                print(f"Client {client_id} timed out waiting for response.")
    except Exception as e:
        with lock:
            failed_count += 1
        print(f"Client {client_id} failed to connect: {e}")
    finally:
        if sio.connected:
            sio.disconnect()

# =====================================================
# Main Execution
# =====================================================
if __name__ == "__main__":
    print(f"Starting WebSocket Load Test with {TOTAL_CLIENTS} clients...")
    threads = []
    
    start_time = time.time()
    for i in range(1, TOTAL_CLIENTS + 1):
        t = threading.Thread(target=start_client, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    
    end_time = time.time()

    print("\n====================================")
    print(f"WebSocket Test Results Summary:")
    print(f"Total Clients: {TOTAL_CLIENTS}")
    print(f"PASSED:        {passed_count}")
    print(f"FAILED:        {failed_count}")
    print(f"Total Time:    {end_time - start_time:.2f} seconds")
    print("====================================")
