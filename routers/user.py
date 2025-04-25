from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, status
from fastapi.security import OAuth2PasswordBearer
from helper.models import Users, Token
from helper.database import get_db
from passlib.context import CryptContext
from jose import jwt, JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=8, max_length=20)

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Here, decode token and return user info (for now mock)
    return {"id": 1, "username": "test_user"}  # Mocking current user

@router.get("/", status_code=status.HTTP_200_OK)
async def get_users(
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[dict, Depends(get_current_user)]
):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    return user_model

@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    user_verification: UserVerification
):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    
    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.commit()
    db.refresh(user_model)
    return {"message": "Password updated successfully"}

@router.put("/phonenumber/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(
    user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    phone_number: str
):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return {"message": "Phone number updated successfully"}
