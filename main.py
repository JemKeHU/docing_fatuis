from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI(
    title="My API",
    description="I'm just fooling around with fastapi",
    version="1.0.0"
)

class User(BaseModel):
    id: int
    name: str
    age: int

class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None

users_db = [
    {"id": 1, "name": "Stas", "age": 19},
    {"id": 2, "name": "Plaid", "age": 18}
]

@app.get("/")
async def main():
    return {"message": "Hello World!"}

@app.get("/users")
async def get_users():
    return users_db

@app.get("/user/{user_id}")
async def get_user(user_id: int):
    for user in users_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/users")
async def add_user(user: User):
    users_db.append(user.model_dump())
    return {"message": "User Created", "user": user}

@app.put("/users/{user_id}")
async def update_user(user_id: int, updated_user: User):
    for index, user in enumerate(users_db):
        if user["id"] == user_id:
            users_db[index] = updated_user.model_dump()
            return {"message": "User updated succesfully", "user": updated_user}
    raise HTTPException(status_code=404, detail="User not found")

@app.patch("/users/{user_id}")
async def update_specific_user(user_id: int, user_update: UserUpdate):
    for user in users_db:
        if user["id"] == user_id:
            if user_update.name is not None:
                user["name"] = user_update.name
            if user_update.age is not None:
                user["age"] = user_update.age
            return {"message": f"User {user["name"]} updated partially", "user": user}
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    for index, user in enumerate(users_db):
        if user["id"] == user_id:
            del users_db[index]
            return {"message": f"User {user_id} deleted"}
    raise HTTPException(status_code=404, detail="User not found")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)