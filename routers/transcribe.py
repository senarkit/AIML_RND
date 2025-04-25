from fastapi import APIRouter, WebSocket
from fastapi.responses import HTMLResponse
import json

router = APIRouter()

@router.get("/")
async def ol_api_endpoint_seq(audioObj):
    data = json.loads(audioObj)
    return data