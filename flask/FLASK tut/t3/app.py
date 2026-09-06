"""
============================================================
                Flask Login System Tutorial
============================================================

Topics Covered
----------------
1. Basic Flask Routes
2. JSON Responses
3. Query Parameters
4. GET vs POST Requests
5. Form Data Handling
6. Simple Login Validation
7. Route Methods
8. Debug Mode
9. curl Testing Commands

Run Application
----------------
flask --app app run

OR

python app.py

Application URL
----------------
http://127.0.0.1:5000/

============================================================
"""

from flask import Flask, request, render_template

# ============================================================
# Create Flask Application
# ============================================================

app = Flask(__name__)


# ============================================================
# 1. Home Route
# ============================================================

@app.route('/')
def home():
    """
    Home route.

    URL:
        /

    Method:
        GET

    Returns:
        Simple welcome message
    """

    return 'Hello, World!'


# ============================================================
# 2. Health Check Route
# ============================================================

@app.route('/health')
def health():
    """
    Health check endpoint.

    URL:
        /health

    Method:
        GET

    Returns:
        JSON response indicating application status
    """

    return {
        "status": "OK",
        "message": "Application is healthy",
        "code": 200
    }


# ============================================================
# 3. Query Parameter Example
# ============================================================

@app.route('/greet')
def greet():
    """
    Greeting route using query parameters.

    URL Examples:
        /greet
        /greet?name=Praveen

    Method:
        GET

    Query Parameter:
        name

    Returns:
        Personalized greeting if name is provided
    """

    name = request.args.get('name', 'World')

    return f'Hello, {name}!'


# ============================================================
# 4. Login Validation Function
# ============================================================

def do_the_login(username, password):
    """
    Validates username and password.

    Parameters:
        username (str)
        password (str)

    Returns:
        Success or failure message
    """

    if username == 'admin' and password == 'secret':
        return 'Login successful'

    return 'Invalid credentials'


# ============================================================
# 5. Login Form Display Function
# ============================================================

def show_the_login_form():
    """
    Displays login form.

    Returns:
        Simple HTML login form
    """

    return """
    <h2>Login Form</h2>

    <form method="POST" action="/login">

        <label>Username:</label><br>
        <input type="text" name="username"><br><br>

        <label>Password:</label><br>
        <input type="password" name="password"><br><br>

        <button type="submit">
            Login
        </button>

    </form>
    """


# ============================================================
# 6. Login Route
# ============================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login route handling both GET and POST requests.

    GET Request:
        Displays login form

    POST Request:
        Reads form data and validates credentials

    URL:
        /login
    """

    # --------------------------------------------------------
    # POST Request
    # --------------------------------------------------------

    if request.method == 'POST':

        # Read form data
        username = request.form['username']
        password = request.form['password']

        # Validate credentials
        return do_the_login(username, password)

    # --------------------------------------------------------
    # GET Request
    # --------------------------------------------------------

    return show_the_login_form()

@app.route('/index/')
@app.route('/index/<user>')
def index(user=None):
    """
    Index route demonstrating template rendering.

    URL Examples:
        /index/
        /index/Alice
    """
    return render_template('index.html', user=user)



# ===========================================================
# Test Routes for Dynamic URL Examples
# ==========================================================
with app.test_request_context('/'):
    
    print("\n========== HOME ROUTE TEST ==========")

    print("Request Path  :", request.path)
    print("Request Method:", request.method)

    assert request.path == '/'
    assert request.method == 'GET'


# ============================================================
# 2. Query Parameter Test
# ============================================================

with app.test_request_context('/greet?name=Praveen'):
    
    print("\n========== QUERY PARAM TEST ==========")

    print("Request Path  :", request.path)
    print("Request Method:", request.method)
    print("Query Params  :", request.args)
    print("Name Value    :", request.args.get('name'))

    assert request.path == '/greet'
    assert request.method == 'GET'
    assert request.args.get('name') == 'Praveen'


# ============================================================
# 3. POST Request Test
# ============================================================

with app.test_request_context('/login', method='POST'):
    
    print("\n========== POST METHOD TEST ==========")

    print("Request Path  :", request.path)
    print("Request Method:", request.method)

    assert request.path == '/login'
    assert request.method == 'POST'


# ============================================================
# 4. Form Data Test
# ============================================================

with app.test_request_context(
    '/login',
    method='POST',
    data={
        'username': 'admin',
        'password': 'secret'
    }
):
    
    print("\n========== FORM DATA TEST ==========")

    print("Request Path  :", request.path)
    print("Request Method:", request.method)

    print("\nForm Data:")
    print("Username:", request.form['username'])
    print("Password:", request.form['password'])

    assert request.form['username'] == 'admin'
    assert request.form['password'] == 'secret'


# ============================================================
# 5. Multiple Query Parameters Test
# ============================================================

with app.test_request_context(
    '/search?q=flask&page=2&sort=latest'
):
    
    print("\n========== MULTIPLE QUERY PARAMS TEST ==========")

    print("Request Path  :", request.path)
    print("Request Method:", request.method)

    print("\nQuery Parameters:")
    print("Search Query:", request.args.get('q'))
    print("Page Number :", request.args.get('page'))
    print("Sort Type   :", request.args.get('sort'))

    assert request.args.get('q') == 'flask'
    assert request.args.get('page') == '2'
    assert request.args.get('sort') == 'latest'


# ============================================================
# 6. Headers Test
# ============================================================

with app.test_request_context(
    '/api/data',
    headers={
        'Authorization': 'Bearer xyz123',
        'Content-Type': 'application/json'
    }
):
    
    print("\n========== HEADERS TEST ==========")

    print("Request Path  :", request.path)
    print("Request Method:", request.method)

    print("\nHeaders:")
    print("Authorization:", request.headers.get('Authorization'))
    print("Content-Type :", request.headers.get('Content-Type'))

    assert request.headers.get('Authorization') == 'Bearer xyz123'


# ============================================================
# 7. JSON Request Test
# ============================================================

with app.test_request_context(
    '/api/login',
    method='POST',
    json={
        'username': 'Praveen',
        'password': '1234'
    }
):
    
    print("\n========== JSON REQUEST TEST ==========")

    print("Request Path  :", request.path)
    print("Request Method:", request.method)

    print("\nJSON Data:")
    print(request.json)

    print("\nUsername:", request.json['username'])
    print("Password:", request.json['password'])

    assert request.json['username'] == 'Praveen'


# ============================================================
# Final Success Message
# ============================================================

print("\n================================================")
print("All Request Context Tests Passed Successfully ✅")
print("================================================")

# ============================================================
# Main Entry Point
# ============================================================

if __name__ == '__main__':

    # debug=True automatically reloads the server
    # when code changes are detected

    app.run(debug=True)


"""
============================================================
                    TEST URLS
============================================================

Home Route
------------
http://127.0.0.1:5000/

Health Route
--------------
http://127.0.0.1:5000/health

Greet Route
-------------
http://127.0.0.1:5000/greet?name=Praveen

Login Route
-------------
http://127.0.0.1:5000/login

============================================================
                LOGIN CREDENTIALS
============================================================

Username : admin
Password : secret

============================================================
                CURL COMMANDS
============================================================

NOTE:
-----
In PowerShell use curl.exe instead of curl.

------------------------------------------------------------
1. GET Request - Home Route
------------------------------------------------------------

curl.exe http://127.0.0.1:5000/

------------------------------------------------------------
2. GET Request - Health Route
------------------------------------------------------------

curl.exe http://127.0.0.1:5000/health

------------------------------------------------------------
3. GET Request - Greet Route
------------------------------------------------------------

curl.exe "http://127.0.0.1:5000/greet?name=Praveen"

------------------------------------------------------------
4. GET Request - Login Route
------------------------------------------------------------

curl.exe http://127.0.0.1:5000/login

------------------------------------------------------------
5. POST Request - Valid Login
------------------------------------------------------------

curl.exe -X POST ^
-d "username=admin&password=secret" ^
http://127.0.0.1:5000/login

Expected Output:
----------------
Login successful

------------------------------------------------------------
6. POST Request - Invalid Login
------------------------------------------------------------

curl.exe -X POST ^
-d "username=test&password=wrong" ^
http://127.0.0.1:5000/login

Expected Output:
----------------
Invalid credentials

============================================================
"""