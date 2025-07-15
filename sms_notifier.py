import os
import cv2
import time
from datetime import datetime
from twilio.rest import Client
from twilio.base.exceptions import TwilioException
from typing import List, Dict, Optional
import base64
import requests
from config import Config

class SMSNotifier:
    """SMS notification system using Twilio"""
    
    def __init__(self):
        """Initialize the SMS notifier"""
        self.client = None
        self.last_alert_time = {}  # Track last alert time for cooldown
        
        # Initialize Twilio client
        if Config.validate_config():
            try:
                self.client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
                print("✅ Twilio client initialized successfully")
            except Exception as e:
                print(f"❌ Error initializing Twilio client: {e}")
                self.client = None
        else:
            print("❌ Cannot initialize SMS notifier - missing configuration")
    
    def save_alert_image(self, frame, emotions: List[Dict], objects: List[Dict]) -> str:
        """
        Save the alert image with annotations
        
        Args:
            frame: Current frame from camera
            emotions: Detected emotions
            objects: Detected objects
            
        Returns:
            Path to saved image
        """
        if not Config.SAVE_IMAGES:
            return None
            
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"alert_{timestamp}.jpg"
        filepath = os.path.join(Config.IMAGES_DIR, filename)
        
        # Annotate the frame
        annotated_frame = frame.copy()
        
        # Add emotion annotations
        for emotion_data in emotions:
            box = emotion_data['bounding_box']
            emotion = emotion_data['emotion']
            confidence = emotion_data['confidence']
            
            x, y, w, h = box
            cv2.rectangle(annotated_frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            label = f"EMOTION: {emotion.upper()} ({confidence:.2f})"
            cv2.putText(annotated_frame, label, (x, y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Add object annotations
        for obj in objects:
            x1, y1, x2, y2 = obj['bounding_box']
            class_name = obj['class_name']
            confidence = obj['confidence']
            
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            label = f"OBJECT: {class_name.upper()} ({confidence:.2f})"
            cv2.putText(annotated_frame, label, (x1, y1 - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
        # Add timestamp to image
        timestamp_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(annotated_frame, f"ALERT: {timestamp_text}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        
        # Save image
        cv2.imwrite(filepath, annotated_frame)
        print(f"💾 Alert image saved: {filepath}")
        
        return filepath
    
    def send_alert(self, alert_type: str, detected_items: List[Dict], 
                   image_path: Optional[str] = None) -> bool:
        """
        Send SMS alert
        
        Args:
            alert_type: Type of alert ('emotion' or 'object')
            detected_items: List of detected items (emotions or objects)
            image_path: Path to alert image
            
        Returns:
            True if sent successfully, False otherwise
        """
        if self.client is None:
            print("❌ Cannot send SMS - Twilio client not initialized")
            return False
        
        # Check cooldown
        current_time = time.time()
        alert_key = f"{alert_type}_{len(detected_items)}"
        
        if alert_key in self.last_alert_time:
            time_since_last = current_time - self.last_alert_time[alert_key]
            if time_since_last < Config.ALERT_COOLDOWN_SECONDS:
                print(f"⏳ Alert cooldown active ({time_since_last:.1f}s < {Config.ALERT_COOLDOWN_SECONDS}s)")
                return False
        
        # Create alert message
        message = self._create_alert_message(alert_type, detected_items)
        
        try:
            # Send SMS with or without image
            if image_path and os.path.exists(image_path):
                # Upload image to a temporary hosting service or send as MMS
                message_instance = self.client.messages.create(
                    body=message,
                    from_=Config.TWILIO_PHONE_NUMBER,
                    to=Config.YOUR_PHONE_NUMBER,
                    media_url=[f"file://{os.path.abspath(image_path)}"] if image_path else None
                )
            else:
                message_instance = self.client.messages.create(
                    body=message,
                    from_=Config.TWILIO_PHONE_NUMBER,
                    to=Config.YOUR_PHONE_NUMBER
                )
            
            # Update last alert time
            self.last_alert_time[alert_key] = current_time
            
            print(f"📱 SMS Alert sent successfully: {message_instance.sid}")
            return True
            
        except TwilioException as e:
            print(f"❌ Error sending SMS: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error sending SMS: {e}")
            return False
    
    def _create_alert_message(self, alert_type: str, detected_items: List[Dict]) -> str:
        """Create alert message text"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if alert_type == 'emotion':
            emotions = [item['emotion'] for item in detected_items]
            emotions_text = ', '.join(emotions)
            message = f"🚨 EMOTION ALERT - {timestamp}\n"
            message += f"Detected emotions: {emotions_text}\n"
            message += f"Number of faces: {len(detected_items)}\n"
            message += "Location: Camera Monitor\n"
            
        elif alert_type == 'object':
            objects = [f"{item['class_name']} ({item['confidence']:.2f})" for item in detected_items]
            objects_text = ', '.join(objects)
            message = f"🚨 OBJECT ALERT - {timestamp}\n"
            message += f"Detected objects: {objects_text}\n"
            message += f"Number of objects: {len(detected_items)}\n"
            message += "Location: Camera Monitor\n"
            
        else:
            message = f"🚨 SECURITY ALERT - {timestamp}\n"
            message += f"Alert type: {alert_type}\n"
            message += f"Items detected: {len(detected_items)}\n"
        
        message += "\nThis is an automated alert from your AI monitoring system."
        
        return message
    
    def send_system_status(self, status: str) -> bool:
        """Send system status message"""
        if self.client is None:
            return False
            
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = f"🤖 AI Monitor Status - {timestamp}\n{status}"
            
            self.client.messages.create(
                body=message,
                from_=Config.TWILIO_PHONE_NUMBER,
                to=Config.YOUR_PHONE_NUMBER
            )
            
            print(f"📱 Status message sent: {status}")
            return True
            
        except Exception as e:
            print(f"❌ Error sending status message: {e}")
            return False
    
    def test_sms(self) -> bool:
        """Test SMS functionality"""
        if self.client is None:
            print("❌ Cannot test SMS - Twilio client not initialized")
            return False
            
        try:
            message = self.client.messages.create(
                body="🧪 Test message from AI Monitor System - Setup complete!",
                from_=Config.TWILIO_PHONE_NUMBER,
                to=Config.YOUR_PHONE_NUMBER
            )
            
            print(f"✅ Test SMS sent successfully: {message.sid}")
            return True
            
        except Exception as e:
            print(f"❌ Test SMS failed: {e}")
            return False