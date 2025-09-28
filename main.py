#!/usr/bin/env python3
"""
Steel Rebar Price Predictor - Main Application
API REST para predicción de precios de varilla de acero
"""

import uvicorn
import sys
import os

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    # Ejecutar la aplicación FastAPI
    uvicorn.run(
        "src.app.enhanced_api_with_dynamic_confidence:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
