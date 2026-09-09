from flask import Flask, request, jsonify, render_template
from celery import Celery
import time
import random

app = Flask(__name__)

# 1. Celery Configuration
# We use Redis as the 'Broker' (queue) and 'Backend' (store results)
# Format: redis://:password@hostname:port/db_number
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# -------------------------------------------------------------------------
# BACKGROUND TASK DEFINITION
# -------------------------------------------------------------------------

@celery.task(bind=True)
def heavy_ml_task(self, model_name):
    """
    Simulates a heavy AI/ML task (like training a model or generating an image).
    Instead of blocking the Flask app, it runs in the background.
    """
    print(f"Starting background task for model: {model_name}")
    
    total_steps = 10
    for i in range(total_steps):
        # Update progress so the user knows what's happening
        # 'self.update_state' allows us to store metadata while the task is running
        self.update_state(state='PROGRESS',
                          meta={'current': i + 1, 'total': total_steps,
                                'status': f'Processing step {i+1}...'})
        
        # Simulate heavy computation
        time.sleep(random.uniform(1, 2))
    
    return {'current': 10, 'total': 10, 'status': 'Task completed!',
            'result': f'Final prediction for {model_name}: SUCCESS'}

# -------------------------------------------------------------------------
# FLASK ROUTES
# -------------------------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    """Starts the background task and returns a Task ID immediately."""
    model_name = request.json.get('model', 'DefaultModel')
    
    # '.delay()' is the Celery way to send a task to the background queue
    task = heavy_ml_task.delay(model_name)
    
    return jsonify({'task_id': task.id}), 202

@app.route('/status/<task_id>')
def task_status(task_id):
    """Checks the status of a specific task using its ID."""
    task = heavy_ml_task.AsyncResult(task_id)
    
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
