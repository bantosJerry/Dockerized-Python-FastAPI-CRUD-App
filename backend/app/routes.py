from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from database import get_db
from handlers import register_user, login_user, get_all_users, update_user, delete_user

# Define Pydantic models
class RegisterUser(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str


class LoginUser(BaseModel):
    username: str
    password: str


class UpdateUser(BaseModel):
    username: str = None
    email: EmailStr = None
    password: str = None
    role: str = None


# Create an API router
auth_router = APIRouter()


# Register route
@auth_router.post("/api/register")
def register(user: RegisterUser, db: Session = Depends(get_db)):
    """
    Endpoint to register a new user.
    """
    try:
        return register_user(db, user.username, user.email, user.password, user.role)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Login route
@auth_router.post("/api/login")
def login(credentials: LoginUser, db: Session = Depends(get_db)):
    """
    Endpoint to log in a user.
    """
    return login_user(db, credentials.username, credentials.password)


# Protected route to get all users
@auth_router.get("/api/users")
def get_users(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve all users.
    """
    return get_all_users(db)


# Update user route
@auth_router.put("/api/user/{user_id}")
def update_user_route(user_id: int, updates: UpdateUser, db: Session = Depends(get_db)):
    """
    Endpoint to update user details.
    """
    return update_user(
        db,
        user_id,
        updates.username,
        updates.email,
        updates.password,
        updates.role,
    )


# Delete user route
@auth_router.delete("/api/user/{user_id}")
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to delete a user.
    """
    return delete_user(db, user_id)
