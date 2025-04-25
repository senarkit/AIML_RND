from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from helper.database import get_db
from helper.models import Users, Token
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError

router = APIRouter()

SECRET_KEY = 'mysupersecretkey'
ALGORITHM = 'HS256'
STATIC_TOKEN = 'test123'

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str = Field(min_length=8, max_length=20)
    role: str = Field(default="user")
    phone_number: str = Field(default="")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(Users).filter(Users.username == username).first()
    if not user or not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    create_user_request: CreateUserRequest,
    db: Annotated[Session, Depends(get_db)]
):
    user = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        phone_number=create_user_request.phone_number
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User created successfully"}

@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)]
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid username or password")
    access_token = create_access_token(
        data={"sub": user.username, "id": user.id, "role": user.role},
        expires_delta=timedelta(minutes=30)
    )
    # Save token to DB
    db_token = Token(
        serviceAccount=user.username,
        pladaName="dummyPlada",
        clientName="dummyClient",
        tokenVal=access_token
    )
    db.add(db_token)
    db.commit()

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/validate")
async def validate_token(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)]
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        db_token = db.query(Token).filter(Token.tokenVal == token).first()
        if not db_token or not db_token.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found or inactive")

        return {"message": "Token is valid", "user": username}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token decode failed")
