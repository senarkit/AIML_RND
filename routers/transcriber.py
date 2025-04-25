from fastapi import APIRouter, HTTPException, Header
from helper.utils import verify_token

router = APIRouter()

# Protected endpoint that requires a valid token
@router.get("/data")
def get_data(username: str, token: str = Header(...)):  # Token must be passed in request headers
    if verify_token(username, token):
        # If token is valid, return dummy data
        return {"data": f"Welcome {username}, here is your data."}
    # Raise 403 if token is invalid or missing
    raise HTTPException(status_code=403, detail="Invalid token")
