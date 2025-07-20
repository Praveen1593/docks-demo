#!/usr/bin/env python3
"""
Example integration script showing how to use the database with Obscure Eye AI system.
This demonstrates how to store alerts and run the API server for mobile app access.
"""

import time
import threading
import logging
from ai_database_integration import ai_db
from api_server import app
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start_api_server():
    """Start the Flask API server in a separate thread."""
    try:
        # Set environment variables for the API server
        os.environ.setdefault('API_HOST', '0.0.0.0')
        os.environ.setdefault('API_PORT', '5000')
        os.environ.setdefault('DEBUG', 'False')
        
        logger.info("Starting API server...")
        app.run(
            host=os.environ.get('API_HOST', '0.0.0.0'),
            port=int(os.environ.get('API_PORT', 5000)),
            debug=False,
            use_reloader=False  # Disable reloader when running in thread
        )
    except Exception as e:
        logger.error(f"Error starting API server: {e}")

def example_alert_storage():
    """Example of how to store different types of alerts."""
    try:
        # Register a camera
        ai_db.register_camera(
            camera_id="cam_001",
            name="Main Entrance",
            location="Front Door",
            ip_address="192.168.1.100",
            rtsp_url="rtsp://192.168.1.100:554/stream1"
        )
        
        # Register a zone
        ai_db.register_zone(
            zone_id="zone_001",
            name="Restricted Area",
            description="High-value items storage",
            coordinates=[{'x': 100, 'y': 100}, {'x': 300, 'y': 100}, 
                       {'x': 300, 'y': 300}, {'x': 100, 'y': 300}],
            alert_types=['theft', 'motion', 'object']
        )
        
        # Example 1: Store a theft alert
        theft_alert_id = ai_db.store_theft_alert(
            confidence=0.85,
            description="Suspicious behavior detected - person reaching into restricted area",
            camera_id="cam_001",
            zone_id="zone_001",
            image_path="detected_images/theft_20240115_143022.jpg",
            suspects=1,
            behaviors=['reaching_behavior', 'crouching_behavior'],
            factors=['suspicious_behavior', 'valuables_at_risk']
        )
        logger.info(f"Stored theft alert with ID: {theft_alert_id}")
        
        # Example 2: Store an emotion alert
        emotion_alert_id = ai_db.store_emotion_alert(
            emotions=['angry', 'fear'],
            confidence=0.72,
            camera_id="cam_001",
            zone_id="zone_001",
            image_path="detected_images/emotion_20240115_143025.jpg",
            num_faces=2
        )
        logger.info(f"Stored emotion alert with ID: {emotion_alert_id}")
        
        # Example 3: Store an object alert
        object_alert_id = ai_db.store_object_alert(
            objects=[
                {'name': 'person', 'confidence': 0.89},
                {'name': 'knife', 'confidence': 0.76}
            ],
            confidence=0.82,
            camera_id="cam_001",
            zone_id="zone_001",
            image_path="detected_images/object_20240115_143028.jpg",
            num_objects=2
        )
        logger.info(f"Stored object alert with ID: {object_alert_id}")
        
        # Example 4: Store a motion alert
        motion_alert_id = ai_db.store_motion_alert(
            confidence=0.65,
            camera_id="cam_001",
            zone_id="zone_001",
            image_path="detected_images/motion_20240115_143030.jpg",
            motion_type="rapid_movement",
            motion_area=0.15
        )
        logger.info(f"Stored motion alert with ID: {motion_alert_id}")
        
        # Get recent alerts
        recent_alerts = ai_db.get_recent_alerts(limit=10)
        logger.info(f"Retrieved {len(recent_alerts)} recent alerts")
        
        # Get statistics
        stats = ai_db.get_alert_statistics(days=7)
        logger.info(f"Alert statistics: {stats}")
        
    except Exception as e:
        logger.error(f"Error in example alert storage: {e}")

def integrate_with_existing_ai():
    """
    Example of how to integrate with your existing AI system.
    This shows where you would add database calls in your existing code.
    """
    
    # Example: In your theft_detector.py, you would add something like:
    """
    # When theft is detected:
    if theft_detected:
        alert_id = ai_db.store_theft_alert(
            confidence=theft_confidence,
            description=f"CRITICAL THEFT ALERT - {theft_description}",
            camera_id="cam_001",  # or get from your camera config
            zone_id="zone_001",   # or determine from coordinates
            image_path=alert_image_path,
            suspects=num_suspects,
            behaviors=detected_behaviors,
            factors=contributing_factors
        )
        print(f"Alert stored in database with ID: {alert_id}")
    """
    
    # Example: In your emotion_detector.py:
    """
    # When emotions are detected:
    if emotions_detected:
        alert_id = ai_db.store_emotion_alert(
            emotions=detected_emotions,
            confidence=emotion_confidence,
            camera_id="cam_001",
            zone_id="zone_001",
            image_path=alert_image_path,
            num_faces=num_faces_detected
        )
        print(f"Emotion alert stored in database with ID: {alert_id}")
    """
    
    # Example: In your object_detector.py:
    """
    # When objects are detected:
    if objects_detected:
        alert_id = ai_db.store_object_alert(
            objects=detected_objects_with_confidence,
            confidence=object_confidence,
            camera_id="cam_001",
            zone_id="zone_001",
            image_path=alert_image_path,
            num_objects=len(detected_objects)
        )
        print(f"Object alert stored in database with ID: {alert_id}")
    """
    
    logger.info("Integration examples documented")

def main():
    """Main function to demonstrate the database integration."""
    try:
        logger.info("Starting Obscure Eye Database Integration Example")
        
        # Start the API server in a background thread
        api_thread = threading.Thread(target=start_api_server, daemon=True)
        api_thread.start()
        
        # Wait a moment for the server to start
        time.sleep(2)
        
        # Run the example alert storage
        example_alert_storage()
        
        # Show integration examples
        integrate_with_existing_ai()
        
        logger.info("Database integration example completed")
        logger.info("API server is running on http://localhost:5000")
        logger.info("You can now access the API endpoints from your mobile app")
        
        # Keep the main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutting down...")
            
    except Exception as e:
        logger.error(f"Error in main: {e}")

if __name__ == "__main__":
    main()