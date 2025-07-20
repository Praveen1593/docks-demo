import datetime
import logging
from typing import Dict, Any, Optional
from database import db, Alert, Camera, Zone
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIDatabaseIntegration:
    """Integration class to connect AI system with database."""
    
    def __init__(self):
        """Initialize the AI database integration."""
        self.db = db
        logger.info("AI Database Integration initialized")
    
    def store_alert(self, alert_type: str, confidence: float, description: str, 
                   camera_id: str, zone_id: Optional[str] = None, 
                   image_path: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> int:
        """
        Store an alert in the database.
        
        Args:
            alert_type: Type of alert ('theft', 'emotion', 'object', 'motion')
            confidence: Confidence score (0.0 to 1.0)
            description: Human-readable description of the alert
            camera_id: ID of the camera that triggered the alert
            zone_id: Optional zone ID where the alert occurred
            image_path: Optional path to the alert image
            metadata: Optional additional data about the alert
            
        Returns:
            Alert ID from the database
        """
        try:
            timestamp = datetime.datetime.now().isoformat()
            
            alert = Alert(
                id=None,  # Will be set by database
                timestamp=timestamp,
                alert_type=alert_type,
                confidence=confidence,
                description=description,
                camera_id=camera_id,
                zone_id=zone_id,
                image_path=image_path,
                status='new',
                metadata=metadata or {}
            )
            
            alert_id = self.db.add_alert(alert)
            logger.info(f"Stored alert {alert_id}: {alert_type} - {description}")
            return alert_id
            
        except Exception as e:
            logger.error(f"Error storing alert: {e}")
            raise
    
    def store_theft_alert(self, confidence: float, description: str, camera_id: str,
                         zone_id: Optional[str] = None, image_path: Optional[str] = None,
                         suspects: Optional[int] = None, behaviors: Optional[list] = None,
                         factors: Optional[list] = None) -> int:
        """
        Store a theft detection alert with specific metadata.
        
        Args:
            confidence: Theft confidence score
            description: Description of the theft event
            camera_id: Camera that detected the theft
            zone_id: Zone where theft occurred
            image_path: Path to the alert image
            suspects: Number of suspects detected
            behaviors: List of suspicious behaviors
            factors: List of contributing factors
            
        Returns:
            Alert ID from the database
        """
        metadata = {
            'alert_level': 'CRITICAL' if confidence > 0.8 else 'HIGH' if confidence > 0.6 else 'MEDIUM',
            'suspects': suspects,
            'behaviors': behaviors or [],
            'factors': factors or [],
            'theft_confidence': confidence
        }
        
        return self.store_alert(
            alert_type='theft',
            confidence=confidence,
            description=description,
            camera_id=camera_id,
            zone_id=zone_id,
            image_path=image_path,
            metadata=metadata
        )
    
    def store_emotion_alert(self, emotions: list, confidence: float, camera_id: str,
                           zone_id: Optional[str] = None, image_path: Optional[str] = None,
                           num_faces: Optional[int] = None) -> int:
        """
        Store an emotion detection alert.
        
        Args:
            emotions: List of detected emotions
            confidence: Overall confidence score
            camera_id: Camera that detected emotions
            zone_id: Zone where emotions were detected
            image_path: Path to the alert image
            num_faces: Number of faces detected
            
        Returns:
            Alert ID from the database
        """
        metadata = {
            'emotions': emotions,
            'num_faces': num_faces,
            'emotion_confidence': confidence
        }
        
        description = f"Detected emotions: {', '.join(emotions)}"
        if num_faces:
            description += f" (Number of faces: {num_faces})"
        
        return self.store_alert(
            alert_type='emotion',
            confidence=confidence,
            description=description,
            camera_id=camera_id,
            zone_id=zone_id,
            image_path=image_path,
            metadata=metadata
        )
    
    def store_object_alert(self, objects: list, confidence: float, camera_id: str,
                          zone_id: Optional[str] = None, image_path: Optional[str] = None,
                          num_objects: Optional[int] = None) -> int:
        """
        Store an object detection alert.
        
        Args:
            objects: List of detected objects with confidence scores
            confidence: Overall confidence score
            camera_id: Camera that detected objects
            zone_id: Zone where objects were detected
            image_path: Path to the alert image
            num_objects: Number of objects detected
            
        Returns:
            Alert ID from the database
        """
        metadata = {
            'objects': objects,
            'num_objects': num_objects,
            'object_confidence': confidence
        }
        
        object_list = [f"{obj['name']} ({obj['confidence']:.2f})" for obj in objects]
        description = f"Detected objects: {', '.join(object_list)}"
        if num_objects:
            description += f" (Number of objects: {num_objects})"
        
        return self.store_alert(
            alert_type='object',
            confidence=confidence,
            description=description,
            camera_id=camera_id,
            zone_id=zone_id,
            image_path=image_path,
            metadata=metadata
        )
    
    def store_motion_alert(self, confidence: float, camera_id: str,
                          zone_id: Optional[str] = None, image_path: Optional[str] = None,
                          motion_type: Optional[str] = None, motion_area: Optional[float] = None) -> int:
        """
        Store a motion detection alert.
        
        Args:
            confidence: Motion confidence score
            camera_id: Camera that detected motion
            zone_id: Zone where motion was detected
            image_path: Path to the alert image
            motion_type: Type of motion detected
            motion_area: Area of motion detected
            
        Returns:
            Alert ID from the database
        """
        metadata = {
            'motion_type': motion_type,
            'motion_area': motion_area,
            'motion_confidence': confidence
        }
        
        description = f"Motion detected"
        if motion_type:
            description += f" ({motion_type})"
        
        return self.store_alert(
            alert_type='motion',
            confidence=confidence,
            description=description,
            camera_id=camera_id,
            zone_id=zone_id,
            image_path=image_path,
            metadata=metadata
        )
    
    def register_camera(self, camera_id: str, name: str, location: str,
                       ip_address: Optional[str] = None, rtsp_url: Optional[str] = None,
                       config: Optional[Dict[str, Any]] = None) -> bool:
        """
        Register a camera in the database.
        
        Args:
            camera_id: Unique camera identifier
            name: Human-readable camera name
            location: Physical location of the camera
            ip_address: Camera IP address
            rtsp_url: RTSP stream URL
            config: Camera configuration
            
        Returns:
            True if successful
        """
        try:
            camera = Camera(
                id=camera_id,
                name=name,
                location=location,
                ip_address=ip_address,
                rtsp_url=rtsp_url,
                status='active',
                last_seen=datetime.datetime.now().isoformat(),
                config=config or {}
            )
            
            success = self.db.add_camera(camera)
            if success:
                logger.info(f"Registered camera: {camera_id} - {name}")
            return success
            
        except Exception as e:
            logger.error(f"Error registering camera: {e}")
            raise
    
    def update_camera_status(self, camera_id: str, status: str) -> bool:
        """
        Update camera status.
        
        Args:
            camera_id: Camera identifier
            status: New status ('active', 'inactive', 'error')
            
        Returns:
            True if successful
        """
        try:
            last_seen = datetime.datetime.now().isoformat() if status == 'active' else None
            success = self.db.update_camera_status(camera_id, status, last_seen)
            
            if success:
                logger.info(f"Updated camera {camera_id} status to: {status}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error updating camera status: {e}")
            raise
    
    def register_zone(self, zone_id: str, name: str, description: str,
                     coordinates: list, alert_types: list) -> bool:
        """
        Register a monitoring zone in the database.
        
        Args:
            zone_id: Unique zone identifier
            name: Zone name
            description: Zone description
            coordinates: List of coordinate dictionaries [{'x': int, 'y': int}, ...]
            alert_types: List of alert types to monitor in this zone
            
        Returns:
            True if successful
        """
        try:
            zone = Zone(
                id=zone_id,
                name=name,
                description=description,
                coordinates=coordinates,
                alert_types=alert_types,
                status='active'
            )
            
            success = self.db.add_zone(zone)
            if success:
                logger.info(f"Registered zone: {zone_id} - {name}")
            return success
            
        except Exception as e:
            logger.error(f"Error registering zone: {e}")
            raise
    
    def get_recent_alerts(self, limit: int = 50, alert_type: Optional[str] = None) -> list:
        """
        Get recent alerts from the database.
        
        Args:
            limit: Maximum number of alerts to return
            alert_type: Optional filter by alert type
            
        Returns:
            List of alert dictionaries
        """
        try:
            alerts = self.db.get_alerts(limit=limit, alert_type=alert_type)
            
            # Convert to dictionary format for easier handling
            alert_dicts = []
            for alert in alerts:
                alert_dict = {
                    'id': alert.id,
                    'timestamp': alert.timestamp,
                    'alert_type': alert.alert_type,
                    'confidence': alert.confidence,
                    'description': alert.description,
                    'camera_id': alert.camera_id,
                    'zone_id': alert.zone_id,
                    'image_path': alert.image_path,
                    'status': alert.status,
                    'metadata': alert.metadata
                }
                alert_dicts.append(alert_dict)
            
            return alert_dicts
            
        except Exception as e:
            logger.error(f"Error getting recent alerts: {e}")
            raise
    
    def get_alert_statistics(self, days: int = 7) -> Dict[str, Any]:
        """
        Get alert statistics for the specified period.
        
        Args:
            days: Number of days to look back
            
        Returns:
            Dictionary with alert statistics
        """
        try:
            return self.db.get_alert_statistics(days=days)
        except Exception as e:
            logger.error(f"Error getting alert statistics: {e}")
            raise
    
    def cleanup_old_alerts(self, days: int = 30) -> int:
        """
        Clean up alerts older than specified days.
        
        Args:
            days: Age threshold for cleanup
            
        Returns:
            Number of alerts deleted
        """
        try:
            return self.db.cleanup_old_alerts(days=days)
        except Exception as e:
            logger.error(f"Error cleaning up old alerts: {e}")
            raise

# Global instance for easy access
ai_db = AIDatabaseIntegration()