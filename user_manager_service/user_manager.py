from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI()

class User(BaseModel):
    username: str
    email: EmailStr
    password: str

@app.post("/users/", status_code=201)
async def create_user(user: User):
    print("User", User.username, "Email", User.email, "Password", User.password)