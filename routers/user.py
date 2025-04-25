from fastapi import APIRouter
from helper.models import User
from helper.utils import load_db, save_db

router = APIRouter()

# Endpoint for user registration
@router.post("/register")
def register(user: User):
    db = load_db()
    if user.username in db:
        return {"message": "User already exists"}
    # Add new user with blank token initially
    db[user.username] = {"password": user.password, "token": ""}
    save_db(db)
    return {"message": f"User {user.username} registered successfully"}