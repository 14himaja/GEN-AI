"""
ASYNCHRONOUS TASKS FOR AI/ML (t7)
================================

WHY USE CELERY?
---------------
In AI/ML, running a model (inference or training) often takes 10+ seconds.
If you run this inside a standard Flask route:
1. The user's browser waits until the task is done.
2. The browser might "Time Out" and show an error.
3. The server can't handle other users while it's busy with the model.

CELERY solves this by moving the task to a "Background Worker."

ARCHITECTURE:
-------------
[Client (Browser)]  <-- (Polls for Status) --> [Flask App]
        |                                         |
        | (1. Request Task)                       | (2. Queue Task)
        v                                         v
   [Flask Route] ---------------------------> [Redis (Broker)]
                                                  |
                                                  | (3. Pick up Task)
                                                  v
                                           [Celery Worker]
                                           (Runs ML Model)

HOW TO RUN THIS TUTORIAL:
-------------------------
1. Install Redis on your machine (or use a Docker container).
2. Start the Redis server.
3. Open two terminal windows:
   - Terminal 1 (The Worker):
     cd t7
     celery -A app.celery worker --loglevel=info
   - Terminal 2 (The Flask App):
     python t7/app.py

Note: On Windows, Celery might need 'eventlet' or 'solo' to work properly:
pip install eventlet
celery -A app.celery worker --loglevel=info -P eventlet
"""

def get_summary():
    return "Celery + Redis allow for long-running AI tasks without blocking the UI."
