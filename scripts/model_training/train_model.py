#!/usr/bin/env python3
"""
Script para entrenar el modelo de predicción de precios de varilla corrugada.
"""

import os
import sys
import logging
import pandas as pd
from datetime import datetime
from pathlib import Path

# Agregar el directorio app al path
sys.path.append(str(Path(__file__).parent / "app"))

from src.app.services.data_collector import DataCollector
from src.app.models.ml_model import SteelRebarPredictor
from src.app.services.cache_service import CacheService
from src.app.config import settings

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Función principal para entrenar el modelo."""
    print("🏗️ Steel Rebar Price Predictor - Entrenamiento del Modelo")
    print("=" * 60)
    
    try:
        # Inicializar servicios
        print("📊 Inicializando servicios...")
        data_collector = DataCollector()
        ml_model = SteelRebarPredictor()
        cache_service = CacheService(settings.redis_url)
        
        # Recopilar datos
        print("📈 Recopilando datos históricos...")
        economic_data = data_collector.get_all_economic_data()
        
        if not economic_data:
            print("❌ No se pudieron recopilar datos. Verifica la conexión a internet.")
            return False
        
        print(f"✅ Datos recopilados de {len(economic_data)} fuentes:")
        for source, data in economic_data.items():
            print(f"   - {source}: {len(data)} registros")
        
        # Combinar datos para entrenamiento
        print("🔄 Combinando datos para entrenamiento...")
        training_data = data_collector.combine_data_for_training(economic_data)
        
        if training_data.empty:
            print("❌ No se pudieron combinar los datos.")
            return False
        
        print(f"✅ Dataset combinado: {len(training_data)} registros, {len(training_data.columns)} columnas")
        
        # Guardar datos de entrenamiento
        training_data.to_csv("training_data.csv", index=False)
        print("💾 Datos de entrenamiento guardados en training_data.csv")
        
        # Entrenar modelo
        print("🤖 Entrenando modelo...")
        training_result = ml_model.train(training_data)
        
        print("✅ Modelo entrenado exitosamente:")
        print(f"   - Muestras de entrenamiento: {training_result['training_samples']}")
        print(f"   - Número de features: {training_result['feature_count']}")
        print(f"   - Confianza del modelo: {training_result['model_confidence']:.3f}")
        
        # Mostrar importancia de features
        print("\n📊 Top 10 features más importantes:")
        feature_importance = training_result['feature_importance']
        sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
        
        for i, (feature, importance) in enumerate(sorted_features[:10], 1):
            print(f"   {i:2d}. {feature}: {importance:.4f}")
        
        # Guardar modelo
        model_path = "model.joblib"
        ml_model.save_model(model_path)
        print(f"💾 Modelo guardado en {model_path}")
        
        # Cachear datos de entrenamiento
        cache_service.set_training_data(training_data, ttl=86400)  # 24 horas
        print("🗄️ Datos de entrenamiento cacheados")
        
        # Hacer predicción de prueba
        print("\n🧪 Realizando predicción de prueba...")
        try:
            prediction, prediction_details = ml_model.predict(training_data)
            print(f"✅ Predicción de prueba: ${prediction:.2f} USD/ton")
            print(f"   Confianza: {prediction_details['confidence']:.3f}")
        except Exception as e:
            print(f"⚠️ Error en predicción de prueba: {e}")
        
        print("\n🎉 Entrenamiento completado exitosamente!")
        return True
        
    except Exception as e:
        logger.error(f"Error durante el entrenamiento: {e}")
        print(f"❌ Error: {e}")
        return False


def validate_data_quality(data: pd.DataFrame) -> bool:
    """Validar la calidad de los datos."""
    print("🔍 Validando calidad de datos...")
    
    issues = []
    
    # Verificar tamaño mínimo
    if len(data) < 30:
        issues.append(f"Dataset muy pequeño: {len(data)} registros (mínimo 30)")
    
    # Verificar columnas requeridas
    required_cols = ['date', 'price']
    missing_cols = [col for col in required_cols if col not in data.columns]
    if missing_cols:
        issues.append(f"Columnas faltantes: {missing_cols}")
    
    # Verificar valores faltantes
    missing_pct = data.isnull().sum().sum() / (len(data) * len(data.columns)) * 100
    if missing_pct > 20:
        issues.append(f"Muchos valores faltantes: {missing_pct:.1f}%")
    
    # Verificar rango de fechas
    if 'date' in data.columns:
        data['date'] = pd.to_datetime(data['date'])
        date_range = (data['date'].max() - data['date'].min()).days
        if date_range < 30:
            issues.append(f"Rango de fechas muy corto: {date_range} días (mínimo 30)")
    
    if issues:
        print("⚠️ Problemas encontrados en los datos:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    else:
        print("✅ Calidad de datos validada")
        return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
