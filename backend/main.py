from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import datetime

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock data
class Alert(BaseModel):
    id: int
    type: str
    message: str
    timestamp: datetime.datetime

alerts_db = [
    Alert(id=1, type="theft", message="Theft detected in Zone A", timestamp=datetime.datetime.now()),
    Alert(id=2, type="emotion", message="Angry person detected", timestamp=datetime.datetime.now()),
]

@app.get("/api/alerts", response_model=List[Alert])
def get_alerts():
    return alerts_db

@app.get("/api/video")
def get_video():
    # Return a test MJPEG stream URL or static video file path
    return {"url": "http://webcam.st-malo.com/axis-cgi/mjpg/video.cgi?resolution=320x240"}

@app.post("/api/login")
def login(username: str, password: str):
    # Always succeed for demo
    return {"token": "testtoken"}