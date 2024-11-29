import bcrypt
import jwt
import os
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import User
from datetime import datetime, timedelta

# Secret for JWT signing
JWT_SECRET = "W3siZG%%VzaXJlZFJlcGxpG%k5r!Uz61b" # this is just for testing purposes. It will only be in .env

# Helper function to hash passwords
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Helper function to check password
def check_password_hash(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# Helper function to generate JWT
def generate_jwt(user_id: int) -> str:
    expiration = datetime.utcnow() + timedelta(hours=72)
    token = jwt.encode({"user_id": user_id, "exp": expiration}, JWT_SECRET, algorithm="HS256")
    return token

# Register
def register_user(db: Session, username: str, email: str, password: str, role: str):
    # Check if username already exists
    existing_user_by_username = db.query(User).filter(User.username == username).first()
    if existing_user_by_username:
        return {"error": "Username is already taken."}

    # Check if email already exists
    existing_user_by_email = db.query(User).filter(User.email == email).first()
    if existing_user_by_email:
        return {"error": "Email is already registered."}

    # Hash the password
    hashed_password = hash_password(password)

    # Create a new user instance
    db_user = User(username=username, email=email, password=hashed_password, role=role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Generate a JWT token for the new user
    token = generate_jwt(db_user.id)

    return {"token": token}

# Login
def login_user(db: Session, username: str, password: str):
    db_user = db.query(User).filter(User.username == username).first()
    if db_user is None or not check_password_hash(password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = generate_jwt(db_user.id) 
    return {
        "token": token,
        "user": {"id": db_user.id, "username": db_user.username, "email": db_user.email, "role": db_user.role}
    }

# Getting all users
def get_all_users(db: Session):
    users = db.query(User).all()
    return [
        {"id": user.id, "username": user.username, "email": user.email, "role": user.role} 
        for user in users
    ]

# Updating a user
def update_user(db: Session, user_id: int, username: str = None, email: str = None, password: str = None, role: str = None):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if username:
        db_user.username = username
    if email:
        db_user.email = email
    if password:
        db_user.password = hash_password(password)
    if role:
        db_user.role = role
    db.commit()
    db.refresh(db_user)
    return "User updated successfully"

# Deleting a user
def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}
