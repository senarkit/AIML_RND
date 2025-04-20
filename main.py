# fastapi_server/main.py
from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
import random

app = FastAPI()

# === Config ===
API_KEY = "mysecretkey123"  # my API key

# === Models ===
class DataPoint(BaseModel):
    id: int
    value: float
    description: str

# === Auth Dependency ===
def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")
    return True

# === Routes ===
@app.get("/data", response_model=DataPoint, dependencies=[Depends(verify_api_key)])
def get_random_data():
    out = DataPoint(
        id=random.randint(1, 1000),
        value=round(random.uniform(0.0, 100.0), 2),
        description="Randomly generated datapoint"
    )
    json_output = out.model_dump()
    return json_output

