# HTTP Methods in FastAPI

HTTP methods (often called "verbs") tell the server *what action* the client wants to perform on a resource. FastAPI provides decorators for all standard HTTP methods. 

In the context of databases and APIs, these map to **CRUD** operations: Create, Read, Update, Delete.

## 1. `@app.get()` - READ
Used to retrieve data from the server. A GET request should **never** modify data on the server; it is strictly for fetching information.

```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/users")
def get_users():
    # In a real app, this would fetch data from a database
    return [{"name": "Alice"}, {"name": "Bob"}]
```

## 2. `@app.post()` - CREATE
Used to send data to the server to create a new resource (e.g., registering a new user, adding an item to a cart).

```python
@app.post("/users")
def create_user(username: str):
    # This data would be saved to a database
    return {"message": f"User {username} created successfully"}
```

## 3. `@app.put()` - UPDATE (Replace)
Used to update an existing resource. A PUT request is typically expected to **replace the entire resource** with the new data provided. 

```python
@app.put("/users/{user_id}")
def update_user_entirely(user_id: int, new_username: str, new_email: str):
    # Replaces all details of the user with ID user_id
    return {"id": user_id, "username": new_username, "email": new_email}
```

## 4. `@app.patch()` - UPDATE (Partial)
Used to apply partial modifications to a resource. Unlike PUT, you only send the fields you want to change, leaving the rest intact.

```python
@app.patch("/users/{user_id}")
def update_user_partially(user_id: int, new_email: str):
    # Only updates the email, leaves the username alone
    return {"id": user_id, "status": "Email updated", "new_email": new_email}
```

## 5. `@app.delete()` - DELETE
Used to remove a resource from the server.

```python
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    # Deletes the user from the database
    return {"message": f"User {user_id} has been deleted"}
```

### Summary of Decorators
When you use `@app.post("/items")`, you are telling FastAPI:
1. "When an HTTP request comes in..."
2. "...using the **POST** method..."
3. "...and the path is exactly `/items`..."
4. "...execute the Python function immediately below this decorator."
