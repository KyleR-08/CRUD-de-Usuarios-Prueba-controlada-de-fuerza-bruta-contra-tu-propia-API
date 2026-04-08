from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel
from typing import Optional

app = FastAPI()

class User(SQLModel):
    id: Optional[int] = None
    username: str
    password: str
    is_active: bool = True

db_users = [
    User(id=1, username="admin", password="ab1"),
    User(id=2, username="user", password="db0"),
    User(id=3, username="guest", password="HG7"),
]

@app.post("/users")
def create_user(user: User):
    user.id = len(db_users) + 1
    db_users.append(user)
    return user

@app.get("/users")
def get_users():
    return db_users

@app.get("/users/{id}")
def get_user(id: int):
    for u in db_users:
        if u.id == id:
            return u
    raise HTTPException(status_code=404, detail="Not found")

@app.put("/users/{id}")
def update_user(id: int, data: User):
    for u in db_users:
        if u.id == id:
            u.username = data.username
            u.is_active = data.is_active
            return u
    raise HTTPException(status_code=404, detail="Not found")

@app.delete("/users/{id}")
def delete_user(id: int):
    for i, u in enumerate(db_users):
        if u.id == id:
            db_users.pop(i)
            return {"message": "Deleted"}
    raise HTTPException(status_code=404, detail="Not found")

@app.post("/login")
def login(user: User):
    for u in db_users:
        if u.username == user.username and u.password == user.password:
            return {"message": "Login successful"}
    return {"message": "Invalid username or password"}