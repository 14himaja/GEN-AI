# Interactive API Documentation

One of the most loved features of FastAPI is its automatic API documentation. Because FastAPI is built on the **OpenAPI** standard, it automatically generates a "schema" (a blueprint) of your entire API based on your Python code and type hints.

FastAPI uses this schema to serve two different, interactive documentation web pages automatically. You do not need to write a single line of HTML or extra config!

## 1. Swagger UI (`/docs`)

If you run your FastAPI server locally, you can navigate to `http://127.0.0.1:8000/docs`.

**What is it?**
Swagger UI is a dynamic, interactive interface.
* **Exploration:** It lists every endpoint, HTTP method, and parameter in your API.
* **Interaction:** It includes a "Try it out" button. You can literally fill in the parameters, click execute, and it will send a real HTTP request to your running API and show you the real response.
* **Schemas:** It displays the exact JSON structure expected for request bodies and returned in responses, based on your Pydantic models.

## 2. ReDoc (`/redoc`)

Alternatively, you can navigate to `http://127.0.0.1:8000/redoc`.

**What is it?**
ReDoc is another tool that reads your OpenAPI schema.
* **Layout:** It provides a different layout that is heavily focused on readability. It puts the endpoint list on a left-hand sidebar and the details on the right.
* **Read-only:** Unlike Swagger UI, ReDoc is not interactive; you cannot send test requests from it. However, many developers prefer it for simply *reading* the API documentation because of its clean design.

## How it works (The magic of type hints)

The documentation isn't magic; it comes from your Python code:
1. When you define a path parameter `user_id: int`, FastAPI updates the docs to say that endpoint requires an integer.
2. When you use a Pydantic `BaseModel` for a request body, FastAPI converts that class into a JSON schema and displays it in the docs.
3. When you add docstrings (`"""..."""`) to your route functions, FastAPI extracts them and uses them as the description for that specific endpoint in the docs.
