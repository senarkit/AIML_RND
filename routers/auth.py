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