import threading
import requests
import time

# =====================================================
# Configuration
# =====================================================
BASE_URL = "http://127.0.0.1:5000"
REGISTER_URL = f"{BASE_URL}/register"
LOGIN_URL = f"{BASE_URL}/login"
TOTAL_USERS = 500

# Synchronization Event to start all threads at once
start_event = threading.Event()
counter_lock = threading.Lock()
passed_count = 0
failed_count = 0

# =====================================================
# Test Function
# =====================================================
def simulate_user(user_id):
    global passed_count, failed_count
    username = f"user_{user_id}"
    password = f"pass_{user_id}"

    # Wait until all threads are ready
    start_event.wait()

    try:
        # 1. Registration Phase
        reg_response = requests.post(
            REGISTER_URL,
            data={"username": username, "password": password},
            allow_redirects=True,
            timeout=5
        )
        
        # 2. Login Phase
        login_response = requests.post(
            LOGIN_URL,
            data={"username": username, "password": password},
            timeout=5
        )

        success = "Welcome" in login_response.text
        
        with counter_lock:
            if success:
                passed_count += 1
                status = "SUCCESS"
            else:
                failed_count += 1
                status = "FAILED (Content mismatch)"
        
        print(
            f"User {user_id:03} | "
            f"Reg: {reg_response.status_code} | "
            f"Login: {login_response.status_code} | "
            f"Result: {status}"
        )

    except Exception as e:
        with counter_lock:
            failed_count += 1
        print(f"User {user_id} Error: {e}")

# =====================================================
# Main Execution
# =====================================================
if __name__ == "__main__":
    print(f"Preparing {TOTAL_USERS} threads...")
    threads = []
    
    for i in range(1, TOTAL_USERS + 1):
        t = threading.Thread(target=simulate_user, args=(i,))
        threads.append(t)
        t.start()

    print(f"\nStarting Load Test for {TOTAL_USERS} Users (Register + Login)...\n")
    start_time = time.time()

    # Release all threads together
    start_event.set()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    end_time = time.time()

    print("\n====================================")
    print(f"Test Results Summary:")
    print(f"Total Users: {TOTAL_USERS}")
    print(f"PASSED:      {passed_count}")
    print(f"FAILED:      {failed_count}")
    print(f"Total Time:  {end_time - start_time:.2f} seconds")
    print(f"Avg Time:    {(end_time - start_time)/TOTAL_USERS:.4f}s / user")
    print("====================================")
