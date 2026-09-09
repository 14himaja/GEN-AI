"""
API SECURITY & RATE LIMITING FOR AI (t9)
========================================

WHY SECURITY IS CRITICAL FOR AI ENGINEERS:
-----------------------------------------
1. COST: AI models (GPUs/LLM APIs) are expensive. Unprotected endpoints can lead to high bills.
2. LATENCY: High traffic can slow down inference for legitimate users.
3. DATA PRIVACY: Ensuring only authorized clients can access your proprietary models.

CONCEPTS IN THIS TUTORIAL:
--------------------------
1. API KEY AUTHENTICATION:
   - Uses a custom Decorator (`@require_api_key`) to check the 'X-API-KEY' header.
   - This is the standard way to protect Machine Learning APIs.

2. RATE LIMITING (Flask-Limiter):
   - Restricts how many times an IP address can call an endpoint.
   - Example: `@limiter.limit("3 per minute")`.
   - Returns HTTP 429 (Too Many Requests) when the limit is hit.

3. CUSTOM ERROR HANDLING:
   - Using `@app.errorhandler(429)` to return a professional JSON response instead of a raw HTML error.

HOW TO TEST:
-----------
1. cd t9
2. python app.py
3. Open http://127.0.0.1:5000
4. Try clicking the button without an API Key -> You get a 401 Unauthorized error.
5. Enter the key `sk-ai-12345` and click -> Success!
6. Click the button 4 times quickly -> You will see the "Rate Limit Exceeded" error (HTTP 429).
"""

def get_summary():
    return "API Keys and Rate Limits are the first line of defense for AI services."
