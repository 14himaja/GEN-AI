"""
========================================================
                Flask Routing Tutorial
========================================================

This file demonstrates:

1. Basic routes
2. Query parameters
3. HTML escaping for security
4. Dynamic URL routing
5. Flask converter types
6. Trailing slash behavior

Run:
------
flask --app tut_01 run

Test URLs:
-----------
http://127.0.0.1:5000/
http://127.0.0.1:5000/health
http://127.0.0.1:5000/greet?name=Praveen
http://127.0.0.1:5000/hello?name=Praveen
http://127.0.0.1:5000/user/Praveen
http://127.0.0.1:5000/post/10
http://127.0.0.1:5000/path/folder1/folder2/file.txt
http://127.0.0.1:5000/projects/
http://127.0.0.1:5000/about

========================================================
"""

from flask import Flask, request
from markupsafe import escape

# Create Flask application
app = Flask(__name__)


# ======================================================
# 1. Home Route
# ======================================================

@app.route('/')
def home():
    """
    Basic route.

    URL:
        /

    Returns:
        Simple HTML heading
    """
    return '<h1>Hello, World!</h1>'


# ======================================================
# 2. Health Check Route
# ======================================================

@app.route('/health')
def health():
    """
    Health check endpoint.

    URL:
        /health

    Returns:
        JSON response
    """
    return {
        "status": "OK",
        "message": "Application is healthy",
        "code": 200
    }


# ======================================================
# 3. Secure Query Parameter Example
# ======================================================

@app.route('/greet')
def greet():
    """
    Secure greeting endpoint.

    Uses escape() to prevent XSS attacks.

    Example:
        /greet?name=Praveen

    Dangerous Example:
        /greet?name=<script>alert("bad")</script>

    Output:
        The script tag is displayed as text instead
        of executing in the browser.
    """

    name = request.args.get('name', 'Praveen')

    return f'<h1>Hello, {escape(name)}!</h1>'


# ======================================================
# 4. Insecure Query Parameter Example
# ======================================================

@app.route('/hello')
def hello():
    """
    Insecure greeting endpoint.

    This route DOES NOT use escape().

    Example:
        /hello?name=Praveen

    Warning:
        User input is directly rendered into HTML.
        This may allow XSS attacks.
    """

    name = request.args.get('name', 'Praveen')

    return f'<h1>Hello, {name}!</h1>'


# ======================================================
# Flask Converter Types
# ======================================================

"""
Converter Types:
-----------------

string  -> Default, accepts text without "/"
int     -> Accepts integers
float   -> Accepts floating point numbers
path    -> Accepts slashes as part of value
uuid    -> Accepts UUID strings
"""


# ======================================================
# 5. Dynamic URL - String Converter
# ======================================================

@app.route('/user/<username>')
def show_user_profile(username):
    """
    Dynamic route using string converter.

    Example:
        /user/Praveen
    """

    print(type(username))

    return f'User: {escape(username)}'


# ======================================================
# 6. Dynamic URL - Integer Converter
# ======================================================

@app.route('/post/<int:post_id>')
def show_post(post_id):
    """
    Dynamic route using int converter.

    Example:
        /post/10
    """

    print(type(post_id))

    return f'Post ID: {post_id}'


# ======================================================
# 7. Dynamic URL - Path Converter
# ======================================================

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    """
    Dynamic route using path converter.

    Example:
        /path/folder1/folder2/file.txt
    """

    print(type(subpath))

    return f'Subpath: {escape(subpath)}'


# ======================================================
# 8. Trailing Slash Example
# ======================================================

@app.route('/projects/')
def projects():
    """
    Route with trailing slash.

    If user accesses:
        /projects

    Flask automatically redirects to:
        /projects/
    """

    return 'The project page'


# ======================================================
# 9. Route Without Trailing Slash
# ======================================================

@app.route('/about')
def about():
    """
    Route without trailing slash.

    Valid:
        /about

    Invalid:
        /about/
    """

    return 'The about page'




# ======================================================
# Main Entry Point
# ======================================================

if __name__ == '__main__':
    app.run(debug=True)