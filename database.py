import sqlite3
import json
import datetime
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Alert:
    id: Optional[int]
    timestamp: str
    alert_type: str  # 'theft', 'emotion', 'object', 'motion'
    confidence: float
    description: str
    camera_id: str
    zone_id: Optional[str]
    image_path: Optional[str]
    status: str  # 'new', 'acknowledged', 'resolved'
    metadata: Dict[str, Any]

@dataclass
class Camera:
    id: str
    name: str
    location: str
    ip_address: Optional[str]
    rtsp_url: Optional[str]
    status: str  # 'active', 'inactive', 'error'
    last_seen: Optional[str]
    config: Dict[str, Any]

@dataclass
class Zone:
    id: str
    name: str
    description: str
    coordinates: List[Dict[str, int]]  # x, y coordinates
    alert_types: List[str]  # what to monitor in this zone
    status: str  # 'active', 'inactive'

@dataclass
class User:
    id: int
    username: str
    email: str
    password_hash: str
    role: str  # 'admin', 'security', 'viewer'
    created_at: str
    last_login: Optional[str]
    preferences: Dict[str, Any]

class ObscureEyeDatabase:
    def __init__(self, db_path: str = "obscure_eye.db"):
        """Initialize the database with the specified path."""
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get a database connection with proper configuration."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    
    def init_database(self):
        """Initialize the database with all required tables."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Create alerts table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS alerts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        alert_type TEXT NOT NULL,
                        confidence REAL NOT NULL,
                        description TEXT NOT NULL,
                        camera_id TEXT NOT NULL,
                        zone_id TEXT,
                        image_path TEXT,
                        status TEXT DEFAULT 'new',
                        metadata TEXT,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Create cameras table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS cameras (
                        id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        location TEXT NOT NULL,
                        ip_address TEXT,
                        rtsp_url TEXT,
                        status TEXT DEFAULT 'active',
                        last_seen TEXT,
                        config TEXT,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Create zones table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS zones (
                        id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        description TEXT,
                        coordinates TEXT NOT NULL,
                        alert_types TEXT NOT NULL,
                        status TEXT DEFAULT 'active',
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Create users table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        role TEXT DEFAULT 'viewer',
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                        last_login TEXT,
                        preferences TEXT
                    )
                ''')
                
                # Create system_config table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS system_config (
                        key TEXT PRIMARY KEY,
                        value TEXT NOT NULL,
                        description TEXT,
                        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Create indexes for better performance
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_alerts_timestamp ON alerts(timestamp)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_alerts_type ON alerts(alert_type)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_alerts_status ON alerts(status)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_alerts_camera ON alerts(camera_id)')
                
                conn.commit()
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    # Alert operations
    def add_alert(self, alert: Alert) -> int:
        """Add a new alert to the database."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO alerts (timestamp, alert_type, confidence, description, 
                                      camera_id, zone_id, image_path, status, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    alert.timestamp,
                    alert.alert_type,
                    alert.confidence,
                    alert.description,
                    alert.camera_id,
                    alert.zone_id,
                    alert.image_path,
                    alert.status,
                    json.dumps(alert.metadata)
                ))
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            logger.error(f"Error adding alert: {e}")
            raise
    
    def get_alerts(self, limit: int = 100, offset: int = 0, 
                   alert_type: Optional[str] = None, 
                   status: Optional[str] = None,
                   camera_id: Optional[str] = None) -> List[Alert]:
        """Get alerts with optional filtering."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                query = "SELECT * FROM alerts WHERE 1=1"
                params = []
                
                if alert_type:
                    query += " AND alert_type = ?"
                    params.append(alert_type)
                
                if status:
                    query += " AND status = ?"
                    params.append(status)
                
                if camera_id:
                    query += " AND camera_id = ?"
                    params.append(camera_id)
                
                query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
                params.extend([limit, offset])
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                alerts = []
                for row in rows:
                    alert = Alert(
                        id=row['id'],
                        timestamp=row['timestamp'],
                        alert_type=row['alert_type'],
                        confidence=row['confidence'],
                        description=row['description'],
                        camera_id=row['camera_id'],
                        zone_id=row['zone_id'],
                        image_path=row['image_path'],
                        status=row['status'],
                        metadata=json.loads(row['metadata']) if row['metadata'] else {}
                    )
                    alerts.append(alert)
                
                return alerts
        except Exception as e:
            logger.error(f"Error getting alerts: {e}")
            raise
    
    def update_alert_status(self, alert_id: int, status: str) -> bool:
        """Update the status of an alert."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE alerts SET status = ? WHERE id = ?
                ''', (status, alert_id))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error updating alert status: {e}")
            raise
    
    # Camera operations
    def add_camera(self, camera: Camera) -> bool:
        """Add or update a camera in the database."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO cameras (id, name, location, ip_address, 
                                                  rtsp_url, status, last_seen, config)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    camera.id,
                    camera.name,
                    camera.location,
                    camera.ip_address,
                    camera.rtsp_url,
                    camera.status,
                    camera.last_seen,
                    json.dumps(camera.config)
                ))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error adding camera: {e}")
            raise
    
    def get_cameras(self) -> List[Camera]:
        """Get all cameras."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM cameras ORDER BY name')
                rows = cursor.fetchall()
                
                cameras = []
                for row in rows:
                    camera = Camera(
                        id=row['id'],
                        name=row['name'],
                        location=row['location'],
                        ip_address=row['ip_address'],
                        rtsp_url=row['rtsp_url'],
                        status=row['status'],
                        last_seen=row['last_seen'],
                        config=json.loads(row['config']) if row['config'] else {}
                    )
                    cameras.append(camera)
                
                return cameras
        except Exception as e:
            logger.error(f"Error getting cameras: {e}")
            raise
    
    def update_camera_status(self, camera_id: str, status: str, last_seen: Optional[str] = None) -> bool:
        """Update camera status and last seen timestamp."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                if last_seen:
                    cursor.execute('''
                        UPDATE cameras SET status = ?, last_seen = ? WHERE id = ?
                    ''', (status, last_seen, camera_id))
                else:
                    cursor.execute('''
                        UPDATE cameras SET status = ? WHERE id = ?
                    ''', (status, camera_id))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error updating camera status: {e}")
            raise
    
    # Zone operations
    def add_zone(self, zone: Zone) -> bool:
        """Add or update a zone in the database."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO zones (id, name, description, coordinates, 
                                                alert_types, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    zone.id,
                    zone.name,
                    zone.description,
                    json.dumps(zone.coordinates),
                    json.dumps(zone.alert_types),
                    zone.status
                ))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error adding zone: {e}")
            raise
    
    def get_zones(self) -> List[Zone]:
        """Get all zones."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM zones ORDER BY name')
                rows = cursor.fetchall()
                
                zones = []
                for row in rows:
                    zone = Zone(
                        id=row['id'],
                        name=row['name'],
                        description=row['description'],
                        coordinates=json.loads(row['coordinates']),
                        alert_types=json.loads(row['alert_types']),
                        status=row['status']
                    )
                    zones.append(zone)
                
                return zones
        except Exception as e:
            logger.error(f"Error getting zones: {e}")
            raise
    
    # User operations
    def add_user(self, username: str, email: str, password_hash: str, role: str = 'viewer') -> int:
        """Add a new user to the database."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO users (username, email, password_hash, role)
                    VALUES (?, ?, ?, ?)
                ''', (username, email, password_hash, role))
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            logger.error(f"Error adding user: {e}")
            raise
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get a user by username."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
                row = cursor.fetchone()
                
                if row:
                    return User(
                        id=row['id'],
                        username=row['username'],
                        email=row['email'],
                        password_hash=row['password_hash'],
                        role=row['role'],
                        created_at=row['created_at'],
                        last_login=row['last_login'],
                        preferences=json.loads(row['preferences']) if row['preferences'] else {}
                    )
                return None
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            raise
    
    # System configuration operations
    def set_config(self, key: str, value: str, description: str = "") -> bool:
        """Set a system configuration value."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO system_config (key, value, description, updated_at)
                    VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                ''', (key, value, description))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error setting config: {e}")
            raise
    
    def get_config(self, key: str) -> Optional[str]:
        """Get a system configuration value."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT value FROM system_config WHERE key = ?', (key,))
                row = cursor.fetchone()
                return row['value'] if row else None
        except Exception as e:
            logger.error(f"Error getting config: {e}")
            raise
    
    # Statistics and analytics
    def get_alert_statistics(self, days: int = 7) -> Dict[str, Any]:
        """Get alert statistics for the specified number of days."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Total alerts in the period
                cursor.execute('''
                    SELECT COUNT(*) as total_alerts,
                           COUNT(CASE WHEN status = 'new' THEN 1 END) as new_alerts,
                           COUNT(CASE WHEN status = 'acknowledged' THEN 1 END) as acknowledged_alerts,
                           COUNT(CASE WHEN status = 'resolved' THEN 1 END) as resolved_alerts
                    FROM alerts 
                    WHERE timestamp >= datetime('now', '-{} days')
                '''.format(days))
                
                stats = cursor.fetchone()
                
                # Alerts by type
                cursor.execute('''
                    SELECT alert_type, COUNT(*) as count
                    FROM alerts 
                    WHERE timestamp >= datetime('now', '-{} days')
                    GROUP BY alert_type
                '''.format(days))
                
                alerts_by_type = {row['alert_type']: row['count'] for row in cursor.fetchall()}
                
                return {
                    'total_alerts': stats['total_alerts'],
                    'new_alerts': stats['new_alerts'],
                    'acknowledged_alerts': stats['acknowledged_alerts'],
                    'resolved_alerts': stats['resolved_alerts'],
                    'alerts_by_type': alerts_by_type
                }
        except Exception as e:
            logger.error(f"Error getting alert statistics: {e}")
            raise
    
    def cleanup_old_alerts(self, days: int = 30) -> int:
        """Clean up alerts older than specified days."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    DELETE FROM alerts 
                    WHERE timestamp < datetime('now', '-{} days')
                '''.format(days))
                deleted_count = cursor.rowcount
                conn.commit()
                logger.info(f"Cleaned up {deleted_count} old alerts")
                return deleted_count
        except Exception as e:
            logger.error(f"Error cleaning up old alerts: {e}")
            raise

# Global database instance
db = ObscureEyeDatabase()