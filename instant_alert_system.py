#!/usr/bin/env python3
"""
Instant Alert System for Theft Detection
Provides immediate notifications through multiple channels
"""

import cv2
import time
import asyncio
import threading
import subprocess
from datetime import datetime
from typing import List, Dict, Optional, Callable
from pathlib import Path
import os
import json

# Import notification modules
from sms_notifier import SMSNotifier
from config import Config

class InstantAlertSystem:
    """High-priority instant alert system for theft detection"""
    
    def __init__(self):
        """Initialize the instant alert system"""
        self.sms_notifier = SMSNotifier()
        self.alert_queue = []
        self.processing_alert = False
        self.alert_cooldowns = {}
        
        # Alert channels configuration
        self.channels = {
            'sms': True,
            'email': False,  # Can be enabled later
            'sound': True,
            'file_log': True,
            'webhook': False  # Can be enabled later
        }
        
        # Sound alert configuration
        self.sound_enabled = True
        self.sound_file = "alert_sound.wav"
        
        # File logging
        self.log_file = Path("alerts.log")
        
        # Critical alert thresholds
        self.critical_threshold = 0.8
        self.high_threshold = 0.6
        
        print("🚨 Instant Alert System initialized")
    
    def trigger_theft_alert(self, theft_data: Dict, frame: Optional[cv2.Mat] = None) -> bool:
        """
        Trigger immediate theft alert
        
        Args:
            theft_data: Theft detection results
            frame: Current camera frame
            
        Returns:
            True if alert was triggered successfully
        """
        alert_level = theft_data.get('alert_level', 'LOW')
        confidence = theft_data.get('confidence', 0.0)
        theft_type = theft_data.get('theft_type', 'UNKNOWN')
        
        # Check if this is a critical alert
        is_critical = (alert_level == 'CRITICAL' or 
                      confidence >= self.critical_threshold or
                      theft_type in ['OBJECT_THEFT', 'ORGANIZED_THEFT'])
        
        # Create alert data
        alert_data = {
            'timestamp': datetime.now(),
            'alert_level': alert_level,
            'confidence': confidence,
            'theft_type': theft_type,
            'theft_data': theft_data,
            'is_critical': is_critical,
            'frame': frame
        }
        
        # Process alert immediately if critical
        if is_critical:
            return self._process_critical_alert(alert_data)
        else:
            return self._process_normal_alert(alert_data)
    
    def _process_critical_alert(self, alert_data: Dict) -> bool:
        """Process critical theft alerts immediately"""
        print(f"🚨 CRITICAL THEFT ALERT - {alert_data['theft_type']}")
        
        success_count = 0
        total_channels = 0
        
        # Immediate SMS alert
        if self.channels['sms']:
            total_channels += 1
            if self._send_critical_sms(alert_data):
                success_count += 1
        
        # Sound alert
        if self.channels['sound']:
            total_channels += 1
            if self._play_alert_sound(critical=True):
                success_count += 1
        
        # Save critical image immediately
        if alert_data.get('frame') is not None:
            image_path = self._save_critical_image(alert_data)
            if image_path:
                # Send image via SMS if enabled
                if self.channels['sms']:
                    self._send_image_sms(image_path, alert_data)
        
        # Log critical alert
        if self.channels['file_log']:
            total_channels += 1
            if self._log_alert(alert_data):
                success_count += 1
        
        # Update alert cooldown
        self._update_cooldown(alert_data)
        
        return success_count > 0
    
    def _process_normal_alert(self, alert_data: Dict) -> bool:
        """Process normal priority alerts"""
        alert_key = f"{alert_data['theft_type']}_{alert_data['alert_level']}"
        
        # Check cooldown
        if self._is_in_cooldown(alert_key):
            return False
        
        print(f"⚠️ THEFT ALERT - {alert_data['theft_type']} ({alert_data['alert_level']})")
        
        success_count = 0
        total_channels = 0
        
        # SMS alert
        if self.channels['sms']:
            total_channels += 1
            if self._send_normal_sms(alert_data):
                success_count += 1
        
        # Sound alert
        if self.channels['sound']:
            total_channels += 1
            if self._play_alert_sound(critical=False):
                success_count += 1
        
        # Save image
        if alert_data.get('frame') is not None:
            self._save_alert_image(alert_data)
        
        # Log alert
        if self.channels['file_log']:
            total_channels += 1
            if self._log_alert(alert_data):
                success_count += 1
        
        # Update alert cooldown
        self._update_cooldown(alert_data)
        
        return success_count > 0
    
    def _send_critical_sms(self, alert_data: Dict) -> bool:
        """Send critical SMS alert"""
        try:
            theft_data = alert_data['theft_data']
            timestamp = alert_data['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
            
            message = f"🚨 CRITICAL THEFT ALERT 🚨\n"
            message += f"Time: {timestamp}\n"
            message += f"Type: {alert_data['theft_type']}\n"
            message += f"Confidence: {alert_data['confidence']:.2f}\n"
            message += f"Alert Level: {alert_data['alert_level']}\n\n"
            
            # Add suspicious persons info
            if theft_data.get('suspicious_persons'):
                persons = theft_data['suspicious_persons']
                message += f"Suspects: {len(persons)} detected\n"
                for i, person in enumerate(persons[:3]):  # Limit to 3
                    behaviors = ', '.join(person.get('behaviors', []))
                    message += f"  Suspect {i+1}: {behaviors}\n"
            
            # Add theft factors
            if theft_data.get('theft_factors'):
                factors = ', '.join(theft_data['theft_factors'])
                message += f"Factors: {factors}\n"
            
            message += f"\n⚠️ IMMEDIATE ACTION REQUIRED ⚠️\n"
            message += f"Location: Camera Monitor\n"
            message += f"System: AI Theft Detection"
            
            return self.sms_notifier.client.messages.create(
                body=message,
                from_=Config.TWILIO_PHONE_NUMBER,
                to=Config.YOUR_PHONE_NUMBER
            ) is not None
            
        except Exception as e:
            print(f"❌ Critical SMS failed: {e}")
            return False
    
    def _send_normal_sms(self, alert_data: Dict) -> bool:
        """Send normal priority SMS alert"""
        try:
            theft_data = alert_data['theft_data']
            detected_items = theft_data.get('suspicious_persons', [])
            
            return self.sms_notifier.send_alert(
                'theft', 
                detected_items, 
                None  # Image will be sent separately if needed
            )
            
        except Exception as e:
            print(f"❌ Normal SMS failed: {e}")
            return False
    
    def _send_image_sms(self, image_path: str, alert_data: Dict) -> bool:
        """Send image via SMS"""
        try:
            if not os.path.exists(image_path):
                return False
            
            # Create message with image
            message = f"🚨 THEFT EVIDENCE\n"
            message += f"Time: {alert_data['timestamp'].strftime('%H:%M:%S')}\n"
            message += f"Type: {alert_data['theft_type']}\n"
            message += f"Confidence: {alert_data['confidence']:.2f}"
            
            # Send with image attachment (Note: Twilio MMS)
            return self.sms_notifier.client.messages.create(
                body=message,
                from_=Config.TWILIO_PHONE_NUMBER,
                to=Config.YOUR_PHONE_NUMBER,
                media_url=[f"file://{os.path.abspath(image_path)}"]
            ) is not None
            
        except Exception as e:
            print(f"❌ Image SMS failed: {e}")
            return False
    
    def _play_alert_sound(self, critical: bool = False) -> bool:
        """Play audio alert"""
        if not self.sound_enabled:
            return True
        
        try:
            # Create simple beep pattern
            if critical:
                # Rapid beeps for critical alerts
                duration = 0.1
                frequency = 1000
                for _ in range(5):
                    self._beep(frequency, duration)
                    time.sleep(0.05)
            else:
                # Single beep for normal alerts
                self._beep(800, 0.2)
            
            return True
            
        except Exception as e:
            print(f"⚠️ Sound alert failed: {e}")
            return False
    
    def _beep(self, frequency: int, duration: float):
        """Generate system beep"""
        try:
            # Try different methods based on OS
            if os.name == 'nt':  # Windows
                import winsound
                winsound.Beep(frequency, int(duration * 1000))
            else:  # Linux/Mac
                os.system(f'speaker-test -t sine -f {frequency} -l 1 -s 1 >/dev/null 2>&1 &')
                time.sleep(duration)
                os.system('pkill speaker-test >/dev/null 2>&1')
                
        except Exception:
            # Fallback to system bell
            print('\a', end='', flush=True)
    
    def _save_critical_image(self, alert_data: Dict) -> Optional[str]:
        """Save critical alert image with special naming"""
        if alert_data.get('frame') is None:
            return None
        
        try:
            timestamp = alert_data['timestamp'].strftime("%Y%m%d_%H%M%S")
            theft_type = alert_data['theft_type'].lower()
            confidence = int(alert_data['confidence'] * 100)
            
            filename = f"CRITICAL_THEFT_{theft_type}_{timestamp}_{confidence}.jpg"
            
            # Save to both regular and critical directories
            critical_dir = Path(Config.IMAGES_DIR) / "critical"
            critical_dir.mkdir(exist_ok=True)
            
            image_path = critical_dir / filename
            
            # Annotate frame with critical alert info
            frame = alert_data['frame'].copy()
            
            # Add big red warning
            cv2.rectangle(frame, (0, 0), (frame.shape[1], 100), (0, 0, 255), -1)
            cv2.putText(frame, "CRITICAL THEFT ALERT", (20, 40),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
            cv2.putText(frame, f"{alert_data['theft_type']} - {alert_data['confidence']:.2f}",
                       (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            # Add timestamp
            timestamp_text = alert_data['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
            cv2.putText(frame, timestamp_text, (20, frame.shape[0] - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            
            cv2.imwrite(str(image_path), frame)
            
            print(f"💾 Critical image saved: {image_path}")
            return str(image_path)
            
        except Exception as e:
            print(f"❌ Failed to save critical image: {e}")
            return None
    
    def _save_alert_image(self, alert_data: Dict) -> Optional[str]:
        """Save normal alert image"""
        if alert_data.get('frame') is None:
            return None
        
        try:
            timestamp = alert_data['timestamp'].strftime("%Y%m%d_%H%M%S")
            filename = f"theft_alert_{timestamp}.jpg"
            image_path = Path(Config.IMAGES_DIR) / filename
            
            cv2.imwrite(str(image_path), alert_data['frame'])
            return str(image_path)
            
        except Exception as e:
            print(f"❌ Failed to save alert image: {e}")
            return None
    
    def _log_alert(self, alert_data: Dict) -> bool:
        """Log alert to file"""
        try:
            log_entry = {
                'timestamp': alert_data['timestamp'].isoformat(),
                'alert_level': alert_data['alert_level'],
                'theft_type': alert_data['theft_type'],
                'confidence': alert_data['confidence'],
                'is_critical': alert_data['is_critical'],
                'theft_factors': alert_data['theft_data'].get('theft_factors', []),
                'suspicious_persons_count': len(alert_data['theft_data'].get('suspicious_persons', []))
            }
            
            # Append to log file
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to log alert: {e}")
            return False
    
    def _is_in_cooldown(self, alert_key: str) -> bool:
        """Check if alert type is in cooldown period"""
        if alert_key not in self.alert_cooldowns:
            return False
        
        cooldown_time = self.alert_cooldowns[alert_key]
        current_time = time.time()
        
        # Different cooldowns for different alert levels
        cooldown_duration = {
            'CRITICAL': 10,  # 10 seconds for critical
            'HIGH': 30,      # 30 seconds for high
            'MEDIUM': 60,    # 1 minute for medium
            'LOW': 120       # 2 minutes for low
        }
        
        # Extract alert level from key
        alert_level = alert_key.split('_')[-1] if '_' in alert_key else 'MEDIUM'
        duration = cooldown_duration.get(alert_level, 60)
        
        return (current_time - cooldown_time) < duration
    
    def _update_cooldown(self, alert_data: Dict):
        """Update cooldown for alert type"""
        alert_key = f"{alert_data['theft_type']}_{alert_data['alert_level']}"
        self.alert_cooldowns[alert_key] = time.time()
    
    def test_alert_system(self):
        """Test all alert channels"""
        print("🧪 Testing Instant Alert System...")
        
        # Create test alert data
        test_alert = {
            'timestamp': datetime.now(),
            'alert_level': 'HIGH',
            'confidence': 0.85,
            'theft_type': 'TEST_THEFT',
            'theft_data': {
                'suspicious_persons': [{'person_id': 1, 'behaviors': ['test_behavior']}],
                'theft_factors': ['test_factor']
            },
            'is_critical': False,
            'frame': None
        }
        
        results = {}
        
        # Test SMS
        if self.channels['sms']:
            print("📱 Testing SMS alerts...")
            results['sms'] = self._send_normal_sms(test_alert)
        
        # Test sound
        if self.channels['sound']:
            print("🔊 Testing sound alerts...")
            results['sound'] = self._play_alert_sound(critical=False)
        
        # Test logging
        if self.channels['file_log']:
            print("📝 Testing file logging...")
            results['logging'] = self._log_alert(test_alert)
        
        # Summary
        print("\n📊 Test Results:")
        for channel, success in results.items():
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"   {channel.upper()}: {status}")
        
        return all(results.values())
    
    def get_alert_statistics(self) -> Dict:
        """Get alert statistics from log file"""
        stats = {
            'total_alerts': 0,
            'critical_alerts': 0,
            'alerts_by_type': {},
            'alerts_by_level': {},
            'recent_alerts': []
        }
        
        try:
            if not self.log_file.exists():
                return stats
            
            with open(self.log_file, 'r') as f:
                for line in f:
                    try:
                        alert = json.loads(line.strip())
                        stats['total_alerts'] += 1
                        
                        if alert.get('is_critical'):
                            stats['critical_alerts'] += 1
                        
                        # Count by type
                        theft_type = alert.get('theft_type', 'UNKNOWN')
                        stats['alerts_by_type'][theft_type] = stats['alerts_by_type'].get(theft_type, 0) + 1
                        
                        # Count by level
                        alert_level = alert.get('alert_level', 'UNKNOWN')
                        stats['alerts_by_level'][alert_level] = stats['alerts_by_level'].get(alert_level, 0) + 1
                        
                        # Keep recent alerts (last 10)
                        stats['recent_alerts'].append(alert)
                        if len(stats['recent_alerts']) > 10:
                            stats['recent_alerts'].pop(0)
                            
                    except json.JSONDecodeError:
                        continue
        
        except Exception as e:
            print(f"⚠️ Error reading alert statistics: {e}")
        
        return stats
    
    def print_alert_summary(self):
        """Print alert system summary"""
        stats = self.get_alert_statistics()
        
        print("\n📊 Alert System Summary")
        print("=" * 40)
        print(f"Total Alerts: {stats['total_alerts']}")
        print(f"Critical Alerts: {stats['critical_alerts']}")
        
        if stats['alerts_by_type']:
            print("\nAlerts by Type:")
            for theft_type, count in stats['alerts_by_type'].items():
                print(f"  {theft_type}: {count}")
        
        if stats['alerts_by_level']:
            print("\nAlerts by Level:")
            for level, count in stats['alerts_by_level'].items():
                print(f"  {level}: {count}")
        
        print(f"\nEnabled Channels: {', '.join([k for k, v in self.channels.items() if v])}")
        print(f"Log File: {self.log_file}")

def main():
    """Test the instant alert system"""
    alert_system = InstantAlertSystem()
    
    print("🚨 Instant Alert System Test")
    print("=" * 40)
    
    # Test the system
    alert_system.test_alert_system()
    
    # Show summary
    alert_system.print_alert_summary()

if __name__ == "__main__":
    main()