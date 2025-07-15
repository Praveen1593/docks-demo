import os
from dotenv import load_dotenv
from typing import List

# Load environment variables
load_dotenv()

class Config:
    """Configuration management for the AI monitoring system"""
    
    # Twilio Settings
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
    YOUR_PHONE_NUMBER = os.getenv('YOUR_PHONE_NUMBER')
    
    # Camera Settings
    CAMERA_INDEX = int(os.getenv('CAMERA_INDEX', 0))
    CAMERA_WIDTH = int(os.getenv('CAMERA_WIDTH', 640))
    CAMERA_HEIGHT = int(os.getenv('CAMERA_HEIGHT', 480))
    
    # Detection Thresholds
    EMOTION_CONFIDENCE_THRESHOLD = float(os.getenv('EMOTION_CONFIDENCE_THRESHOLD', 0.7))
    OBJECT_CONFIDENCE_THRESHOLD = float(os.getenv('OBJECT_CONFIDENCE_THRESHOLD', 0.5))
    
    # Alert Settings
    ALERT_COOLDOWN_SECONDS = int(os.getenv('ALERT_COOLDOWN_SECONDS', 30))
    SAVE_IMAGES = os.getenv('SAVE_IMAGES', 'true').lower() == 'true'
    IMAGES_DIR = os.getenv('IMAGES_DIR', './detected_images')
    
    # Monitoring Schedule
    MONITOR_24_7 = os.getenv('MONITOR_24_7', 'true').lower() == 'true'
    MONITOR_START_TIME = os.getenv('MONITOR_START_TIME', '00:00')
    MONITOR_END_TIME = os.getenv('MONITOR_END_TIME', '23:59')
    
    # Alert Objects and Emotions
    ALERT_OBJECTS = os.getenv('ALERT_OBJECTS', 'person,knife,gun,bottle').split(',')
    ALERT_EMOTIONS = os.getenv('ALERT_EMOTIONS', 'angry,fear,surprise').split(',')
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate required configuration"""
        required_fields = [
            cls.TWILIO_ACCOUNT_SID,
            cls.TWILIO_AUTH_TOKEN,
            cls.TWILIO_PHONE_NUMBER,
            cls.YOUR_PHONE_NUMBER
        ]
        
        missing_fields = [field for field in required_fields if not field]
        
        if missing_fields:
            print("❌ Missing required configuration:")
            if not cls.TWILIO_ACCOUNT_SID:
                print("  - TWILIO_ACCOUNT_SID")
            if not cls.TWILIO_AUTH_TOKEN:
                print("  - TWILIO_AUTH_TOKEN")
            if not cls.TWILIO_PHONE_NUMBER:
                print("  - TWILIO_PHONE_NUMBER")
            if not cls.YOUR_PHONE_NUMBER:
                print("  - YOUR_PHONE_NUMBER")
            return False
        
        return True
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories"""
        if cls.SAVE_IMAGES and not os.path.exists(cls.IMAGES_DIR):
            os.makedirs(cls.IMAGES_DIR)
            print(f"📁 Created images directory: {cls.IMAGES_DIR}")