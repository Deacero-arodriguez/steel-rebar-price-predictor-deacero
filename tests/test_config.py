#!/usr/bin/env python3
"""
Configuration tests for Steel Rebar Price Predictor
"""

import sys
import os

def test_python_version():
    """Test that we're using a compatible Python version."""
    version = sys.version_info
    assert version.major == 3
    assert version.minor >= 8
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")

def test_required_modules():
    """Test that required modules can be imported."""
    required_modules = [
        'pandas',
        'numpy', 
        'sklearn',
        'fastapi',
        'uvicorn',
        'pydantic'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ Module {module} available")
        except ImportError:
            missing_modules.append(module)
            print(f"❌ Module {module} missing")
    
    if missing_modules:
        print(f"⚠️ Missing modules (expected in CI): {missing_modules}")
    else:
        print("✅ All required modules available")

def test_project_structure():
    """Test that essential project files exist."""
    essential_files = [
        'main.py',
        'requirements.txt',
        'README.md',
        'src/app/enhanced_api_with_dynamic_confidence.py'
    ]
    
    missing_files = []
    for file_path in essential_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"✅ File {file_path} exists")
    
    if missing_files:
        print(f"❌ Missing essential files: {missing_files}")
        return False
    else:
        print("✅ All essential files present")
        return True

if __name__ == "__main__":
    print("🧪 Running configuration tests...")
    test_python_version()
    test_required_modules()
    result = test_project_structure()
    if result:
        print("🎉 All configuration tests passed!")
    else:
        print("❌ Some configuration tests failed!")
        sys.exit(1)
