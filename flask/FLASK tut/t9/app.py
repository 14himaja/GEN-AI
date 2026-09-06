from flask import Flask, request, jsonify, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import functools

app = Flask(__name__)

# -------------------------------------------------------------------------
# 1. RATE LIMITING LOGIC (The "Police" of our API)
# -------------------------------------------------------------------------
# How it works:
# - Limiter tracks every visitor's IP address (get_remote_address).
# - It counts how many times that IP hits your server.
# - If the count is too high, it blocks the request BEFORE it reaches your code.
limiter = Limiter(
    key_func=get_remote_address,  # This identifies users by their IP address.
    app=app,
    default_limits=["200 per day"], # General safety net for all pages.
    storage_uri="memory://",       # Saves the 'hit counts' in RAM (simple for tutorials).
)

# -------------------------------------------------------------------------
# 2. SECURITY DECORATOR LOGIC (The "Bouncer" at the door)
# -------------------------------------------------------------------------
# In Python, a 'Decorator' is a function that wraps another function.
# Think of it as a security checkpoint that everyone must pass.

VALID_API_KEYS = {"sk-ai-12345", "sk-ml-67890"}

def require_api_key(original_route_function):
    """
    This is a custom decorator. It 'wraps' our route function to check 
    for an API key before allowing the route to execute.
    """
    @functools.wraps(original_route_function) # This ensures Flask still knows the name of your route.
    def check_security_logic(*args, **kwargs):
        # STEP 1: Look into the 'Request Headers' sent by the browser/client.
        # We expect a header named 'X-API-KEY'.
        provided_key = request.headers.get('X-API-KEY')

        # STEP 2: Check if the key exists and if it is in our 'Allowed' list.
        if provided_key and provided_key in VALID_API_KEYS:
            # SUCCESS: Pass the request along to the actual route function.
            return original_route_function(*args, **kwargs)
        else:
            # FAILURE: Stop the request here and return a 401 error.
            return jsonify({"error": "Unauthorized", "message": "Invalid API Key"}), 401
            
    return check_security_logic

# -------------------------------------------------------------------------
# 3. ROUTE IMPLEMENTATION
# -------------------------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
# ORDER OF EXECUTION:
# 1. @limiter.limit -> Checks if the user is spamming (Rate Limit).
# 2. @require_api_key -> Checks if the user has a valid key (Authentication).
# 3. def predict() -> Only runs if both checks above pass.
@limiter.limit("3 per minute") 
@require_api_key
def predict():
    """This function simulates expensive AI logic."""
    # If the code reaches this line, it means the user passed BOTH checks!
    return jsonify({
        "status": "success",
        "prediction": "Positive Sentiment Detected!",
        "cost_saved": "Prevented 1000 automated spam requests"
    })

# This runs automatically if @limiter.limit triggers a block
@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        "error": "Rate limit exceeded",
        "message": f"Too many requests! Wait until: {e.description}"
    }), 429

if __name__ == '__main__':
    app.run(debug=True)
