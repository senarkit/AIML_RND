# fastapi_server/main.py
from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

class DataPoint(BaseModel):
    id: int
    value: float
    description: str

@app.get("/data", response_model=DataPoint)
def get_random_data():
    out = DataPoint(
        id=random.randint(1, 1000),
        value=round(random.uniform(0.0, 100.0), 2),
        description="Randomly generated datapoint"
    )
    json_output = out.model_dump()
    return json_output
