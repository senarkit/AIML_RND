from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from routers import auth, transcriber, user
from helper.database import engine, Base
from helper.models import Token, Users

# Create the database tables if they don't already exist
Base.metadata.create_all(bind=engine)

# Initialize the FastAPI app
app = FastAPI()

# Include the routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(transcriber.router, prefix="/transcriber", tags=["transcriber"])
app.include_router(user.router, prefix="/user", tags=["user"])

@app.get("/")
async def root():
    return {"message": "Welcome to the API! Use /auth for authentication, /user for user management, and /transcriber for transcriber functionality."}

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

