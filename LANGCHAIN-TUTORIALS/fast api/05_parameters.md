# Path and Query Parameters

Parameters are how clients send specific dynamic data to your API to ask for exactly what they want.

## 1. Path Parameters

Path parameters are variables embedded directly into the URL path. They are essential for identifying a specific resource.

**How to use them:**
1. Put a variable inside curly braces `{}` in the path of your decorator.
2. Add that exact same variable name as an argument to your Python function.
3. Provide a type hint for the argument. FastAPI will automatically validate and convert the data!

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int):
    # If the user goes to /items/42, item_id will be the integer 42
    return {"item_id": item_id}
```

*What happens if a user types `/items/apple`?*
FastAPI's built-in validation (Pydantic) kicks in. It knows `item_id` should be an `int`, so it will automatically return a nice error to the user saying the value is invalid, without your code ever crashing!

## 2. Query Parameters

When you declare function parameters that are **not** part of the path, FastAPI automatically interprets them as "query" parameters.
Query parameters appear at the end of a URL after a question mark `?`, separated by ampersands `&`.
Example URL: `http://localhost:8000/items/?skip=0&limit=10`

**How to use them:**
Just add them as function arguments.

```python
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    # These parameters have default values (0 and 10), 
    # so they are optional.
    return {"skip": skip, "limit": limit}
```

### Optional Parameters vs Required Parameters
* **Optional:** Give it a default value (like `= 0` or `= None`).
* **Required:** Don't give it a default value. If the client doesn't provide it in the URL, FastAPI will return an error.

```python
# 'q' is an optional string, 'user_id' is a required integer
@app.get("/search/")
def search_data(user_id: int, q: str | None = None):
    return {"user": user_id, "search_query": q}
```
