#!/usr/bin/env python3
"""
Dynamic Confidence Calculator - Calcula confianza del modelo en tiempo real.
Implementa métricas dinámicas basadas en intervalos de predicción, R-cuadrado,
y cálculos de confianza propios para sistemas de producción.
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple, Optional
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import joblib
from datetime import datetime

class DynamicConfidenceCalculator:
    """Calculadora dinámica de confianza para modelos de ML en producción."""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_names = []
        self.historical_performance = {}
        self.confidence_thresholds = {
            'excellent': 0.90,
            'good': 0.80,
            'fair': 0.70,
            'poor': 0.60
        }
    
    def load_model(self, model_path: str):
        """Cargar modelo entrenado."""
        try:
            model_data = joblib.load(model_path)
            self.model = model_data['model']
            self.scaler = model_data['scaler']
            self.feature_names = model_data['feature_names']
            print(f"✅ Modelo cargado exitosamente desde {model_path}")
            return True
        except Exception as e:
            print(f"❌ Error cargando modelo: {e}")
            return False
    
    def calculate_prediction_intervals(self, X_scaled: np.ndarray, confidence_level: float = 0.95) -> Tuple[float, float, float]:
        """Calcular intervalos de predicción usando ensemble de árboles."""
        
        if not hasattr(self.model, 'estimators_'):
            raise ValueError("El modelo debe ser un ensemble para calcular intervalos de predicción")
        
        # Obtener predicciones de todos los árboles
        tree_predictions = np.array([tree.predict(X_scaled) for tree in self.model.estimators_])
        
        # Calcular estadísticas
        mean_prediction = np.mean(tree_predictions, axis=0)
        std_prediction = np.std(tree_predictions, axis=0)
        
        # Calcular intervalos de confianza
        alpha = 1 - confidence_level
        z_score = 1.96  # Para 95% de confianza
        
        lower_bound = mean_prediction - z_score * std_prediction
        upper_bound = mean_prediction + z_score * std_prediction
        
        # Ancho del intervalo (menor ancho = mayor confianza)
        interval_width = upper_bound - lower_bound
        
        return mean_prediction[0], lower_bound[0], upper_bound[0]
    
    def calculate_feature_stability(self, features: np.ndarray) -> float:
        """Calcular estabilidad de features basada en importancia y valores."""
        
        if not hasattr(self.model, 'feature_importances_'):
            return 0.5  # Valor por defecto
        
        # Obtener importancia de features
        feature_importance = self.model.feature_importances_
        
        # Asegurar que features sea un array 1D
        if features.ndim > 1:
            features = features.flatten()
        
        # Normalizar features
        features_normalized = (features - np.mean(features)) / (np.std(features) + 1e-8)
        
        # Calcular estabilidad basada en desviación estándar de features importantes
        top_features_mask = feature_importance > np.percentile(feature_importance, 75)
        top_features_values = features_normalized[top_features_mask]
        
        # Estabilidad inversamente proporcional a la variabilidad
        if len(top_features_values) > 0:
            stability = 1.0 / (1.0 + np.std(top_features_values))
        else:
            stability = 0.5
        
        return min(1.0, max(0.0, stability))
    
    def calculate_data_quality_score(self, data: pd.DataFrame) -> float:
        """Calcular score de calidad de datos."""
        
        # Verificar datos faltantes
        missing_ratio = data.isnull().sum().sum() / (len(data) * len(data.columns))
        
        # Verificar outliers (usando IQR)
        outlier_ratio = 0
        for col in data.select_dtypes(include=[np.number]).columns:
            Q1 = data[col].quantile(0.25)
            Q3 = data[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((data[col] < (Q1 - 1.5 * IQR)) | (data[col] > (Q3 + 1.5 * IQR))).sum()
            outlier_ratio += outliers / len(data)
        
        outlier_ratio = outlier_ratio / len(data.select_dtypes(include=[np.number]).columns)
        
        # Calcular score de calidad (0-1, donde 1 es perfecto)
        quality_score = 1.0 - missing_ratio - outlier_ratio
        return max(0.0, min(1.0, quality_score))
    
    def calculate_temporal_confidence(self, current_date: datetime, last_training_date: datetime) -> float:
        """Calcular confianza basada en la antigüedad del modelo."""
        
        days_since_training = (current_date - last_training_date).days
        
        # Confianza decrece con el tiempo (modelo de decaimiento exponencial)
        decay_factor = 0.01  # 1% de pérdida por día
        temporal_confidence = max(0.5, 1.0 - (days_since_training * decay_factor))
        
        return temporal_confidence
    
    def calculate_market_volatility_impact(self, features: np.ndarray) -> float:
        """Calcular impacto de volatilidad del mercado en la confianza."""
        
        # Asegurar que features sea un array 1D
        if features.ndim > 1:
            features = features.flatten()
        
        # Buscar features relacionados con volatilidad
        volatility_features = [f for f in self.feature_names if 'volatility' in f.lower()]
        
        if not volatility_features:
            return 0.8  # Valor por defecto
        
        # Obtener índices de features de volatilidad
        volatility_indices = []
        for f in volatility_features:
            if f in self.feature_names:
                volatility_indices.append(self.feature_names.index(f))
        
        if not volatility_indices:
            return 0.8
        
        # Calcular volatilidad promedio
        avg_volatility = np.mean([features[i] for i in volatility_indices])
        
        # Normalizar volatilidad (asumiendo que valores altos = mayor incertidumbre)
        max_expected_volatility = 50.0  # Valor de referencia
        normalized_volatility = min(1.0, abs(avg_volatility) / max_expected_volatility)
        
        # Confianza inversamente proporcional a la volatilidad
        volatility_confidence = 1.0 - (normalized_volatility * 0.3)  # Máximo 30% de impacto
        
        return max(0.5, volatility_confidence)
    
    def calculate_dynamic_confidence(self, 
                                   X: np.ndarray, 
                                   data_quality: pd.DataFrame,
                                   current_date: datetime = None,
                                   last_training_date: datetime = None) -> Dict:
        """Calcular confianza dinámica del modelo."""
        
        if current_date is None:
            current_date = datetime.now()
        
        if last_training_date is None:
            last_training_date = datetime.now()
        
        # Escalar features
        X_scaled = self.scaler.transform(X.reshape(1, -1))
        
        # 1. Intervalos de predicción (40% del peso)
        try:
            pred_mean, pred_lower, pred_upper = self.calculate_prediction_intervals(X_scaled)
            interval_width = pred_upper - pred_lower
            interval_confidence = max(0.0, 1.0 - (interval_width / pred_mean)) if pred_mean > 0 else 0.5
        except:
            interval_confidence = 0.5
        
        # 2. Estabilidad de features (20% del peso)
        feature_stability = self.calculate_feature_stability(X[0])
        
        # 3. Calidad de datos (15% del peso)
        data_quality_score = self.calculate_data_quality_score(data_quality)
        
        # 4. Confianza temporal (15% del peso)
        temporal_confidence = self.calculate_temporal_confidence(current_date, last_training_date)
        
        # 5. Impacto de volatilidad del mercado (10% del peso)
        volatility_confidence = self.calculate_market_volatility_impact(X[0])
        
        # Calcular confianza ponderada
        weights = {
            'interval': 0.40,
            'stability': 0.20,
            'quality': 0.15,
            'temporal': 0.15,
            'volatility': 0.10
        }
        
        dynamic_confidence = (
            weights['interval'] * interval_confidence +
            weights['stability'] * feature_stability +
            weights['quality'] * data_quality_score +
            weights['temporal'] * temporal_confidence +
            weights['volatility'] * volatility_confidence
        )
        
        # Ajustar a rango [0.5, 0.98] para evitar valores extremos
        dynamic_confidence = max(0.5, min(0.98, dynamic_confidence))
        
        # Determinar nivel de confianza
        if dynamic_confidence >= self.confidence_thresholds['excellent']:
            confidence_level = 'excellent'
        elif dynamic_confidence >= self.confidence_thresholds['good']:
            confidence_level = 'good'
        elif dynamic_confidence >= self.confidence_thresholds['fair']:
            confidence_level = 'fair'
        else:
            confidence_level = 'poor'
        
        return {
            'dynamic_confidence': dynamic_confidence,
            'confidence_level': confidence_level,
            'components': {
                'interval_confidence': interval_confidence,
                'feature_stability': feature_stability,
                'data_quality_score': data_quality_score,
                'temporal_confidence': temporal_confidence,
                'volatility_confidence': volatility_confidence
            },
            'prediction_interval': {
                'mean': pred_mean,
                'lower_bound': pred_lower,
                'upper_bound': pred_upper,
                'width': pred_upper - pred_lower
            },
            'weights_used': weights
        }

def demo_dynamic_confidence():
    """Demostración del cálculo de confianza dinámica."""
    
    print("🎯 DEMOSTRACIÓN DE CONFIANZA DINÁMICA")
    print("=" * 50)
    
    # Simular componentes de confianza para demostración
    print("📊 Simulando cálculo de confianza dinámica para sistema de producción...")
    
    # Simular diferentes escenarios
    scenarios = [
        {
            'name': 'Escenario Óptimo',
            'dynamic_confidence': 0.923,
            'confidence_level': 'excellent',
            'components': {
                'interval_confidence': 0.95,
                'feature_stability': 0.92,
                'data_quality_score': 0.98,
                'temporal_confidence': 0.95,
                'volatility_confidence': 0.85
            },
            'prediction_interval': {
                'mean': 880.12,
                'lower_bound': 865.45,
                'upper_bound': 894.79,
                'width': 29.34
            }
        },
        {
            'name': 'Escenario Normal',
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
                'width': 59.34
            }
        },
        {
            'name': 'Escenario Volátil',
            'dynamic_confidence': 0.723,
            'confidence_level': 'fair',
            'components': {
                'interval_confidence': 0.70,
                'feature_stability': 0.75,
                'data_quality_score': 0.85,
                'temporal_confidence': 0.80,
                'volatility_confidence': 0.55
            },
            'prediction_interval': {
                'mean': 880.12,
                'lower_bound': 820.45,
                'upper_bound': 939.79,
                'width': 119.34
            }
        }
    ]
    
    weights = {
        'interval': 0.40,
        'stability': 0.20,
        'quality': 0.15,
        'temporal': 0.15,
        'volatility': 0.10
    }
    
    for scenario in scenarios:
        print(f"\n🔍 {scenario['name']}:")
        print(f"   🎯 Confianza Total: {scenario['dynamic_confidence']:.3f} ({scenario['confidence_level'].upper()})")
        
        print(f"\n   📊 Componentes:")
        components = scenario['components']
        print(f"      📈 Intervalos: {components['interval_confidence']:.3f} (peso: {weights['interval']:.0%})")
        print(f"      🏗️ Estabilidad: {components['feature_stability']:.3f} (peso: {weights['stability']:.0%})")
        print(f"      📊 Calidad: {components['data_quality_score']:.3f} (peso: {weights['quality']:.0%})")
        print(f"      ⏰ Temporal: {components['temporal_confidence']:.3f} (peso: {weights['temporal']:.0%})")
        print(f"      📉 Volatilidad: {components['volatility_confidence']:.3f} (peso: {weights['volatility']:.0%})")
        
        print(f"\n   📏 Intervalo de Predicción:")
        interval = scenario['prediction_interval']
        print(f"      💰 Predicción: ${interval['mean']:.2f} USD/ton")
        print(f"      📉 Límite Inferior: ${interval['lower_bound']:.2f} USD/ton")
        print(f"      📈 Límite Superior: ${interval['upper_bound']:.2f} USD/ton")
        print(f"      📊 Ancho: ${interval['width']:.2f} USD/ton")
    
    # Mostrar comparación con confianza estática
    print(f"\n📊 COMPARACIÓN: CONFIANZA DINÁMICA vs ESTÁTICA")
    print("=" * 60)
    
    static_confidence = 0.85
    print(f"   🔒 Confianza Estática (actual): {static_confidence:.3f} (85%)")
    
    for scenario in scenarios:
        diff = scenario['dynamic_confidence'] - static_confidence
        direction = "📈" if diff > 0 else "📉" if diff < 0 else "➡️"
        print(f"   {direction} {scenario['name']}: {scenario['dynamic_confidence']:.3f} ({diff:+.3f})")
    
    print(f"\n💡 BENEFICIOS DE LA CONFIANZA DINÁMICA:")
    print("   ✅ Refleja la calidad real de los datos")
    print("   ✅ Considera la volatilidad del mercado")
    print("   ✅ Ajusta según la antigüedad del modelo")
    print("   ✅ Proporciona intervalos de predicción")
    print("   ✅ Mejora la transparencia para el usuario")
    print("   ✅ Facilita la toma de decisiones informadas")
    
    return scenarios

if __name__ == "__main__":
    demo_dynamic_confidence()
