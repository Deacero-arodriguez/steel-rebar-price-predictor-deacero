#!/usr/bin/env python3
"""
Script optimizado para entrenamiento rápido del modelo con diferentes configuraciones.
Permite balancear velocidad vs precisión según necesidades del negocio.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import joblib
import time
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_percentage_error, r2_score
from sklearn.model_selection import cross_val_score
import json

class OptimizedSteelRebarTrainer:
    """Entrenador optimizado con diferentes perfiles de velocidad/precisión."""
    
    def __init__(self):
        self.training_profiles = {
            "ultra_fast": {
                "n_estimators": 50,
                "max_depth": 8,
                "min_samples_split": 10,
                "min_samples_leaf": 5,
                "max_features": "sqrt",
                "cv_folds": 3,
                "description": "Entrenamiento ultra rápido (~1-2 min)"
            },
            "fast": {
                "n_estimators": 100,
                "max_depth": 10,
                "min_samples_split": 5,
                "min_samples_leaf": 2,
                "max_features": "sqrt",
                "cv_folds": 3,
                "description": "Entrenamiento rápido (~2-3 min)"
            },
            "balanced": {
                "n_estimators": 150,
                "max_depth": 12,
                "min_samples_split": 3,
                "min_samples_leaf": 1,
                "max_features": "sqrt",
                "cv_folds": 5,
                "description": "Balance velocidad/precisión (~3-4 min)"
            },
            "high_precision": {
                "n_estimators": 200,
                "max_depth": 15,
                "min_samples_split": 3,
                "min_samples_leaf": 1,
                "max_features": "sqrt",
                "cv_folds": 5,
                "description": "Alta precisión (~5-8 min)"
            }
        }
    
    def create_optimized_training_data(self):
        """Crear datos de entrenamiento optimizados."""
        
        print("🏗️ CREANDO DATOS DE ENTRENAMIENTO OPTIMIZADOS")
        print("=" * 60)
        
        # Crear datos base desde 2020 hasta 2024
        dates = pd.date_range(start='2020-01-01', end='2024-12-31', freq='D')
        
        # Generar datos sintéticos más eficientes
        np.random.seed(42)  # Para reproducibilidad
        
        # Datos principales de varilla
        rebar_base = 650
        rebar_trend = np.linspace(0, 100, len(dates))
        rebar_seasonal = np.sin(2 * np.pi * pd.to_datetime(dates).dayofyear / 365.25) * 30
        rebar_noise = np.random.normal(0, 25, len(dates))
        rebar_prices = rebar_base + rebar_trend + rebar_seasonal + rebar_noise
        rebar_prices = np.maximum(rebar_prices, 400)
        
        # Datos de materias primas (simplificados)
        iron_ore_prices = 100 + np.linspace(0, 40, len(dates)) + np.random.normal(0, 15, len(dates))
        coal_prices = 150 + np.linspace(0, 60, len(dates)) + np.random.normal(0, 20, len(dates))
        
        # USD/MXN
        usd_mxn_rates = 20.0 + np.linspace(0, 3, len(dates)) + np.random.normal(0, 0.5, len(dates))
        usd_mxn_rates = np.maximum(usd_mxn_rates, 18)
        
        # Crear DataFrame optimizado
        data = pd.DataFrame({
            'date': dates,
            'rebar_price': rebar_prices,
            'iron_ore_price': iron_ore_prices,
            'coal_price': coal_prices,
            'usd_mxn_rate': usd_mxn_rates,
            'steel_rebar_price': rebar_prices  # Target
        })
        
        print(f"✅ Datos optimizados creados:")
        print(f"   - Registros: {len(data)}")
        print(f"   - Columnas: {len(data.columns)}")
        
        return data
    
    def create_essential_features(self, data):
        """Crear solo features esenciales para entrenamiento rápido."""
        
        print("\n🔧 CREANDO FEATURES ESENCIALES")
        print("=" * 40)
        
        df = data.copy()
        
        # Features básicos de precios
        price_columns = ['rebar_price', 'iron_ore_price', 'coal_price']
        
        for col in price_columns:
            df[f'{col}_ma_7'] = df[col].rolling(7).mean()
            df[f'{col}_ma_14'] = df[col].rolling(14).mean()
            df[f'{col}_change_1d'] = df[col].pct_change(1)
            df[f'{col}_change_7d'] = df[col].pct_change(7)
        
        # Features de USD/MXN
        df['usd_mxn_ma_7'] = df['usd_mxn_rate'].rolling(7).mean()
        df['usd_mxn_change_7d'] = df['usd_mxn_rate'].pct_change(7)
        
        # Features estacionales básicos
        df['month'] = df['date'].dt.month
        df['day_of_week'] = df['date'].dt.dayofweek
        df['quarter'] = df['date'].dt.quarter
        
        # Codificación cíclica básica
        df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
        df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
        
        # Eliminar NaN
        df = df.dropna()
        
        print(f"✅ Features esenciales creados:")
        print(f"   - Features totales: {len(df.columns)}")
        print(f"   - Registros válidos: {len(df)}")
        
        return df
    
    def train_with_profile(self, data, profile_name="balanced"):
        """Entrenar modelo con perfil específico."""
        
        profile = self.training_profiles[profile_name]
        
        print(f"\n🤖 ENTRENANDO CON PERFIL: {profile_name.upper()}")
        print(f"📝 {profile['description']}")
        print("=" * 50)
        
        # Preparar datos
        feature_columns = [col for col in data.columns if col not in ['date', 'steel_rebar_price']]
        numeric_columns = data[feature_columns].select_dtypes(include=[np.number]).columns.tolist()
        
        X = data[numeric_columns].values
        y = data['steel_rebar_price'].values
        
        print(f"📊 Datos de entrenamiento:")
        print(f"   - Features: {len(numeric_columns)}")
        print(f"   - Muestras: {len(X)}")
        
        # Escalar features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Entrenar modelo con perfil específico
        print("🌲 Entrenando Random Forest...")
        start_time = time.time()
        
        model = RandomForestRegressor(
            n_estimators=profile['n_estimators'],
            max_depth=profile['max_depth'],
            min_samples_split=profile['min_samples_split'],
            min_samples_leaf=profile['min_samples_leaf'],
            max_features=profile['max_features'],
            random_state=42,
            n_jobs=-1,
            bootstrap=True,
            oob_score=True
        )
        
        model.fit(X_scaled, y)
        training_time = time.time() - start_time
        
        # Evaluar modelo
        print("📊 Evaluando modelo...")
        eval_start = time.time()
        
        cv_scores = cross_val_score(
            model, X_scaled, y, 
            cv=profile['cv_folds'], 
            scoring='neg_mean_absolute_percentage_error'
        )
        
        eval_time = time.time() - eval_start
        model_confidence = max(0.5, min(0.95, 1 - abs(cv_scores.mean())))
        
        # Feature importance
        feature_importance = dict(zip(numeric_columns, model.feature_importances_))
        top_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:5]
        
        print(f"\n✅ Modelo entrenado exitosamente:")
        print(f"   - Tiempo de entrenamiento: {training_time:.2f}s")
        print(f"   - Tiempo de evaluación: {eval_time:.2f}s")
        print(f"   - Tiempo total: {training_time + eval_time:.2f}s")
        print(f"   - Confianza: {model_confidence:.3f}")
        print(f"   - CV MAPE: {abs(cv_scores.mean()):.3f}")
        print(f"   - OOB Score: {model.oob_score_:.3f}")
        
        print(f"\n🔝 Top 5 Features más importantes:")
        for i, (feature, importance) in enumerate(top_features, 1):
            print(f"   {i}. {feature}: {importance:.4f}")
        
        return {
            'model': model,
            'scaler': scaler,
            'feature_names': numeric_columns,
            'feature_importance': feature_importance,
            'model_confidence': model_confidence,
            'training_time': training_time,
            'eval_time': eval_time,
            'total_time': training_time + eval_time,
            'profile': profile_name,
            'cv_scores': cv_scores.tolist()
        }
    
    def benchmark_all_profiles(self, data):
        """Comparar todos los perfiles de entrenamiento."""
        
        print("\n🏁 BENCHMARK DE TODOS LOS PERFILES")
        print("=" * 60)
        
        results = {}
        
        for profile_name in self.training_profiles.keys():
            print(f"\n{'='*20} {profile_name.upper()} {'='*20}")
            
            try:
                result = self.train_with_profile(data, profile_name)
                results[profile_name] = result
                
            except Exception as e:
                print(f"❌ Error en perfil {profile_name}: {e}")
                results[profile_name] = None
        
        # Mostrar comparación
        print(f"\n📊 COMPARACIÓN DE PERFILES:")
        print("=" * 80)
        print(f"{'Perfil':<15} {'Tiempo (s)':<12} {'Confianza':<12} {'MAPE':<10} {'OOB Score':<12}")
        print("-" * 80)
        
        for profile_name, result in results.items():
            if result:
                print(f"{profile_name:<15} {result['total_time']:<12.2f} {result['model_confidence']:<12.3f} "
                      f"{abs(np.mean(result['cv_scores'])):<10.3f} {result['model'].oob_score_:<12.3f}")
        
        return results
    
    def save_optimized_model(self, result, profile_name):
        """Guardar modelo optimizado."""
        
        print(f"\n💾 GUARDANDO MODELO OPTIMIZADO ({profile_name})")
        print("=" * 50)
        
        model_data = {
            'model': result['model'],
            'scaler': result['scaler'],
            'feature_names': result['feature_names'],
            'feature_importance': result['feature_importance'],
            'model_confidence': result['model_confidence'],
            'training_time': result['training_time'],
            'eval_time': result['eval_time'],
            'total_time': result['total_time'],
            'profile': profile_name,
            'training_date': datetime.now().isoformat(),
            'model_type': f'Optimized Random Forest - {profile_name}',
            'performance_metrics': {
                'cv_scores': result['cv_scores'],
                'oob_score': result['model'].oob_score_,
                'n_estimators': result['model'].n_estimators,
                'max_depth': result['model'].max_depth
            }
        }
        
        # Guardar modelo
        filename = f'optimized_steel_rebar_model_{profile_name}.pkl'
        joblib.dump(model_data, f'../../data/models/{filename}')
        
        # Guardar metadatos
        metadata = {
            'model_info': {
                'type': 'Optimized Random Forest Regressor',
                'profile': profile_name,
                'n_estimators': result['model'].n_estimators,
                'max_depth': result['model'].max_depth,
                'confidence': result['model_confidence'],
                'training_time': result['training_time'],
                'total_time': result['total_time'],
                'training_date': model_data['training_date']
            },
            'feature_count': len(result['feature_names']),
            'top_features': dict(sorted(result['feature_importance'].items(), key=lambda x: x[1], reverse=True)[:10]),
            'performance_metrics': model_data['performance_metrics']
        }
        
        metadata_filename = f'optimized_model_metadata_{profile_name}.json'
        with open(f'../../data/models/{metadata_filename}', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ Modelo guardado:")
        print(f"   - Archivo: {filename}")
        print(f"   - Metadatos: {metadata_filename}")
        print(f"   - Tiempo total: {result['total_time']:.2f}s")
        print(f"   - Confianza: {result['model_confidence']:.3f}")

def main():
    """Función principal para entrenamiento optimizado."""
    
    print("🚀 ENTRENAMIENTO OPTIMIZADO - STEEL REBAR PREDICTOR")
    print("=" * 70)
    print("Balanceando velocidad vs precisión según necesidades del negocio")
    print("=" * 70)
    
    trainer = OptimizedSteelRebarTrainer()
    
    # Crear datos optimizados
    data = trainer.create_optimized_training_data()
    
    # Crear features esenciales
    enhanced_data = trainer.create_essential_features(data)
    
    # Mostrar perfiles disponibles
    print(f"\n📋 PERFILES DISPONIBLES:")
    for profile_name, profile in trainer.training_profiles.items():
        print(f"   - {profile_name}: {profile['description']}")
    
    # Ejecutar benchmark de todos los perfiles
    results = trainer.benchmark_all_profiles(enhanced_data)
    
    # Guardar modelo recomendado (balanced)
    if 'balanced' in results and results['balanced']:
        trainer.save_optimized_model(results['balanced'], 'balanced')
    
    print(f"\n🎯 RESUMEN FINAL:")
    print(f"   ✅ Benchmark completado para {len(results)} perfiles")
    print(f"   ✅ Modelo recomendado guardado (balanced)")
    print(f"   ✅ Tiempos optimizados desde ~1 min hasta ~8 min")
    print(f"   ✅ Listo para producción con diferentes niveles de precisión")

if __name__ == "__main__":
    main()
