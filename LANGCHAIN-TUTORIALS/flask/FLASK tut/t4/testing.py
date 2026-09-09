import threading
import requests
import time
import random
# =====================================================
# API URL
# =====================================================

URL = "http://127.0.0.1:5000/login"

# =====================================================
# Number of Parallel Users
# =====================================================

TOTAL_USERS = 10

# =====================================================
# Synchronization Event
# =====================================================

start_event = threading.Event()


# =====================================================
# Function Executed by Each User
# =====================================================

usernames = ['admin', 'user1', 'user2', 'user3']
passwords = ['secret', 'password1', 'password2', 'password3']

def send_request(user_id):

    # Wait until all threads are ready
    start_event.wait()

    try:

        response = requests.post(
            URL,
            data={
                "username": random.choice(usernames),
                "password": random.choice(passwords)
            }
        )

        print(
            f"User {user_id} | "
            f"Status: {response.status_code} | "
            f"Response: {response.text}"
            f" | Username: {response.request.body.split('&')[0].split('=')[1]}"
            f" | Password: {response.request.body.split('&')[1].split('=')[1]}"
        )

    except Exception as e:

        print(f"User {user_id} Failed: {e}")


# =====================================================
# Create Threads
# =====================================================

threads = []

for i in range(TOTAL_USERS):

    t = threading.Thread(
        target=send_request,
        args=(i + 1,)
    )

    threads.append(t)

    t.start()

print(threads)

# =====================================================
# Start All Threads AT THE SAME TIME
# =====================================================

print(f"\nStarting {TOTAL_USERS} Parallel Users...\n")

start_time = time.time()

# Release all threads together
start_event.set()


# =====================================================
# Wait for Completion
# =====================================================

for t in threads:
    t.join()

end_time = time.time()

print("\n====================================")
print(f"Completed {TOTAL_USERS} Parallel Requests")
print(f"Total Time: {end_time - start_time:.2f} seconds")
print("====================================")