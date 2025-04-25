from fastapi import FastAPI
from routers import auth, transcriber

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(transcriber.router, prefix="/transcriber", tags=["transcriber"]) 