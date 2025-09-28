#!/usr/bin/env python3
"""
Steel Rebar Price Predictor - Main Application
API REST para predicción de precios de varilla de acero
"""

import uvicorn
import sys
import os

# Cambiar al directorio del script
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(script_dir, 'src'))

# Importar la app para que esté disponible cuando se ejecute como módulo
try:
    from src.app.enhanced_api_with_dynamic_confidence import app
    print("✅ API imported successfully")
except ImportError as e:
    print(f"❌ Error importing API: {e}")
    sys.exit(1)

if __name__ == "__main__":
    print("🚀 Starting Steel Rebar Price Predictor API...")
    print(f"📁 Working directory: {os.getcwd()}")
    print(f"🐍 Python path: {sys.path[:3]}...")
    
    # Ejecutar la aplicación FastAPI
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )
