from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class Alert(BaseModel):
    id: int
    type: str
    message: str
    timestamp: str

class User(BaseModel):
    id: int
    username: str
    email: str
    role: str

class Settings(BaseModel):
    alert_threshold: float
    notify_email: str

class DetectionRequest(BaseModel):
    image_url: str

class DetectionResult(BaseModel):
    objects: list
    emotions: list

# Mock data
alerts_db = [
    Alert(id=1, type="theft", message="Theft detected in Zone A", timestamp="2024-06-01 10:24"),
    Alert(id=2, type="emotion", message="Angry person detected", timestamp="2024-06-01 09:58"),
]
users_db = [
    User(id=1, username="admin", email="admin@obscureeye.ai", role="admin"),
    User(id=2, username="client", email="client@company.com", role="client"),
]
settings_db = Settings(alert_threshold=0.7, notify_email="admin@obscureeye.ai")

@app.get("/api/alerts", response_model=List[Alert])
def get_alerts():
    return alerts_db

@app.get("/api/video")
def get_video():
    return {"url": "http://webcam.st-malo.com/axis-cgi/mjpg/video.cgi?resolution=320x240"}

@app.post("/api/login")
def login(username: str, password: str):
    # Always succeed for demo
    return {"token": "testtoken"}

@app.get("/api/settings", response_model=Settings)
def get_settings():
    return settings_db

@app.post("/api/settings", response_model=Settings)
def update_settings(settings: Settings):
    global settings_db
    settings_db = settings
    return settings_db

@app.get("/api/users", response_model=List[User])
def get_users():
    return users_db

@app.post("/api/users", response_model=User)
def add_user(user: User):
    users_db.append(user)
    return user

@app.delete("/api/users/{user_id}")
def delete_user(user_id: int):
    global users_db
    users_db = [u for u in users_db if u.id != user_id]
    return {"status": "deleted"}

@app.post("/api/ai/detect", response_model=DetectionResult)
def ai_detect(request: DetectionRequest):
    # Mock detection result
    return DetectionResult(
        objects=[{"type": "person", "confidence": 0.98}],
        emotions=[{"type": "angry", "confidence": 0.87}]
    )