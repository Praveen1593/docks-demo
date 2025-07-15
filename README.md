# 🤖 AI Security Monitor System

A comprehensive 24/7 AI-powered security monitoring system that uses computer vision to detect human emotions and objects, sending instant SMS alerts with images to your phone.

## ✨ Features

- **24/7 Camera Monitoring**: Continuous surveillance using your webcam or external camera
- **Emotion Detection**: Real-time facial expression recognition to detect anger, fear, surprise, and other emotions
- **Object Detection**: Advanced YOLO-based detection for persons, weapons, and other objects
- **SMS Alerts**: Instant notifications sent to your phone via Twilio
- **Image Capture**: Automatic saving of alert images with annotations
- **Configurable Thresholds**: Customizable confidence levels and alert triggers
- **Alert Cooldown**: Prevents spam alerts with configurable cooldown periods
- **System Monitoring**: Periodic status updates and health checks

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- Webcam or external USB camera
- Twilio account for SMS functionality
- Linux/macOS/Windows (tested on Ubuntu 22.04)

### 2. Installation

```bash
# Clone or download the project files
cd ai-monitor-system

# Install required dependencies
pip install -r requirements.txt
```

### 3. Configuration

1. Copy the environment template:
```bash
cp .env.example .env
```

2. Edit `.env` with your credentials:
```bash
# Twilio Configuration (Required)
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890  # Your Twilio phone number
YOUR_PHONE_NUMBER=+1987654321    # Your personal phone number

# Camera Configuration
CAMERA_INDEX=0                   # Usually 0 for default webcam
CAMERA_WIDTH=640
CAMERA_HEIGHT=480

# Detection Thresholds (0.0 to 1.0)
EMOTION_CONFIDENCE_THRESHOLD=0.7
OBJECT_CONFIDENCE_THRESHOLD=0.5

# Alert Settings
ALERT_COOLDOWN_SECONDS=30        # Minimum time between similar alerts
SAVE_IMAGES=true                 # Save alert images
IMAGES_DIR=./detected_images     # Directory for saved images

# Objects to monitor (comma-separated)
ALERT_OBJECTS=person,knife,gun,bottle

# Emotions to monitor (comma-separated)
ALERT_EMOTIONS=angry,fear,surprise
```

### 4. Get Twilio Credentials

1. Sign up for a free Twilio account at [twilio.com](https://www.twilio.com)
2. Get your Account SID and Auth Token from the Twilio Console
3. Purchase a Twilio phone number (or use the trial number)
4. Add these credentials to your `.env` file

### 5. Run the System

```bash
# Run with display window (for testing)
python ai_monitor.py

# For 24/7 headless operation, modify the main() function:
# monitor.run(show_display=False)
```

## 📱 SMS Alert Examples

**Emotion Alert:**
```
🚨 EMOTION ALERT - 2024-01-15 14:30:22
Detected emotions: angry, fear
Number of faces: 2
Location: Camera Monitor

This is an automated alert from your AI monitoring system.
```

**Object Alert:**
```
🚨 OBJECT ALERT - 2024-01-15 14:35:10
Detected objects: person (0.89), knife (0.76)
Number of objects: 2
Location: Camera Monitor

This is an automated alert from your AI monitoring system.
```

## 🎛️ Configuration Options

### Detection Thresholds
- `EMOTION_CONFIDENCE_THRESHOLD`: Minimum confidence for emotion detection (0.0-1.0)
- `OBJECT_CONFIDENCE_THRESHOLD`: Minimum confidence for object detection (0.0-1.0)

### Alert Objects
Configure which objects trigger alerts:
```
ALERT_OBJECTS=person,knife,gun,bottle,scissors,car,motorcycle
```

Available objects include: person, car, knife, bottle, gun, phone, laptop, etc.

### Alert Emotions
Configure which emotions trigger alerts:
```
ALERT_EMOTIONS=angry,fear,surprise,disgust,sad
```

Available emotions: angry, fear, surprise, disgust, sad, happy, neutral

### Camera Settings
- `CAMERA_INDEX`: Camera device index (usually 0 for built-in webcam)
- `CAMERA_WIDTH/HEIGHT`: Resolution settings
- Multiple camera support available

## 🛠️ Advanced Usage

### Running as a Service (Linux)

Create a systemd service for 24/7 operation:

```bash
sudo nano /etc/systemd/system/ai-monitor.service
```

```ini
[Unit]
Description=AI Security Monitor
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/ai-monitor-system
ExecStart=/usr/bin/python3 /path/to/ai-monitor-system/ai_monitor.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl enable ai-monitor.service
sudo systemctl start ai-monitor.service
sudo systemctl status ai-monitor.service
```

### Headless Operation

For servers without displays, modify the main function in `ai_monitor.py`:

```python
def main():
    # ... existing code ...
    monitor.run(show_display=False)  # Set to False for headless
```

### Multiple Cameras

To monitor multiple cameras, run separate instances with different camera indices:

```bash
# Terminal 1 - Camera 0
CAMERA_INDEX=0 python ai_monitor.py

# Terminal 2 - Camera 1  
CAMERA_INDEX=1 python ai_monitor.py
```

## 📊 System Monitoring

The system provides:
- Real-time FPS monitoring
- Frame processing statistics
- Hourly status updates via SMS
- Error notifications and recovery
- Automatic restart capabilities

## 🔧 Troubleshooting

### Camera Issues
```bash
# List available cameras
ls /dev/video*

# Test camera access
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK' if cap.isOpened() else 'Camera Failed')"
```

### Dependency Issues
```bash
# Install system dependencies (Ubuntu)
sudo apt-get update
sudo apt-get install python3-opencv python3-pip

# For audio alerts (optional)
sudo apt-get install python3-pygame
```

### SMS Issues
- Verify Twilio credentials
- Check phone number format (+1234567890)
- Ensure sufficient Twilio account balance
- Test with the built-in SMS test function

### Performance Optimization
```python
# Reduce detection frequency for better performance
if self.frame_count % 5 == 0:  # Process every 5th frame
    emotions, objects, alert_triggered = self.process_frame(frame)
```

## 📁 File Structure

```
ai-monitor-system/
├── ai_monitor.py          # Main monitoring script
├── config.py              # Configuration management
├── emotion_detector.py    # Emotion detection module
├── object_detector.py     # Object detection module
├── sms_notifier.py        # SMS notification system
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── .env                  # Your configuration (create this)
├── README.md             # This file
└── detected_images/      # Alert images (auto-created)
```

## 🛡️ Security Considerations

- Keep your `.env` file secure and never commit it to version control
- Use strong Twilio credentials
- Consider firewall rules for network access
- Regularly update dependencies for security patches
- Monitor system logs for unusual activity

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review system logs
3. Test individual components
4. Create an issue with detailed information

---

**⚠️ Important Notes:**
- This system is for personal/educational use
- Ensure compliance with local privacy laws
- Test thoroughly before deploying in production
- Monitor system resource usage
- Keep dependencies updated for security