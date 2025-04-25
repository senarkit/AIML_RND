from fastapi import FastAPI
from routers import auth, transcriber, user

app = FastAPI()

# Mount all routers under respective route prefixes
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(transcriber.router, prefix="/transcriber", tags=["transcriber"])
app.include_router(user.router, prefix="/user", tags=["user"])