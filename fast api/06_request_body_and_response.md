# Request Body and Responses

When you need to send data *from* the client (like a browser) *to* your API, you send it in the **Request Body**. This is heavily used with POST, PUT, and PATCH methods.

## 1. Request Body

FastAPI uses **Pydantic** models to declare the structure of your request bodies. This gives you automatic data validation, conversion, and editor support.

**How to do it:**
1. Import `BaseModel` from `pydantic`.
2. Create a class that inherits from `BaseModel`.
3. Define the attributes as standard Python types.
4. Use this class as a type hint in your route function.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 1. Define the data model
class Item(BaseModel):
    name: str
    description: str | None = None  # Optional string
    price: float
    tax: float | None = None

# 2. Use the model as a parameter
@app.post("/items/")
def create_item(item: Item):
    # 'item' is now a fully validated Python object.
    # You can access its attributes using dot notation: item.name, item.price
    
    total_price = item.price
    if item.tax:
        total_price += item.tax
        
    return {"item_name": item.name, "total": total_price}
```

If a client sends JSON that is missing the `name` or `price` fields, FastAPI will automatically reject the request and tell the client exactly what was wrong.

## 2. Response Models

Just as you can validate incoming data, you can (and should!) define the shape of the data your API *returns*. You do this using the `response_model` parameter in the decorator.

**Why use `response_model`?**
1. **Validation:** It ensures your API actually returns the data it promised to return.
2. **Filtering:** It filters out sensitive data. E.g., if you return a `UserInDB` model that includes a hashed password, you can use a `UserPublic` response model to ensure the password is automatically stripped out before being sent to the client.
3. **Documentation:** It automatically updates the Swagger UI docs so users know what to expect.

```python
from pydantic import BaseModel

class UserIn(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    username: str
    # password is NOT in the output model

@app.post("/user/", response_model=UserOut)
def create_user(user: UserIn):
    # We receive the password
    print(f"Saving password: {user.password}")
    
    # We return the whole user object
    # But FastAPI will look at 'UserOut' and automatically REMOVE the password 
    # before sending the final JSON to the client!
    return user
```
