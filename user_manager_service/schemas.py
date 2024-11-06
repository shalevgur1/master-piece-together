from pydantic import BaseModel, EmailStr


# Define a new user schema
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# Defined a response user schema (influenced by database structure)
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True
