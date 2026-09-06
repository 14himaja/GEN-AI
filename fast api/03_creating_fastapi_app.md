# Creating Your First FastAPI Application

Let's walk through the exact steps to create and run a FastAPI application from scratch.

## Step 1: Installation

You need to install both the framework (FastAPI) and the ASGI server (Uvicorn).
Open your terminal and run:

```bash
pip install fastapi uvicorn
```
*(Alternatively, you can run `pip install "fastapi[all]"` which installs FastAPI along with Uvicorn and other useful optional dependencies).*

## Step 2: Writing the Code

Create a new Python file named `main.py`. This is typically the entry point for your application.

```python
# main.py

# 1. Import the FastAPI class
from fastapi import FastAPI

# 2. Create an instance of the FastAPI class.
# This 'app' variable is the core of your application.
app = FastAPI()

# 3. Create a route (an endpoint)
# We use a decorator to tell FastAPI that the function below 
# handles GET requests going to the root URL ("/")
@app.get("/")
def read_root():
    # 4. Return data. FastAPI automatically converts Python dictionaries to JSON.
    return {"message": "Welcome to my first FastAPI app!"}
```

### Breaking down the code:
1. `from fastapi import FastAPI`: We import the main class.
2. `app = FastAPI()`: We instantiate it. This `app` object is what Uvicorn will look for to run your server.
3. `@app.get("/")`: This is a "path operation decorator". 
   * `@app` refers to the instance we just created.
   * `.get` is the HTTP method.
   * `("/")` is the path (the root of the domain).
4. `def read_root():`: The function that gets executed when a user visits that path.

## Step 3: Running the Server

To start your API, open your terminal in the same folder as `main.py` and run:

```bash
uvicorn main:app --reload
```

### What does this command mean?
* `uvicorn`: The command to start the ASGI server.
* `main`: The name of your Python file (without the `.py` extension). This is the module.
* `app`: The name of the FastAPI instance variable you created inside `main.py` (`app = FastAPI()`).
* `--reload`: This is a lifesaver for development. It tells Uvicorn to watch your code files. Whenever you save a change, the server will automatically restart so you can see your changes immediately. **Do not use this in production.**

After running the command, you will see output like:
```text
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```
You can now open your browser and go to `http://127.0.0.1:8000` to see your JSON response!
