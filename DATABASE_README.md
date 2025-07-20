# Obscure Eye Database Backend & API

This document explains the database backend and REST API for the Obscure Eye AI Security System, which enables mobile app integration and data persistence.

## 🗄️ Database Overview

The system uses **SQLite** as the local database, providing:
- **Alerts storage** - All AI detection events
- **Camera management** - Camera registration and status tracking
- **Zone configuration** - Monitoring zones and their settings
- **User management** - Authentication and authorization
- **System configuration** - Settings and preferences

## 📊 Database Schema

### Tables

1. **alerts** - Stores all AI detection alerts
   - `id` (PRIMARY KEY)
   - `timestamp` - When the alert occurred
   - `alert_type` - Type of alert (theft, emotion, object, motion)
   - `confidence` - AI confidence score (0.0-1.0)
   - `description` - Human-readable description
   - `camera_id` - Which camera triggered the alert
   - `zone_id` - Zone where alert occurred (optional)
   - `image_path` - Path to alert image (optional)
   - `status` - Alert status (new, acknowledged, resolved)
   - `metadata` - Additional JSON data

2. **cameras** - Camera registration and status
   - `id` (PRIMARY KEY)
   - `name` - Human-readable name
   - `location` - Physical location
   - `ip_address` - Camera IP (optional)
   - `rtsp_url` - RTSP stream URL (optional)
   - `status` - Camera status (active, inactive, error)
   - `last_seen` - Last activity timestamp
   - `config` - Camera configuration (JSON)

3. **zones** - Monitoring zones
   - `id` (PRIMARY KEY)
   - `name` - Zone name
   - `description` - Zone description
   - `coordinates` - Zone boundaries (JSON array)
   - `alert_types` - Types to monitor in this zone
   - `status` - Zone status (active, inactive)

4. **users** - User accounts and authentication
   - `id` (PRIMARY KEY)
   - `username` - Unique username
   - `email` - User email
   - `password_hash` - Hashed password
   - `role` - User role (admin, security, viewer)
   - `created_at` - Account creation time
   - `last_login` - Last login timestamp
   - `preferences` - User preferences (JSON)

5. **system_config** - System configuration
   - `key` (PRIMARY KEY)
   - `value` - Configuration value
   - `description` - Configuration description
   - `updated_at` - Last update timestamp

## 🚀 API Server

The REST API server provides endpoints for:
- **Authentication** - Login/register users
- **Alerts** - Get, filter, and update alerts
- **Cameras** - Manage camera registration and status
- **Zones** - Configure monitoring zones
- **Statistics** - Get alert analytics
- **Images** - Serve alert images
- **Configuration** - System settings

### API Endpoints

#### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token

#### Alerts
- `GET /api/alerts` - Get alerts with filtering
- `PUT /api/alerts/{id}/status` - Update alert status
- `GET /api/alerts/statistics` - Get alert statistics

#### Cameras
- `GET /api/cameras` - Get all cameras
- `POST /api/cameras` - Add new camera (admin only)
- `PUT /api/cameras/{id}/status` - Update camera status (admin only)

#### Zones
- `GET /api/zones` - Get all zones
- `POST /api/zones` - Add new zone (admin only)

#### Configuration
- `GET /api/config/{key}` - Get configuration value
- `PUT /api/config/{key}` - Set configuration value (admin only)

#### Images
- `GET /api/images/{filename}` - Serve alert images

#### Health
- `GET /api/health` - Health check

## 🔧 Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize Database

The database is automatically initialized when you first import the `database` module:

```python
from database import db
# Database will be created as 'obscure_eye.db'
```

### 3. Start API Server

```bash
# Set environment variables (optional)
export API_HOST=0.0.0.0
export API_PORT=5000
export SECRET_KEY=your-secret-key
export JWT_SECRET_KEY=your-jwt-secret

# Start the server
python api_server.py
```

### 4. Test the Integration

```bash
python example_integration.py
```

## 📱 Mobile App Integration

### Authentication Flow

1. **Register/Login**:
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'
```

2. **Use JWT Token**:
```bash
curl -X GET http://localhost:5000/api/alerts \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Example API Calls

#### Get Recent Alerts
```bash
curl -X GET "http://localhost:5000/api/alerts?limit=10&type=theft" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### Update Alert Status
```bash
curl -X PUT http://localhost:5000/api/alerts/1/status \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "acknowledged"}'
```

#### Get Alert Statistics
```bash
curl -X GET "http://localhost:5000/api/alerts/statistics?days=7" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 🔗 Integration with AI System

### Store Alerts from AI Detection

```python
from ai_database_integration import ai_db

# Store theft alert
alert_id = ai_db.store_theft_alert(
    confidence=0.85,
    description="Suspicious behavior detected",
    camera_id="cam_001",
    zone_id="zone_001",
    image_path="path/to/image.jpg",
    suspects=1,
    behaviors=['reaching_behavior'],
    factors=['suspicious_behavior']
)

# Store emotion alert
alert_id = ai_db.store_emotion_alert(
    emotions=['angry', 'fear'],
    confidence=0.72,
    camera_id="cam_001",
    num_faces=2
)

# Store object alert
alert_id = ai_db.store_object_alert(
    objects=[{'name': 'person', 'confidence': 0.89}],
    confidence=0.82,
    camera_id="cam_001"
)
```

### Register Cameras and Zones

```python
# Register camera
ai_db.register_camera(
    camera_id="cam_001",
    name="Main Entrance",
    location="Front Door",
    ip_address="192.168.1.100"
)

# Register zone
ai_db.register_zone(
    zone_id="zone_001",
    name="Restricted Area",
    description="High-value items storage",
    coordinates=[{'x': 100, 'y': 100}, {'x': 300, 'y': 300}],
    alert_types=['theft', 'motion']
)
```

## 🔒 Security Features

- **JWT Authentication** - Secure token-based authentication
- **Role-based Access** - Admin, security, and viewer roles
- **Password Hashing** - Secure password storage
- **CORS Support** - Cross-origin requests for mobile apps
- **Input Validation** - All inputs are validated and sanitized

## 📊 Analytics & Statistics

The system provides comprehensive analytics:

```python
# Get alert statistics for last 7 days
stats = ai_db.get_alert_statistics(days=7)
print(f"Total alerts: {stats['total_alerts']}")
print(f"New alerts: {stats['new_alerts']}")
print(f"Alerts by type: {stats['alerts_by_type']}")
```

## 🗂️ Data Management

### Cleanup Old Data

```python
# Clean up alerts older than 30 days
deleted_count = ai_db.cleanup_old_alerts(days=30)
print(f"Deleted {deleted_count} old alerts")
```

### Backup Database

```bash
# Backup the SQLite database
cp obscure_eye.db obscure_eye_backup_$(date +%Y%m%d).db
```

## 🚀 Production Deployment

### Environment Variables

```bash
# Required for production
export SECRET_KEY=your-very-secure-secret-key
export JWT_SECRET_KEY=your-very-secure-jwt-secret
export API_HOST=0.0.0.0
export API_PORT=5000
export IMAGES_DIR=/path/to/alert/images
export DEBUG=False
```

### Run as Service (Linux)

Create `/etc/systemd/system/obscure-eye-api.service`:

```ini
[Unit]
Description=Obscure Eye API Server
After=network.target

[Service]
Type=simple
User=obscure-eye
WorkingDirectory=/path/to/obscure-eye
ExecStart=/usr/bin/python3 api_server.py
Restart=always
Environment=SECRET_KEY=your-secret-key
Environment=JWT_SECRET_KEY=your-jwt-secret

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable obscure-eye-api
sudo systemctl start obscure-eye-api
```

## 📱 Mobile App Development

### API Base URL
```
http://your-server-ip:5000/api
```

### Required Headers
```
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json
```

### Error Handling
All API endpoints return appropriate HTTP status codes:
- `200` - Success
- `400` - Bad request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not found
- `500` - Internal server error

## 🔧 Troubleshooting

### Common Issues

1. **Database not created**: Ensure write permissions in the directory
2. **API server won't start**: Check if port 5000 is available
3. **Authentication fails**: Verify JWT secret keys are set
4. **CORS errors**: Ensure CORS is properly configured for your mobile app domain

### Logs

Check logs for detailed error information:
```bash
tail -f /var/log/obscure-eye-api.log
```

## 📞 Support

For issues or questions:
1. Check the logs for error messages
2. Verify all environment variables are set
3. Ensure database file has proper permissions
4. Test API endpoints with curl or Postman

---

**Obscure Eye Database & API v1.0**  
*Privacy-First AI Security Monitoring*