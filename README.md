# 🤖 AI Security Monitor System

A comprehensive 24/7 AI-powered security monitoring system with advanced theft detection, custom model training, and instant multi-channel alerts. Uses computer vision to detect human emotions, objects, suspicious behaviors, and theft scenarios in real-time.

## ✨ Features

### 🔒 **Advanced Theft Detection**
- **Multi-Layer Analysis**: Combines object detection, motion analysis, pose estimation, and behavioral patterns
- **Real-Time Threat Assessment**: Instant evaluation of theft probability with confidence scoring
- **Suspicious Behavior Recognition**: Detects crouching, reaching, erratic movement, and loitering
- **Zone-Based Monitoring**: Configurable restricted and valuable item zones
- **Person Tracking**: Multi-object tracking with behavioral history analysis

### 🤖 **AI Detection Capabilities**
- **Emotion Detection**: Real-time facial expression recognition (anger, fear, surprise, etc.)
- **Object Detection**: Advanced YOLO-based detection for weapons, valuables, and suspicious items
- **Motion Analysis**: Background subtraction and movement pattern analysis
- **Pose Estimation**: MediaPipe-based human pose analysis for suspicious activities

### 🚨 **Instant Alert System**
- **Multi-Channel Alerts**: SMS, sound, file logging, and visual notifications
- **Critical Alert Priority**: Immediate notifications for high-threat scenarios
- **Image Evidence**: Automatic capture and transmission of annotated alert images
- **Smart Cooldowns**: Prevents alert spam with intelligent timing controls
- **Alert Statistics**: Comprehensive logging and reporting

### 🎯 **Custom Model Training**
- **Interactive Data Collection**: Easy training data capture from your camera
- **Visual Annotation Tool**: Click-and-drag bounding box annotation interface
- **YOLOv8 Training**: Custom model training for your specific environment
- **Performance Evaluation**: Model testing and validation tools
- **Real-Time Testing**: Live model performance assessment

### ⚙️ **Configuration & Setup**
- **Zone Configurator**: Interactive tool for setting up monitoring areas
- **Comprehensive Launcher**: Easy-to-use interface for all system functions
- **Flexible Configuration**: Extensive customization options via environment variables
- **24/7 Operation**: Designed for continuous unattended operation

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

**Option A: Use the Comprehensive Launcher (Recommended)**
```bash
# Launch the main control panel
python launch_ai_monitor.py
```

**Option B: Direct Command Line**
```bash
# Run with display window (for testing)
python ai_monitor.py

# For 24/7 headless operation, modify the main() function:
# monitor.run(show_display=False)
```

**Option C: Individual Components**
```bash
# Configure monitoring zones
python zone_configurator.py

# Train custom theft detection model
python model_trainer.py

# Test alert system
python instant_alert_system.py
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

**Critical Theft Alert:**
```
🚨 CRITICAL THEFT ALERT 🚨
Time: 2024-01-15 14:45:30
Type: OBJECT_THEFT
Confidence: 0.92
Alert Level: CRITICAL

Suspects: 2 detected
  Suspect 1: crouching_behavior, reaching_behavior
  Suspect 2: erratic_movement, rapid_movement
Factors: suspicious_behavior, valuables_at_risk, high_motion

⚠️ IMMEDIATE ACTION REQUIRED ⚠️
Location: Camera Monitor
System: AI Theft Detection
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

## 🔒 Advanced Theft Detection

### Theft Detection Capabilities

The system uses multiple AI techniques to detect theft scenarios:

1. **Motion Analysis**: Background subtraction to detect movement patterns
2. **Object Detection**: Identification of valuable items and potential weapons
3. **Pose Estimation**: Analysis of human poses for suspicious behaviors
4. **Person Tracking**: Multi-object tracking with behavioral history
5. **Zone Monitoring**: Restricted and valuable item zone violations
6. **Behavioral Patterns**: Long-term analysis of suspicious activities

### Configuring Monitoring Zones

Use the interactive zone configurator to set up your monitoring areas:

```bash
python zone_configurator.py
```

**Zone Types:**
- **Restricted Zones**: Areas where unauthorized access triggers alerts
- **Valuable Item Zones**: Locations of important items to monitor
- **Entry/Exit Zones**: Monitor people entering and leaving areas

**Controls:**
- Click and drag to draw rectangular zones
- Press R/V/E/X to switch between zone types
- Press S to save configuration
- Press D to delete last zone

### Custom Model Training

Train a specialized theft detection model for your environment:

```bash
python model_trainer.py
```

**Training Process:**
1. **Data Collection**: Capture images of normal and theft scenarios
2. **Annotation**: Use the visual tool to label objects and behaviors
3. **Dataset Creation**: Automatically generate YOLO-format training data
4. **Model Training**: Train custom YOLOv8 model on your data
5. **Evaluation**: Test model performance and accuracy
6. **Integration**: Use trained model in the monitoring system

### Alert System Features

The instant alert system provides multiple notification channels:

**Alert Levels:**
- **LOW**: Standard detections (2-minute cooldown)
- **MEDIUM**: Suspicious activity (1-minute cooldown)
- **HIGH**: Probable theft (30-second cooldown)
- **CRITICAL**: Confirmed theft (10-second cooldown)

**Notification Channels:**
- **SMS**: Instant text messages with details
- **Sound**: Audio alerts with different patterns
- **Visual**: On-screen notifications and annotations
- **File Logging**: Comprehensive alert history
- **Image Evidence**: Automatic capture and annotation

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
├── 🤖 Core System
│   ├── ai_monitor.py              # Main 24/7 monitoring system
│   ├── config.py                  # Configuration management
│   └── launch_ai_monitor.py       # Comprehensive system launcher
│
├── 🔍 Detection Modules
│   ├── emotion_detector.py        # Facial expression recognition
│   ├── object_detector.py         # YOLO object detection
│   ├── theft_detector.py          # Advanced theft detection
│   └── instant_alert_system.py    # Multi-channel alert system
│
├── 🎯 Training & Configuration
│   ├── model_trainer.py           # Custom model training system
│   ├── zone_configurator.py       # Interactive zone setup tool
│   ├── setup.py                   # Automated installation script
│   └── test_system.py             # Comprehensive testing suite
│
├── ⚙️ Configuration
│   ├── requirements.txt           # Python dependencies
│   ├── .env.example              # Environment template
│   ├── .env                      # Your configuration (create this)
│   └── README.md                 # Complete documentation
│
├── 📁 Generated Directories
│   ├── detected_images/          # Alert images (auto-created)
│   │   └── critical/             # Critical theft evidence
│   ├── theft_training_data/      # Training dataset
│   │   ├── images/               # Training images
│   │   ├── labels/               # Annotation labels
│   │   ├── train/                # Training split
│   │   ├── val/                  # Validation split
│   │   └── test/                 # Test split
│   ├── trained_models/           # Custom trained models
│   │   └── theft_detection/      # Theft detection models
│   └── logs/                     # System and alert logs
│       ├── alerts.log            # Alert history
│       └── system.log            # System activity
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