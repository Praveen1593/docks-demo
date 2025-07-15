#!/usr/bin/env python3
"""
Setup script for AI Security Monitor System
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_system_dependencies():
    """Install system-level dependencies"""
    print("\n🔧 Installing system dependencies...")
    
    # Detect OS
    if sys.platform.startswith('linux'):
        # Ubuntu/Debian
        commands = [
            "sudo apt-get update",
            "sudo apt-get install -y python3-pip python3-dev",
            "sudo apt-get install -y libopencv-dev python3-opencv",
            "sudo apt-get install -y libgl1-mesa-glx libglib2.0-0",
            "sudo apt-get install -y libsm6 libxext6 libxrender-dev",
            "sudo apt-get install -y libfontconfig1 libice6"
        ]
        
        for cmd in commands:
            if not run_command(cmd, f"Running: {cmd}"):
                print("⚠️ Some system dependencies may have failed to install")
                print("This might affect OpenCV functionality")
                break
                
    elif sys.platform == 'darwin':
        # macOS
        print("🍎 macOS detected")
        if shutil.which('brew'):
            run_command("brew install opencv", "Installing OpenCV via Homebrew")
        else:
            print("⚠️ Homebrew not found. Please install it or install OpenCV manually")
            
    elif sys.platform.startswith('win'):
        # Windows
        print("🪟 Windows detected - dependencies will be installed via pip")
    
    else:
        print(f"⚠️ Unsupported OS: {sys.platform}")

def install_python_dependencies():
    """Install Python packages"""
    print("\n📦 Installing Python dependencies...")
    
    # Upgrade pip first
    run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip")
    
    # Install requirements
    if Path("requirements.txt").exists():
        return run_command(f"{sys.executable} -m pip install -r requirements.txt", 
                          "Installing Python packages from requirements.txt")
    else:
        print("❌ requirements.txt not found!")
        return False

def setup_environment():
    """Setup environment configuration"""
    print("\n⚙️ Setting up environment configuration...")
    
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if not env_example.exists():
        print("❌ .env.example file not found!")
        return False
    
    if not env_file.exists():
        shutil.copy2(env_example, env_file)
        print(f"✅ Created .env file from template")
        print(f"📝 Please edit .env file with your Twilio credentials")
        return True
    else:
        print("📄 .env file already exists")
        return True

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = [
        "detected_images",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def test_camera():
    """Test camera functionality"""
    print("\n📷 Testing camera access...")
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print("✅ Camera test successful")
                print(f"   Resolution: {frame.shape[1]}x{frame.shape[0]}")
            else:
                print("⚠️ Camera opened but cannot read frames")
            cap.release()
            return True
        else:
            print("❌ Cannot open camera")
            return False
            
    except ImportError:
        print("⚠️ OpenCV not installed - camera test skipped")
        return False
    except Exception as e:
        print(f"❌ Camera test failed: {e}")
        return False

def test_imports():
    """Test if all required packages can be imported"""
    print("\n🧪 Testing package imports...")
    
    packages = [
        'cv2',
        'numpy', 
        'tensorflow',
        'fer',
        'ultralytics',
        'twilio',
        'mediapipe'
    ]
    
    failed_imports = []
    
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package}: {e}")
            failed_imports.append(package)
    
    if failed_imports:
        print(f"\n⚠️ Failed to import: {', '.join(failed_imports)}")
        return False
    else:
        print("\n✅ All packages imported successfully")
        return True

def show_next_steps():
    """Show next steps to the user"""
    print("\n" + "="*60)
    print("🎉 Setup completed!")
    print("="*60)
    print("\n📋 Next steps:")
    print("1. Edit the .env file with your Twilio credentials:")
    print("   - Get credentials from https://www.twilio.com")
    print("   - Add your phone numbers")
    print("\n2. Test the system:")
    print("   python ai_monitor.py")
    print("\n3. For 24/7 operation, see README.md for service setup")
    print("\n4. Check the README.md for detailed configuration options")
    print("\n⚠️  Important:")
    print("   - Ensure compliance with local privacy laws")
    print("   - Test thoroughly before production use")
    print("   - Keep dependencies updated for security")

def main():
    """Main setup function"""
    print("🤖 AI Security Monitor System Setup")
    print("="*50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install system dependencies
    install_system_dependencies()
    
    # Install Python dependencies
    if not install_python_dependencies():
        print("❌ Failed to install Python dependencies")
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Create directories
    create_directories()
    
    # Test imports
    if not test_imports():
        print("⚠️ Some packages failed to import - check the installation")
    
    # Test camera
    test_camera()
    
    # Show next steps
    show_next_steps()

if __name__ == "__main__":
    main()