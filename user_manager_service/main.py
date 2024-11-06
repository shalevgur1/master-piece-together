from fastapi import FastAPI, status, HTTPException, Response
from fastapi.responses import JSONResponse
from database.database import DBUsersManager
import schemas


# User manager FastAPI app instance
app = FastAPI()

# Creating database manager object
db = DBUsersManager()

""" 
    Implementing CRUD for creating, reading, updating 
    and deleteing users and user's information 
"""

# Creating new users and insert to database
@app.post("/users/create", response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate):
    created_user = db.create_user(user.username, user.email, user.password)
    if created_user is None:
        # If user creation failed (e.g., username or email already exists)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username or email already exists."
        )
    return created_user

# Get requested user by username
@app.get("/users/{username}", response_model=schemas.UserResponse)
async def get_user(username: str):
    user = db.get_user(username)
    if user is None:
            # If user is not found
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )
    return user

# Change requested user by user id
@app.put("/users/{user_id}", response_model=schemas.UserResponse)
async def get_user(user_id: int, user: schemas.UserCreate):
    updated_user = db.update_user(user_id, user.username, user.email, user.password)
    if updated_user is None:
            # If the user to be updated is not found
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found or username or email already exist"
            )
    return updated_user

# Delete requested user by user_id
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def get_user(user_id: int):
    deleted = db.delete_user(user_id)
    if not deleted:
        # If the user is not found, raise a 404 error
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    # Return an empty response with 204 status code
    return Response(status_code=status.HTTP_204_NO_CONTENT)
        