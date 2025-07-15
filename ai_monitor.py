#!/usr/bin/env python3
"""
AI Security Monitor - 24/7 Camera Monitoring with Emotion & Object Detection
"""

import cv2
import time
import signal
import sys
from datetime import datetime
from typing import Optional
import numpy as np

from config import Config
from emotion_detector import EmotionDetector
from object_detector import ObjectDetector
from sms_notifier import SMSNotifier

class AIMonitor:
    """Main AI monitoring system"""
    
    def __init__(self):
        """Initialize the AI monitoring system"""
        self.running = False
        self.camera = None
        
        # Initialize components
        print("🚀 Initializing AI Monitor System...")
        
        # Create necessary directories
        Config.create_directories()
        
        # Initialize detectors
        self.emotion_detector = EmotionDetector()
        self.object_detector = ObjectDetector()
        self.sms_notifier = SMSNotifier()
        
        # Statistics
        self.frame_count = 0
        self.start_time = time.time()
        self.last_status_update = time.time()
        
        print("✅ AI Monitor System initialized successfully")
    
    def initialize_camera(self) -> bool:
        """Initialize camera connection"""
        try:
            self.camera = cv2.VideoCapture(Config.CAMERA_INDEX)
            
            if not self.camera.isOpened():
                print(f"❌ Cannot open camera at index {Config.CAMERA_INDEX}")
                return False
            
            # Set camera properties
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, Config.CAMERA_WIDTH)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.CAMERA_HEIGHT)
            self.camera.set(cv2.CAP_PROP_FPS, 30)
            
            # Test camera
            ret, frame = self.camera.read()
            if not ret:
                print("❌ Cannot read from camera")
                return False
            
            print(f"✅ Camera initialized successfully")
            print(f"   Resolution: {frame.shape[1]}x{frame.shape[0]}")
            return True
            
        except Exception as e:
            print(f"❌ Error initializing camera: {e}")
            return False
    
    def process_frame(self, frame: np.ndarray) -> tuple:
        """
        Process a single frame for detection
        
        Args:
            frame: Input frame from camera
            
        Returns:
            Tuple of (emotions, objects, alert_triggered)
        """
        alert_triggered = False
        
        # Detect emotions
        emotions = self.emotion_detector.detect_emotions(
            frame, Config.EMOTION_CONFIDENCE_THRESHOLD
        )
        
        # Detect objects
        objects = self.object_detector.detect_objects(
            frame, Config.OBJECT_CONFIDENCE_THRESHOLD
        )
        
        # Check for alert conditions
        alert_emotions = self.emotion_detector.get_alert_emotions(emotions, Config.ALERT_EMOTIONS)
        alert_objects = self.object_detector.get_alert_objects(objects, Config.ALERT_OBJECTS)
        
        # Send alerts if necessary
        if alert_emotions:
            print(f"🚨 EMOTION ALERT: {[e['emotion'] for e in alert_emotions]}")
            image_path = self.sms_notifier.save_alert_image(frame, alert_emotions, [])
            self.sms_notifier.send_alert('emotion', alert_emotions, image_path)
            alert_triggered = True
            
        if alert_objects:
            print(f"🚨 OBJECT ALERT: {[o['class_name'] for o in alert_objects]}")
            image_path = self.sms_notifier.save_alert_image(frame, [], alert_objects)
            self.sms_notifier.send_alert('object', alert_objects, image_path)
            alert_triggered = True
        
        return emotions, objects, alert_triggered
    
    def create_display_frame(self, frame: np.ndarray, emotions: list, objects: list) -> np.ndarray:
        """Create annotated frame for display"""
        display_frame = frame.copy()
        
        # Add emotion annotations
        display_frame = self.emotion_detector.draw_emotion_annotations(display_frame, emotions)
        
        # Add object annotations
        display_frame = self.object_detector.draw_object_annotations(display_frame, objects)
        
        # Add system info
        self._add_system_info(display_frame)
        
        return display_frame
    
    def _add_system_info(self, frame: np.ndarray):
        """Add system information overlay to frame"""
        # Current time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, f"Time: {current_time}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Frame count and FPS
        elapsed_time = time.time() - self.start_time
        fps = self.frame_count / elapsed_time if elapsed_time > 0 else 0
        cv2.putText(frame, f"Frames: {self.frame_count} | FPS: {fps:.1f}", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # System status
        status = "MONITORING ACTIVE" if self.running else "STOPPED"
        color = (0, 255, 0) if self.running else (0, 0, 255)
        cv2.putText(frame, f"Status: {status}", (10, 90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    
    def send_periodic_status(self):
        """Send periodic status updates"""
        current_time = time.time()
        if current_time - self.last_status_update > 3600:  # Every hour
            elapsed_time = current_time - self.start_time
            fps = self.frame_count / elapsed_time if elapsed_time > 0 else 0
            
            status = f"System running for {elapsed_time/3600:.1f} hours\n"
            status += f"Processed {self.frame_count} frames\n"
            status += f"Average FPS: {fps:.1f}\n"
            status += f"Status: All systems operational"
            
            self.sms_notifier.send_system_status(status)
            self.last_status_update = current_time
    
    def run(self, show_display: bool = True):
        """
        Main monitoring loop
        
        Args:
            show_display: Whether to show the camera feed window
        """
        if not self.initialize_camera():
            return False
        
        # Test SMS functionality
        print("📱 Testing SMS functionality...")
        self.sms_notifier.test_sms()
        
        # Send startup notification
        self.sms_notifier.send_system_status("AI Monitor System started successfully")
        
        self.running = True
        print("🎯 Starting 24/7 monitoring...")
        print("Press 'q' to quit or Ctrl+C to stop")
        
        try:
            while self.running:
                # Read frame from camera
                ret, frame = self.camera.read()
                
                if not ret:
                    print("⚠️ Failed to read frame from camera")
                    time.sleep(1)
                    continue
                
                self.frame_count += 1
                
                # Process frame
                emotions, objects, alert_triggered = self.process_frame(frame)
                
                # Create display frame if needed
                if show_display:
                    display_frame = self.create_display_frame(frame, emotions, objects)
                    
                    # Show frame
                    cv2.imshow('AI Security Monitor', display_frame)
                    
                    # Check for quit key
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        print("🛑 Quit key pressed")
                        break
                
                # Send periodic status
                self.send_periodic_status()
                
                # Print detection info periodically
                if self.frame_count % 30 == 0:  # Every 30 frames
                    emotion_count = len(emotions)
                    object_count = len(objects)
                    if emotion_count > 0 or object_count > 0:
                        print(f"📊 Frame {self.frame_count}: "
                              f"{emotion_count} emotions, {object_count} objects detected")
                
                # Small delay to prevent overwhelming the system
                time.sleep(0.01)
                
        except KeyboardInterrupt:
            print("\n🛑 Keyboard interrupt received")
        except Exception as e:
            print(f"❌ Error in monitoring loop: {e}")
            self.sms_notifier.send_system_status(f"System error: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources"""
        print("🧹 Cleaning up...")
        
        self.running = False
        
        if self.camera:
            self.camera.release()
        
        cv2.destroyAllWindows()
        
        # Send shutdown notification
        elapsed_time = time.time() - self.start_time
        status = f"AI Monitor System stopped after {elapsed_time/3600:.1f} hours\n"
        status += f"Total frames processed: {self.frame_count}"
        
        self.sms_notifier.send_system_status(status)
        
        print("✅ Cleanup completed")

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n🛑 Signal received, shutting down...")
    sys.exit(0)

def main():
    """Main function"""
    signal.signal(signal.SIGINT, signal_handler)
    
    print("🤖 AI Security Monitor System")
    print("=" * 50)
    
    # Check configuration
    if not Config.validate_config():
        print("❌ Configuration validation failed")
        print("Please copy .env.example to .env and fill in your credentials")
        return
    
    # Create and run monitor
    monitor = AIMonitor()
    
    try:
        # For 24/7 headless operation, set show_display=False
        # For development/testing, set show_display=True
        monitor.run(show_display=True)
    except Exception as e:
        print(f"❌ Fatal error: {e}")
    finally:
        monitor.cleanup()

if __name__ == "__main__":
    main()