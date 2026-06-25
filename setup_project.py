#!/usr/bin/env python3
"""
Setup script for ABSA project

This script handles the initial setup of the ABSA project including
dependency installation and directory verification.
"""

import os
import sys
import subprocess


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required.")
        sys.exit(1)
    print(f"✓ Python {sys.version.split()[0]} detected")


def install_requirements():
    """Install requirements from requirements.txt."""
    requirements_file = "requirements.txt"
    
    if not os.path.exists(requirements_file):
        print(f"Error: {requirements_file} not found")
        return False
    
    try:
        print("Installing requirements...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", requirements_file
        ])
        print("✓ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        return False


def verify_directory_structure():
    """Verify that all required directories and files exist."""
    required_dirs = [
        "src",
        "src/core",
        "src/models", 
        "src/utils",
        "tests",
        "config"
    ]
    
    required_files = [
        "src/core/absa_engine.py",
        "src/models/model_manager.py",
        "src/utils/text_processing.py",
        "tests/test_cases.py",
        "config/settings.py",
        "absa_main.py"
    ]
    
    print("Verifying directory structure...")
    
    # Check directories
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✓ Directory {directory} exists")
        else:
            print(f"✗ Directory {directory} missing")
            return False
    
    # Check files
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ File {file_path} exists")
        else:
            print(f"✗ File {file_path} missing")
            return False
    
    return True


def setup_models():
    """Initialize NLP models."""
    print("Setting up NLP models...")
    try:
        from src.models.model_manager import get_model_manager
        
        manager = get_model_manager()
        if manager.setup_all():
            print("✓ NLP models setup complete")
            return True
        else:
            print("✗ NLP models setup failed")
            return False
    except ImportError as e:
        print(f"Error importing model manager: {e}")
        return False


def main():
    """Main setup function."""
    print("ABSA Project Setup")
    print("=" * 40)
    
    # Check Python version
    check_python_version()
    
    # Verify directory structure
    if not verify_directory_structure():
        print("✗ Directory structure verification failed")
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("✗ Requirements installation failed")
        sys.exit(1)
    
    # Setup models (optional - can be done during first run)
    print("\nDo you want to setup NLP models now? (y/n): ", end="")
    try:
        response = input().lower().strip()
        if response in ['y', 'yes']:
            if setup_models():
                print("✓ Complete setup finished successfully!")
            else:
                print("⚠ Setup completed but model initialization failed.")
                print("  Models will be downloaded on first use.")
        else:
            print("✓ Basic setup completed!")
            print("  NLP models will be downloaded on first use.")
    except KeyboardInterrupt:
        print("\n✓ Basic setup completed!")
        print("  NLP models will be downloaded on first use.")
    
    print("\nYou can now run the project with:")
    print("  python absa_main.py")


if __name__ == "__main__":
    main()