#!/usr/bin/env python3
"""
AI Security Monitor System - Main Launcher
Comprehensive interface for all monitoring features
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """Print system banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                🤖 AI SECURITY MONITOR SYSTEM 🤖               ║
    ║                                                               ║
    ║           Advanced 24/7 Theft Detection & Monitoring         ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """Check if system dependencies are installed"""
    print("🔍 Checking system dependencies...")
    
    required_files = [
        'ai_monitor.py',
        'theft_detector.py',
        'emotion_detector.py',
        'object_detector.py',
        'instant_alert_system.py',
        'model_trainer.py',
        'zone_configurator.py',
        'config.py',
        'requirements.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files present")
    return True

def check_config():
    """Check configuration setup"""
    print("⚙️ Checking configuration...")
    
    env_file = Path('.env')
    if not env_file.exists():
        print("⚠️ .env file not found")
        print("Creating from template...")
        
        env_example = Path('.env.example')
        if env_example.exists():
            import shutil
            shutil.copy2(env_example, env_file)
            print("✅ Created .env file from template")
            print("📝 Please edit .env file with your Twilio credentials")
            return False
        else:
            print("❌ .env.example not found")
            return False
    
    print("✅ Configuration file exists")
    return True

def run_setup():
    """Run system setup"""
    print("🔧 Running system setup...")
    try:
        result = subprocess.run([sys.executable, 'setup.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Setup completed successfully")
            return True
        else:
            print(f"❌ Setup failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Setup error: {e}")
        return False

def run_tests():
    """Run system tests"""
    print("🧪 Running system tests...")
    try:
        result = subprocess.run([sys.executable, 'test_system.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ All tests passed")
            return True
        else:
            print(f"⚠️ Some tests failed. Check output above.")
            return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def launch_monitor(headless=False):
    """Launch the main AI monitor"""
    print(f"🚀 Launching AI Monitor {'(headless mode)' if headless else '(with display)'}...")
    
    try:
        # Modify the main script for headless mode if needed
        if headless:
            print("💡 For headless mode, edit ai_monitor.py to set show_display=False")
        
        subprocess.run([sys.executable, 'ai_monitor.py'])
    except KeyboardInterrupt:
        print("\n🛑 Monitor stopped by user")
    except Exception as e:
        print(f"❌ Monitor error: {e}")

def launch_trainer():
    """Launch the model trainer"""
    print("🎯 Launching Model Training System...")
    try:
        subprocess.run([sys.executable, 'model_trainer.py'])
    except KeyboardInterrupt:
        print("\n🛑 Training stopped by user")
    except Exception as e:
        print(f"❌ Training error: {e}")

def launch_zone_config():
    """Launch zone configurator"""
    print("🎯 Launching Zone Configurator...")
    try:
        subprocess.run([sys.executable, 'zone_configurator.py'])
    except KeyboardInterrupt:
        print("\n🛑 Zone configuration stopped by user")
    except Exception as e:
        print(f"❌ Zone config error: {e}")

def test_alerts():
    """Test alert system"""
    print("🚨 Testing Alert System...")
    try:
        subprocess.run([sys.executable, 'instant_alert_system.py'])
    except Exception as e:
        print(f"❌ Alert test error: {e}")

def show_system_status():
    """Show system status and statistics"""
    print("\n📊 System Status")
    print("=" * 50)
    
    # Check files
    files_status = {
        'Configuration': Path('.env').exists(),
        'Zone Config': Path('theft_zones.json').exists(),
        'Alert Log': Path('alerts.log').exists(),
        'Training Data': Path('theft_training_data').exists(),
        'Trained Models': Path('trained_models').exists()
    }
    
    for item, exists in files_status.items():
        status = "✅ EXISTS" if exists else "❌ MISSING"
        print(f"{item:20}: {status}")
    
    # Show recent alerts if available
    alert_log = Path('alerts.log')
    if alert_log.exists():
        try:
            import json
            with open(alert_log, 'r') as f:
                lines = f.readlines()
                recent_alerts = lines[-5:] if len(lines) >= 5 else lines
            
            if recent_alerts:
                print(f"\n📱 Recent Alerts ({len(recent_alerts)}):")
                for line in recent_alerts:
                    try:
                        alert = json.loads(line.strip())
                        timestamp = alert.get('timestamp', 'Unknown')
                        alert_type = alert.get('theft_type', 'Unknown')
                        level = alert.get('alert_level', 'Unknown')
                        print(f"  {timestamp[:19]} - {alert_type} ({level})")
                    except:
                        continue
        except Exception as e:
            print(f"⚠️ Error reading alert log: {e}")
    
    # Show directories
    print(f"\n📁 Directories:")
    directories = ['detected_images', 'theft_training_data', 'trained_models']
    for directory in directories:
        path = Path(directory)
        if path.exists():
            count = len(list(path.rglob('*'))) if path.is_dir() else 0
            print(f"  {directory:20}: {count} items")
        else:
            print(f"  {directory:20}: ❌ Not found")

def show_quick_start_guide():
    """Show quick start guide"""
    guide = """
    🚀 QUICK START GUIDE
    ══════════════════════

    1. FIRST TIME SETUP:
       • Run option 2 (System Setup) to install dependencies
       • Edit .env file with your Twilio credentials
       • Run option 3 (Test System) to verify everything works

    2. CONFIGURE ZONES (Optional):
       • Run option 7 (Configure Zones) to set up monitoring areas
       • Define restricted zones and valuable item locations

    3. TRAIN CUSTOM MODEL (Optional):
       • Run option 6 (Train Custom Model) to create specialized theft detection
       • Capture training data for your specific environment

    4. START MONITORING:
       • Run option 1 (Start Monitor) to begin 24/7 surveillance
       • System will automatically detect theft and send SMS alerts

    5. CUSTOMIZE SETTINGS:
       • Edit .env file to adjust detection thresholds
       • Configure alert objects and emotions to monitor

    📱 TWILIO SETUP:
       • Sign up at https://www.twilio.com
       • Get Account SID and Auth Token
       • Purchase a phone number for SMS alerts
       • Add credentials to .env file

    📋 IMPORTANT NOTES:
       • Test SMS functionality before relying on alerts
       • Ensure camera permissions are granted
       • Monitor system performance and adjust settings as needed
    """
    print(guide)

def main():
    """Main launcher interface"""
    print_banner()
    
    # Initial checks
    if not check_dependencies():
        print("\n❌ System dependencies check failed")
        print("Please ensure all required files are present")
        return
    
    while True:
        print("\n" + "=" * 60)
        print("🎛️  MAIN CONTROL PANEL")
        print("=" * 60)
        
        print("\n📋 MONITORING:")
        print("  1. 🤖 Start AI Monitor (with display)")
        print("  2. 🖥️  Start AI Monitor (headless)")
        print("  3. 🚨 Test Alert System")
        
        print("\n⚙️  SETUP & CONFIGURATION:")
        print("  4. 🔧 System Setup")
        print("  5. 🧪 Test System")
        print("  6. 🎯 Configure Monitoring Zones")
        
        print("\n🎓 TRAINING & CUSTOMIZATION:")
        print("  7. 🎯 Train Custom Theft Detection Model")
        print("  8. 📊 View Training Data")
        
        print("\n📊 SYSTEM INFO:")
        print("  9. 📈 System Status")
        print(" 10. 📖 Quick Start Guide")
        print(" 11. 🆘 Help & Documentation")
        
        print("\n❌ EXIT:")
        print(" 12. 👋 Exit Launcher")
        
        choice = input("\n🎯 Select option (1-12): ").strip()
        
        if choice == '1':
            if check_config():
                launch_monitor(headless=False)
            else:
                print("⚠️ Please configure system first (option 4)")
        
        elif choice == '2':
            if check_config():
                launch_monitor(headless=True)
            else:
                print("⚠️ Please configure system first (option 4)")
        
        elif choice == '3':
            test_alerts()
        
        elif choice == '4':
            run_setup()
        
        elif choice == '5':
            run_tests()
        
        elif choice == '6':
            launch_zone_config()
        
        elif choice == '7':
            launch_trainer()
        
        elif choice == '8':
            data_dir = Path('theft_training_data')
            if data_dir.exists():
                image_count = len(list(data_dir.glob('**/*.jpg')))
                print(f"📊 Training Data: {image_count} images")
                
                # Show annotation file if exists
                annotations_file = data_dir / 'annotations.json'
                if annotations_file.exists():
                    try:
                        import json
                        with open(annotations_file, 'r') as f:
                            annotations = json.load(f)
                        
                        for category, items in annotations.items():
                            if isinstance(items, list):
                                print(f"  {category}: {len(items)} items")
                    except Exception as e:
                        print(f"⚠️ Error reading annotations: {e}")
            else:
                print("❌ No training data found")
                print("Use option 7 to create training data")
        
        elif choice == '9':
            show_system_status()
        
        elif choice == '10':
            show_quick_start_guide()
        
        elif choice == '11':
            print("\n📖 Help & Documentation")
            print("=" * 40)
            print("📄 README.md - Complete documentation")
            print("🌐 GitHub: Advanced AI security monitoring system")
            print("📧 Issues: Report bugs and feature requests")
            print("📱 Twilio Setup: https://www.twilio.com/docs")
            print("🤖 YOLO Training: https://docs.ultralytics.com/")
            
            # Show key files
            print("\n📁 Key Files:")
            key_files = {
                'ai_monitor.py': 'Main monitoring system',
                'theft_detector.py': 'Advanced theft detection',
                'model_trainer.py': 'Custom model training',
                'zone_configurator.py': 'Zone setup tool',
                'instant_alert_system.py': 'Alert management',
                '.env': 'Configuration file',
                'README.md': 'Complete documentation'
            }
            
            for file, description in key_files.items():
                exists = "✅" if Path(file).exists() else "❌"
                print(f"  {exists} {file:25}: {description}")
        
        elif choice == '12':
            print("\n👋 Thank you for using AI Security Monitor!")
            print("Stay safe and secure! 🛡️")
            break
        
        else:
            print("❌ Invalid option. Please select 1-12.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Launcher interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Launcher error: {e}")
        print("Please check system setup and try again.")