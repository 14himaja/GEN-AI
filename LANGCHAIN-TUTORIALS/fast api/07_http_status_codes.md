# HTTP Status Codes

When an API responds, it includes an HTTP Status Code. This is a 3-digit number that tells the client if the request was successful, or if (and why) it failed.

## 1. Setting Status Codes for Success

By default, FastAPI returns a `200 OK` status code. However, when you create a new resource (e.g., using POST), you should return a `201 Created` status code.

You do this using the `status_code` parameter in your decorator. FastAPI provides a handy `status` module so you don't have to memorize the numbers.

```python
from fastapi import FastAPI, status

app = FastAPI()

@app.post("/items/", status_code=status.HTTP_201_CREATED)
def create_item(name: str):
    return {"name": name}
```

### Common Success Codes (2xx):
* `200 OK`: General success (used for GET, PUT, PATCH).
* `201 Created`: Successfully created a new resource (used for POST).
* `204 No Content`: Successful, but there is no data to return (used for DELETE).

## 2. Returning Errors (HTTPException)

If a client asks for something that doesn't exist, or if they don't have permission, you need to return an error status code.

In FastAPI, you don't *return* an error; you **raise** an `HTTPException`. This instantly stops the function and sends the error response.

```python
from fastapi import FastAPI, HTTPException, status

app = FastAPI()

fake_items_db = {"foo": "The Foo Item"}

@app.get("/items/{item_id}")
def read_item(item_id: str):
    if item_id not in fake_items_db:
        # Stop immediately and return a 404 error
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return {"item": fake_items_db[item_id]}
```

### Common Error Codes:
**Client Errors (4xx) - The client messed up:**
* `400 Bad Request`: General client error.
* `401 Unauthorized`: The client needs to log in.
* `403 Forbidden`: The client is logged in, but doesn't have permission.
* `404 Not Found`: The requested resource doesn't exist.

**Server Errors (5xx) - The server messed up:**
* `500 Internal Server Error`: Your Python code crashed. FastAPI handles this automatically if an unhandled exception occurs in your code.
