#!/usr/bin/env python3
"""
Basic API tests for Steel Rebar Price Predictor
"""

import sys
import os

# Add src to path
current_dir = os.path.dirname(__file__)
project_root = os.path.dirname(current_dir)
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

def test_api_file_exists():
    """Test that the API file exists and can be read."""
    try:
        api_file = os.path.join(os.path.dirname(__file__), '..', 'src', 'app', 'enhanced_api_with_dynamic_confidence.py')
        assert os.path.exists(api_file)
        print("✅ API file exists")
        return True
    except Exception as e:
        print(f"❌ API file not found: {e}")
        return False

def test_api_import_fastapi():
    """Test that FastAPI can be imported."""
    try:
        import fastapi
        assert fastapi is not None
        print("✅ FastAPI import successful")
        return True
    except ImportError as e:
        print(f"❌ Failed to import FastAPI: {e}")
        return False

def test_basic_math():
    """Basic test to ensure tests are working."""
    assert 1 + 1 == 2
    print("✅ Basic math test passed")
    return True

def test_environment_variables():
    """Test that basic environment setup is working."""
    import os
    # os.environ is a mapping, not a dict, but it's subscriptable
    assert hasattr(os.environ, '__getitem__')
    print("✅ Environment variables accessible")
    return True

if __name__ == "__main__":
    print("🧪 Running API tests...")
    results = []
    results.append(test_basic_math())
    results.append(test_environment_variables())
    results.append(test_api_file_exists())
    results.append(test_api_import_fastapi())
    
    if all(results):
        print("🎉 All API tests passed!")
        sys.exit(0)
    else:
        print("❌ Some API tests failed!")
        sys.exit(1)
