#!/usr/bin/env python3
"""
Aplicación de prueba simple para verificar que FastAPI funciona correctamente.
"""

from fastapi import FastAPI, HTTPException, Header
from datetime import datetime
import uvicorn

# Crear aplicación FastAPI
app = FastAPI(
    title="Steel Rebar Price Predictor - Test",
    description="Aplicación de prueba para verificar funcionalidad básica",
    version="1.0.0"
)

# API Key para testing
API_KEY = "deacero_steel_predictor_2025_key"

def verify_api_key(x_api_key: str = Header(None)):
    """Verificar API key."""
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key required")
    
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return x_api_key

@app.get("/")
async def root():
    """Endpoint raíz con información del servicio."""
    return {
        "service": "Steel Rebar Price Predictor",
        "version": "1.0",
        "documentation_url": "http://localhost:8000/docs",
        "data_sources": ["Yahoo Finance", "Alpha Vantage", "FRED"],
        "last_model_update": datetime.now().isoformat(),
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "steel-rebar-predictor",
        "version": "1.0"
    }

@app.get("/predict/steel-rebar-price")
async def predict_steel_rebar_price(api_key: str = Header(None)):
    """Endpoint de predicción simulado."""
    # Verificar API key
    if not api_key:
        raise HTTPException(status_code=401, detail="API key required")
    
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    # Predicción simulada
    next_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    return {
        "prediction_date": next_day.strftime("%Y-%m-%d"),
        "predicted_price_usd_per_ton": 750.45,
        "currency": "USD",
        "unit": "metric ton",
        "model_confidence": 0.85,
        "timestamp": datetime.now().isoformat() + "Z",
        "note": "Esta es una predicción simulada para testing"
    }

@app.get("/test")
async def test_endpoint():
    """Endpoint de prueba sin autenticación."""
    return {
        "message": "¡La aplicación está funcionando correctamente!",
        "timestamp": datetime.now().isoformat(),
        "python_version": "3.13.7",
        "fastapi_version": "0.117.1"
    }

if __name__ == "__main__":
    print("🏗️ Steel Rebar Price Predictor - Aplicación de Prueba")
    print("=" * 50)
    print("🚀 Iniciando servidor de prueba...")
    print("📍 URL: http://localhost:8000")
    print("📖 Documentación: http://localhost:8000/docs")
    print("🧪 Test endpoint: http://localhost:8000/test")
    print("🔑 API Key: deacero_steel_predictor_2025_key")
    print("⏹️ Presiona Ctrl+C para detener")
    print("-" * 50)
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
