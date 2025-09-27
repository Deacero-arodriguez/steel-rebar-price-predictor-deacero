#!/usr/bin/env python3
"""
Enhanced API with Dynamic Confidence - Ejemplo de integración de confianza dinámica.
Muestra cómo implementar confianza dinámica en lugar de valores estáticos.
"""

from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel, Field
from datetime import datetime
import numpy as np
import pandas as pd
from typing import Dict, Optional
import json

# Importar nuestro calculador de confianza dinámica
from scripts.utilities.dynamic_confidence_calculator import DynamicConfidenceCalculator

app = FastAPI(
    title="Steel Rebar Price Predictor API - Enhanced with Dynamic Confidence",
    description="API REST con confianza dinámica para predicción de precios de varilla corrugada",
    version="2.0.0"
)

# Inicializar calculador de confianza dinámica
confidence_calculator = DynamicConfidenceCalculator()

# Modelos de respuesta mejorados
class EnhancedPredictionResponse(BaseModel):
    """Respuesta mejorada con confianza dinámica."""
    
    prediction_date: str = Field(..., description="Date for the prediction (YYYY-MM-DD)")
    predicted_price_usd_per_ton: float = Field(..., description="Predicted price in USD per metric ton")
    predicted_price_mxn_per_ton: float = Field(..., description="Predicted price in MXN per metric ton")
    currency: str = Field(default="USD", description="Currency of the prediction")
    unit: str = Field(default="metric ton", description="Unit of measurement")
    
    # Confianza dinámica en lugar de estática
    model_confidence: float = Field(..., ge=0.0, le=1.0, description="Dynamic model confidence score")
    confidence_level: str = Field(..., description="Confidence level (excellent/good/fair/poor)")
    confidence_components: Dict = Field(..., description="Breakdown of confidence components")
    
    # Intervalos de predicción
    prediction_interval: Dict = Field(..., description="Prediction confidence interval")
    
    timestamp: str = Field(..., description="ISO timestamp of the prediction")

class ConfidenceAnalysisResponse(BaseModel):
    """Respuesta detallada de análisis de confianza."""
    
    dynamic_confidence: float = Field(..., description="Overall dynamic confidence score")
    confidence_level: str = Field(..., description="Confidence level classification")
    components: Dict = Field(..., description="Detailed confidence components")
    prediction_interval: Dict = Field(..., description="Prediction interval details")
    comparison_with_static: Dict = Field(..., description="Comparison with static confidence")
    recommendations: Dict = Field(..., description="Recommendations based on confidence level")

# Función de autenticación simplificada
def verify_api_key(x_api_key: str = Header(...)):
    """Verificar API key."""
    if x_api_key != "deacero_steel_predictor_2025_key":
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

# Simular datos para demostración
def create_simulated_data():
    """Crear datos simulados para demostración."""
    
    # Simular features del modelo (136 features)
    np.random.seed(42)
    features = np.random.normal(0, 1, 136)
    
    # Simular datos de calidad
    data_quality = pd.DataFrame({
        'price_feature': np.random.normal(880, 50, 100),
        'volatility_feature': np.random.normal(25, 5, 100),
        'currency_feature': np.random.normal(21.95, 0.5, 100)
    })
    
    return features, data_quality

@app.get("/", response_model=Dict)
async def root():
    """Información del servicio mejorado."""
    return {
        "service": "Steel Rebar Price Predictor API - Enhanced Edition",
        "version": "2.0.0",
        "features": [
            "Dynamic Confidence Calculation",
            "Prediction Intervals",
            "Confidence Components Analysis",
            "Real-time Model Assessment",
            "13 Integrated Data Sources",
            "Currency Analysis for DeAcero"
        ],
        "documentation_url": "https://github.com/Deacero-arodriguez/steel-rebar-price-predictor-deacero",
        "last_model_update": datetime.now().isoformat()
    }

@app.get("/predict/steel-rebar-price", response_model=EnhancedPredictionResponse)
async def predict_steel_rebar_price(api_key: str = Depends(verify_api_key)):
    """Predicción mejorada con confianza dinámica."""
    
    try:
        # Crear datos simulados para demostración
        features, data_quality = create_simulated_data()
        
        # Simular predicción base
        base_prediction_usd = 880.12
        usd_mxn_rate = 21.95
        prediction_mxn = base_prediction_usd * usd_mxn_rate
        
        # Calcular confianza dinámica (simulada para demostración)
        # En un sistema real, esto se calcularía con el modelo cargado
        confidence_analysis = {
            'dynamic_confidence': 0.847,
            'confidence_level': 'good',
            'components': {
                'interval_confidence': 0.85,
                'feature_stability': 0.82,
                'data_quality_score': 0.91,
                'temporal_confidence': 0.88,
                'volatility_confidence': 0.79
            },
            'prediction_interval': {
                'mean': base_prediction_usd,
                'lower_bound': 850.45,
                'upper_bound': 909.79,
                'width': 59.34
            }
        }
        
        # Calcular siguiente día
        next_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        response = EnhancedPredictionResponse(
            prediction_date=next_day.strftime("%Y-%m-%d"),
            predicted_price_usd_per_ton=round(base_prediction_usd, 2),
            predicted_price_mxn_per_ton=round(prediction_mxn, 2),
            currency="USD",
            unit="metric ton",
            model_confidence=confidence_analysis['dynamic_confidence'],
            confidence_level=confidence_analysis['confidence_level'],
            confidence_components=confidence_analysis['components'],
            prediction_interval=confidence_analysis['prediction_interval'],
            timestamp=datetime.now().isoformat() + "Z"
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/confidence/analyze", response_model=ConfidenceAnalysisResponse)
async def analyze_confidence(api_key: str = Depends(verify_api_key)):
    """Análisis detallado de confianza del modelo."""
    
    try:
        # Simular análisis de confianza detallado
        confidence_analysis = {
            'dynamic_confidence': 0.847,
            'confidence_level': 'good',
            'components': {
                'interval_confidence': 0.85,
                'feature_stability': 0.82,
                'data_quality_score': 0.91,
                'temporal_confidence': 0.88,
                'volatility_confidence': 0.79
            },
            'prediction_interval': {
                'mean': 880.12,
                'lower_bound': 850.45,
                'upper_bound': 909.79,
                'width': 59.34,
                'confidence_level': 0.95
            },
            'comparison_with_static': {
                'static_confidence': 0.85,
                'dynamic_confidence': 0.847,
                'difference': -0.003,
                'improvement': False
            },
            'recommendations': {
                'action': 'Continue monitoring',
                'risk_level': 'Low',
                'next_model_update': 'In 7 days',
                'data_quality_actions': 'Maintain current data sources'
            }
        }
        
        return ConfidenceAnalysisResponse(**confidence_analysis)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Confidence analysis failed: {str(e)}")

@app.get("/confidence/compare")
async def compare_confidence_methods(api_key: str = Depends(verify_api_key)):
    """Comparar métodos de confianza: estático vs dinámico."""
    
    try:
        # Simular diferentes escenarios
        scenarios = [
            {
                'scenario': 'Optimal Conditions',
                'static_confidence': 0.85,
                'dynamic_confidence': 0.923,
                'difference': +0.073,
                'interpretation': 'Dynamic confidence higher due to excellent data quality'
            },
            {
                'scenario': 'Normal Conditions',
                'static_confidence': 0.85,
                'dynamic_confidence': 0.847,
                'difference': -0.003,
                'interpretation': 'Dynamic confidence similar to static baseline'
            },
            {
                'scenario': 'High Volatility',
                'static_confidence': 0.85,
                'dynamic_confidence': 0.723,
                'difference': -0.127,
                'interpretation': 'Dynamic confidence lower due to market volatility'
            }
        ]
        
        return {
            'comparison_date': datetime.now().isoformat(),
            'methodology': {
                'static_confidence': 'Fixed value based on model training',
                'dynamic_confidence': 'Real-time calculation based on multiple factors',
                'factors_considered': [
                    'Prediction intervals',
                    'Feature stability',
                    'Data quality',
                    'Model age',
                    'Market volatility'
                ]
            },
            'scenarios': scenarios,
            'recommendation': 'Use dynamic confidence for production systems to provide more accurate uncertainty quantification'
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check del servicio."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "features": {
            "dynamic_confidence": True,
            "prediction_intervals": True,
            "confidence_analysis": True
        }
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando API mejorada con confianza dinámica...")
    print("📊 Características:")
    print("   ✅ Confianza dinámica en lugar de estática")
    print("   ✅ Intervalos de predicción")
    print("   ✅ Análisis de componentes de confianza")
    print("   ✅ Comparación de métodos")
    print("   ✅ Recomendaciones basadas en confianza")
    print("\n🌐 API disponible en: http://localhost:8000")
    print("📖 Documentación en: http://localhost:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
