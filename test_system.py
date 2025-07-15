#!/usr/bin/env python3
"""
Test script for AI Security Monitor System
"""

import cv2
import numpy as np
import time
from datetime import datetime
import sys
import os

# Import our modules
try:
    from config import Config
    from emotion_detector import EmotionDetector
    from object_detector import ObjectDetector
    from sms_notifier import SMSNotifier
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all required files are in the same directory")
    sys.exit(1)

def test_configuration():
    """Test configuration setup"""
    print("🔧 Testing configuration...")
    
    try:
        # Test config loading
        print(f"   Camera index: {Config.CAMERA_INDEX}")
        print(f"   Camera resolution: {Config.CAMERA_WIDTH}x{Config.CAMERA_HEIGHT}")
        print(f"   Emotion threshold: {Config.EMOTION_CONFIDENCE_THRESHOLD}")
        print(f"   Object threshold: {Config.OBJECT_CONFIDENCE_THRESHOLD}")
        print(f"   Alert objects: {Config.ALERT_OBJECTS}")
        print(f"   Alert emotions: {Config.ALERT_EMOTIONS}")
        
        # Test Twilio config
        if Config.validate_config():
            print("✅ Twilio configuration is valid")
        else:
            print("⚠️ Twilio configuration incomplete - SMS features will not work")
            
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_camera():
    """Test camera functionality"""
    print("\n📷 Testing camera...")
    
    try:
        cap = cv2.VideoCapture(Config.CAMERA_INDEX)
        
        if not cap.isOpened():
            print(f"❌ Cannot open camera at index {Config.CAMERA_INDEX}")
            return False
        
        # Set camera properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, Config.CAMERA_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.CAMERA_HEIGHT)
        
        # Test frame capture
        ret, frame = cap.read()
        if not ret:
            print("❌ Cannot read frame from camera")
            cap.release()
            return False
        
        print(f"✅ Camera working - Resolution: {frame.shape[1]}x{frame.shape[0]}")
        
        # Test multiple frames
        for i in range(5):
            ret, frame = cap.read()
            if not ret:
                print(f"⚠️ Failed to read frame {i+1}")
                break
        else:
            print("✅ Camera streaming is stable")
        
        cap.release()
        return True
        
    except Exception as e:
        print(f"❌ Camera test failed: {e}")
        return False

def test_emotion_detection():
    """Test emotion detection"""
    print("\n😊 Testing emotion detection...")
    
    try:
        emotion_detector = EmotionDetector()
        print("✅ Emotion detector initialized")
        
        # Create a test image with a face (simple placeholder)
        test_image = np.zeros((480, 640, 3), dtype=np.uint8)
        test_image.fill(128)  # Gray background
        
        # Draw a simple face-like shape
        cv2.circle(test_image, (320, 240), 100, (200, 200, 200), -1)  # Face
        cv2.circle(test_image, (290, 210), 10, (0, 0, 0), -1)  # Left eye
        cv2.circle(test_image, (350, 210), 10, (0, 0, 0), -1)  # Right eye
        cv2.ellipse(test_image, (320, 260), (30, 15), 0, 0, 180, (0, 0, 0), 2)  # Mouth
        
        # Test detection
        emotions = emotion_detector.detect_emotions(test_image, 0.1)  # Low threshold for test
        
        if emotions:
            print(f"✅ Detected {len(emotions)} faces with emotions")
            for emotion in emotions:
                print(f"   - {emotion['emotion']}: {emotion['confidence']:.2f}")
        else:
            print("⚠️ No emotions detected in test image (this is normal for synthetic faces)")
        
        return True
        
    except Exception as e:
        print(f"❌ Emotion detection test failed: {e}")
        return False

def test_object_detection():
    """Test object detection"""
    print("\n🎯 Testing object detection...")
    
    try:
        object_detector = ObjectDetector()
        print("✅ Object detector initialized")
        
        # Create a test image
        test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        
        # Test detection
        objects = object_detector.detect_objects(test_image, 0.1)  # Low threshold for test
        
        print(f"✅ Object detection test completed - Found {len(objects)} objects")
        
        if objects:
            for obj in objects[:5]:  # Show first 5 objects
                print(f"   - {obj['class_name']}: {obj['confidence']:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Object detection test failed: {e}")
        return False

def test_sms_notification():
    """Test SMS functionality"""
    print("\n📱 Testing SMS notification...")
    
    try:
        sms_notifier = SMSNotifier()
        
        if sms_notifier.client is None:
            print("⚠️ SMS client not initialized - check Twilio credentials")
            return False
        
        print("✅ SMS client initialized")
        
        # Ask user if they want to send a test SMS
        response = input("   Send test SMS? (y/n): ").strip().lower()
        
        if response == 'y':
            success = sms_notifier.test_sms()
            if success:
                print("✅ Test SMS sent successfully")
                return True
            else:
                print("❌ Test SMS failed")
                return False
        else:
            print("⏭️ Skipping SMS test")
            return True
        
    except Exception as e:
        print(f"❌ SMS test failed: {e}")
        return False

def test_integration():
    """Test integration of all components"""
    print("\n🔗 Testing system integration...")
    
    try:
        # Initialize all components
        emotion_detector = EmotionDetector()
        object_detector = ObjectDetector()
        sms_notifier = SMSNotifier()
        
        # Test with camera
        cap = cv2.VideoCapture(Config.CAMERA_INDEX)
        
        if not cap.isOpened():
            print("⚠️ Cannot test integration - camera not available")
            return False
        
        print("📸 Capturing test frame...")
        ret, frame = cap.read()
        
        if not ret:
            print("❌ Cannot capture test frame")
            cap.release()
            return False
        
        # Test processing pipeline
        start_time = time.time()
        
        emotions = emotion_detector.detect_emotions(frame, Config.EMOTION_CONFIDENCE_THRESHOLD)
        objects = object_detector.detect_objects(frame, Config.OBJECT_CONFIDENCE_THRESHOLD)
        
        processing_time = time.time() - start_time
        
        print(f"✅ Processing completed in {processing_time:.2f} seconds")
        print(f"   - Emotions detected: {len(emotions)}")
        print(f"   - Objects detected: {len(objects)}")
        
        # Test image annotation
        annotated_frame = emotion_detector.draw_emotion_annotations(frame, emotions)
        annotated_frame = object_detector.draw_object_annotations(annotated_frame, objects)
        
        print("✅ Frame annotation successful")
        
        # Test alert logic
        alert_emotions = emotion_detector.get_alert_emotions(emotions, Config.ALERT_EMOTIONS)
        alert_objects = object_detector.get_alert_objects(objects, Config.ALERT_OBJECTS)
        
        if alert_emotions or alert_objects:
            print(f"🚨 Alert conditions detected:")
            if alert_emotions:
                print(f"   - Alert emotions: {[e['emotion'] for e in alert_emotions]}")
            if alert_objects:
                print(f"   - Alert objects: {[o['class_name'] for o in alert_objects]}")
        else:
            print("✅ No alert conditions in test frame")
        
        cap.release()
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def test_performance():
    """Test system performance"""
    print("\n⚡ Testing performance...")
    
    try:
        cap = cv2.VideoCapture(Config.CAMERA_INDEX)
        
        if not cap.isOpened():
            print("⚠️ Cannot test performance - camera not available")
            return False
        
        emotion_detector = EmotionDetector()
        object_detector = ObjectDetector()
        
        frame_count = 0
        start_time = time.time()
        test_duration = 10  # seconds
        
        print(f"   Running {test_duration}s performance test...")
        
        while time.time() - start_time < test_duration:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Process frame
            emotions = emotion_detector.detect_emotions(frame, Config.EMOTION_CONFIDENCE_THRESHOLD)
            objects = object_detector.detect_objects(frame, Config.OBJECT_CONFIDENCE_THRESHOLD)
            
            frame_count += 1
        
        elapsed_time = time.time() - start_time
        fps = frame_count / elapsed_time
        
        print(f"✅ Performance test completed:")
        print(f"   - Processed {frame_count} frames in {elapsed_time:.2f} seconds")
        print(f"   - Average FPS: {fps:.2f}")
        
        if fps >= 5:
            print("✅ Performance is good for real-time monitoring")
        elif fps >= 2:
            print("⚠️ Performance is acceptable but may affect responsiveness")
        else:
            print("⚠️ Performance is low - consider optimizing or reducing resolution")
        
        cap.release()
        return True
        
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 AI Security Monitor System - Test Suite")
    print("=" * 60)
    
    tests = [
        ("Configuration", test_configuration),
        ("Camera", test_camera),
        ("Emotion Detection", test_emotion_detection),
        ("Object Detection", test_object_detection),
        ("SMS Notification", test_sms_notification),
        ("System Integration", test_integration),
        ("Performance", test_performance)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test '{test_name}' crashed: {e}")
            failed += 1
    
    # Summary
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {passed/(passed+failed)*100:.1f}%")
    
    if failed == 0:
        print("\n🎉 All tests passed! Your system is ready for monitoring.")
    elif failed <= 2:
        print("\n⚠️ Some tests failed, but core functionality should work.")
        print("Check the failed tests and ensure proper configuration.")
    else:
        print("\n❌ Multiple tests failed. Please check your setup:")
        print("1. Verify all dependencies are installed")
        print("2. Check camera connectivity")
        print("3. Verify Twilio credentials")
        print("4. Run setup.py if you haven't already")
    
    print("\nFor detailed setup instructions, see README.md")

if __name__ == "__main__":
    main()