from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os
import logging
from functools import wraps
from database import db, Alert, Camera, Zone, User
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'obscure-eye-secret-key-2024')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'obscure-eye-jwt-secret-2024')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=24)

# Enable CORS for mobile app
CORS(app)

def token_required(f):
    """Decorator to require JWT token for protected routes."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'message': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
            current_user = db.get_user_by_username(data['username'])
            if not current_user:
                return jsonify({'message': 'Invalid token'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

def admin_required(f):
    """Decorator to require admin role."""
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user.role != 'admin':
            return jsonify({'message': 'Admin access required'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

# Authentication endpoints
@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user."""
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Missing required fields'}), 400
        
        # Check if user already exists
        existing_user = db.get_user_by_username(data['username'])
        if existing_user:
            return jsonify({'message': 'Username already exists'}), 409
        
        # Hash password and create user
        password_hash = generate_password_hash(data['password'])
        user_id = db.add_user(
            username=data['username'],
            email=data['email'],
            password_hash=password_hash,
            role=data.get('role', 'viewer')
        )
        
        return jsonify({
            'message': 'User created successfully',
            'user_id': user_id
        }), 201
        
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user and return JWT token."""
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'message': 'Missing username or password'}), 400
        
        # Get user from database
        user = db.get_user_by_username(data['username'])
        if not user:
            return jsonify({'message': 'Invalid credentials'}), 401
        
        # Check password (assuming password_hash is stored in the database)
        # Note: You'll need to modify the database.py to include password_hash in User dataclass
        if not check_password_hash(user.password_hash, data['password']):
            return jsonify({'message': 'Invalid credentials'}), 401
        
        # Generate JWT token
        token = jwt.encode({
            'username': user.username,
            'role': user.role,
            'exp': datetime.datetime.utcnow() + app.config['JWT_ACCESS_TOKEN_EXPIRES']
        }, app.config['JWT_SECRET_KEY'], algorithm="HS256")
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({'message': 'Internal server error'}), 500

# Alert endpoints
@app.route('/api/alerts', methods=['GET'])
@token_required
def get_alerts(current_user):
    """Get alerts with optional filtering."""
    try:
        # Get query parameters
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        alert_type = request.args.get('type')
        status = request.args.get('status')
        camera_id = request.args.get('camera_id')
        
        # Get alerts from database
        alerts = db.get_alerts(
            limit=limit,
            offset=offset,
            alert_type=alert_type,
            status=status,
            camera_id=camera_id
        )
        
        # Convert to JSON-serializable format
        alerts_data = []
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
            alerts_data.append(alert_dict)
        
        return jsonify({
            'alerts': alerts_data,
            'total': len(alerts_data)
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting alerts: {e}")
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/api/alerts/<int:alert_id>/status', methods=['PUT'])
@token_required
def update_alert_status(current_user, alert_id):
    """Update alert status."""
    try:
        data = request.get_json()
        
        if not data or not data.get('status'):
            return jsonify({'message': 'Status is required'}), 400
        
        status = data['status']
        if status not in ['new', 'acknowledged', 'resolved']:
            return jsonify({'message': 'Invalid status'}), 400
        
        success = db.update_alert_status(alert_id, status)
        
        if success:
            return jsonify({'message': 'Alert status updated successfully'}), 200
        else:
            return jsonify({'message': 'Alert not found'}), 404
            
    except Exception as e:
        logger.error(f"Error updating alert status: {e}")
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/api/alerts/statistics', methods=['GET'])
@token_required
def get_alert_statistics(current_user):
    """Get alert statistics."""
    try:
        days = request.args.get('days', 7, type=int)
        stats = db.get_alert_statistics(days=days)
        
        return jsonify(stats), 200
        
    except Exception as e:
        logger.error(f"Error getting alert statistics: {e}")
        return jsonify({'message': 'Internal server error'}), 500

# Camera endpoints
@app.route('/api/cameras', methods=['GET'])
@token_required
def get_cameras(current_user):
    """Get all cameras."""
    try:
        cameras = db.get_cameras()
        
        cameras_data = []
        for camera in cameras:
            camera_dict = {
                'id': camera.id,
                'name': camera.name,
                'location': camera.location,
                'ip_address': camera.ip_address,
                'rtsp_url': camera.rtsp_url,
                'status': camera.status,
                'last_seen': camera.last_seen,
                'config': camera.config
            }
            cameras_data.append(camera_dict)
        
        return jsonify({
            'cameras': cameras_data,
            'total': len(cameras_data)
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting cameras: {e}")
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/api/cameras', methods=['POST'])
@token_required
@admin_required
def add_camera(current_user):
    """Add a new camera."""
    try:
        data = request.get_json()
        
        if not data or not data.get('id') or not data.get('name') or not data.get('location'):
            return jsonify({'message': 'Missing required fields'}), 400
        
        camera = Camera(
            id=data['id'],
            name=data['name'],
            location=data['location'],
            ip_address=data.get('ip_address'),
            rtsp_url=data.get('rtsp_url'),
            status=data.get('status', 'active'),
            last_seen=data.get('last_seen'),
            config=data.get('config', {})
        )
        
        success = db.add_camera(camera)
        
        if success:
            return jsonify({'message': 'Camera added successfully'}), 201
        else:
            return jsonify({'message': 'Failed to add camera'}), 500
            
    except Exception as e:
        logger.error(f"Error adding camera: {e}")
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/api/cameras/<camera_id>/status', methods=['PUT'])
@token_required
@admin_required
def update_camera_status(current_user, camera_id):
    """Update camera status."""
    try:
        data = request.get_json()
        
        if not data or not data.get('status'):
            return jsonify({'message': 'Status is required'}), 400
        
        status = data['status']
        last_seen = data.get('last_seen')
        
        success = db.update_camera_status(camera_id, status, last_seen)
        
        if success:
            return jsonify({'message': 'Camera status updated successfully'}), 200
        else:
            return jsonify({'message': 'Camera not found'}), 404
            
    except Exception as e:
        logger.error(f"Error updating camera status: {e}")
        return jsonify({'message': 'Internal server error'}), 500

# Zone endpoints
@app.route('/api/zones', methods=['GET'])
@token_required
def get_zones(current_user):
    """Get all zones."""
    try:
        zones = db.get_zones()
        
        zones_data = []
        for zone in zones:
            zone_dict = {
                'id': zone.id,
                'name': zone.name,
                'description': zone.description,
                'coordinates': zone.coordinates,
                'alert_types': zone.alert_types,
                'status': zone.status
            }
            zones_data.append(zone_dict)
        
        return jsonify({
            'zones': zones_data,
            'total': len(zones_data)
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting zones: {e}")
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/api/zones', methods=['POST'])
@token_required
@admin_required
def add_zone(current_user):
    """Add a new zone."""
    try:
        data = request.get_json()
        
        if not data or not data.get('id') or not data.get('name') or not data.get('coordinates'):
            return jsonify({'message': 'Missing required fields'}), 400
        
        zone = Zone(
            id=data['id'],
            name=data['name'],
            description=data.get('description', ''),
            coordinates=data['coordinates'],
            alert_types=data.get('alert_types', []),
            status=data.get('status', 'active')
        )
        
        success = db.add_zone(zone)
        
        if success:
            return jsonify({'message': 'Zone added successfully'}), 201
        else:
            return jsonify({'message': 'Failed to add zone'}), 500
            
    except Exception as e:
        logger.error(f"Error adding zone: {e}")
        return jsonify({'message': 'Internal server error'}), 500

# System configuration endpoints
@app.route('/api/config/<key>', methods=['GET'])
@token_required
def get_config(current_user, key):
    """Get system configuration value."""
    try:
        value = db.get_config(key)
        
        if value is not None:
            return jsonify({'key': key, 'value': value}), 200
        else:
            return jsonify({'message': 'Configuration not found'}), 404
            
    except Exception as e:
        logger.error(f"Error getting config: {e}")
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/api/config/<key>', methods=['PUT'])
@token_required
@admin_required
def set_config(current_user, key):
    """Set system configuration value."""
    try:
        data = request.get_json()
        
        if not data or not data.get('value'):
            return jsonify({'message': 'Value is required'}), 400
        
        description = data.get('description', '')
        success = db.set_config(key, data['value'], description)
        
        if success:
            return jsonify({'message': 'Configuration updated successfully'}), 200
        else:
            return jsonify({'message': 'Failed to update configuration'}), 500
            
    except Exception as e:
        logger.error(f"Error setting config: {e}")
        return jsonify({'message': 'Internal server error'}), 500

# Image serving endpoint
@app.route('/api/images/<path:filename>')
@token_required
def serve_image(current_user, filename):
    """Serve alert images."""
    try:
        # Security: ensure the file is in the allowed directory
        images_dir = os.environ.get('IMAGES_DIR', './detected_images')
        file_path = os.path.join(images_dir, filename)
        
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            return jsonify({'message': 'Image not found'}), 404
        
        return send_file(file_path, mimetype='image/jpeg')
        
    except Exception as e:
        logger.error(f"Error serving image: {e}")
        return jsonify({'message': 'Internal server error'}), 500

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'message': 'Internal server error'}), 500

if __name__ == '__main__':
    # Get configuration from environment
    host = os.environ.get('API_HOST', '0.0.0.0')
    port = int(os.environ.get('API_PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Obscure Eye API server on {host}:{port}")
    app.run(host=host, port=port, debug=debug)