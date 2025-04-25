from fastapi import APIRouter, HTTPException
from helper.models import User
from helper.utils import authenticate_user

router = APIRouter()

# Login endpoint to validate user and return a token
@router.post("/login")
def login(user: User):
    token = authenticate_user(user.username, user.password)
    if token:
        return {"message": "Login successful", "token": token}
    # Raise 401 if credentials are incorrect
    raise HTTPException(status_code=401, detail="Invalid credentials")
