# fastapi_server/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import random

app = FastAPI()

# === SECRET & ENCRYPTION CONFIG ===
SECRET_KEY = "supersecretjwtkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Simulated "DB" user
synthetic_user_db = {
    "demo_user": {
        "username": "demo_user",
        "hashed_password": "$2b$12$ZnAlJ0O4svcyHCriKNM12uhnOBPHbluYTtKQ.Z96QJ97WIaxGYKze",  # password: "demopass"
    },
    "user_2": {
        "username": "user_2",
        "hashed_password": "$2b$12$vCWkx1gAhHe3Up6EXMfbu.reozf0Sw97vBItdN09tXb/GjJ0xULo2",  # password: "iamuser2pass"
    },
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# === Models ===
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class DataPoint(BaseModel):
    id: int
    value: float
    description: str

# === Utility Functions ===
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username: str):
    user = synthetic_user_db.get(username)
    return user if user else None

# def authenticate_user(username: str, password: str):
#     user = get_user(username)
#     if not user or not verify_password(password, user["hashed_password"]):
#         return False
#     return user

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        print("[DEBUG] User not found")
        return False
    if not verify_password(password, user["hashed_password"]):
        print("[DEBUG] Password did not match")
        return False
    print("[DEBUG] User authenticated")
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# === Auth Endpoint ===
@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

# === Dependency to extract user from token ===
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token validation error")

# === Protected Endpoint ===
@app.get("/data", response_model=DataPoint)
def get_random_data():
    out = DataPoint(
        id=random.randint(1, 1000),
        value=round(random.uniform(0.0, 100.0), 2),
        description="Randomly generated datapoint"
    )
    json_output = out.model_dump()
    return json_output