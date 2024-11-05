from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from . import schemas

# User manager FastAPI app instance
um_app = FastAPI()

# Define a datatype for a user
class User(BaseModel):
    username: str
    email: EmailStr
    password: str

""" Implementing CRUD for creating, reading, updating 
    and deleteing users and user's information """

# Creating new users and insert to database
@um_app.post("/users/create", status_code=201)
async def create_user(user: User):
    print(user.username)
    print(user.email)
    print(user.password)

@um_app.get("/users/", status_code=200)
async def get_user(username: str):
    print(username)

@um_app.post("/users/update", status_code=200)
async def update_user(update_info: User):
    print(update_info)

@um_app.delete("/users/", status_code=200)
async def delete_user(username: str):
    print("going to delete this user: ", username)




@app.post("/users/", response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.UserResponse])
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=schemas.UserResponse)
async def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db=db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}", response_model=schemas.UserResponse)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user