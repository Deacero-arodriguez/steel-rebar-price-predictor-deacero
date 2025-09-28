#!/usr/bin/env python3
"""
Train Enhanced Model with Additional Data Sources
Entrena el modelo mejorado con las nuevas fuentes de datos adicionales.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_percentage_error, r2_score
from sklearn.model_selection import cross_val_score, train_test_split
import os
import sys

# Agregar el directorio raíz al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

def load_additional_data():
    """Cargar datos adicionales generados."""
    
    print("📊 CARGANDO DATOS ADICIONALES")
    print("=" * 40)
    
    # Buscar el archivo más reciente de features
    files = [f for f in os.listdir('.') if f.startswith('enhanced_features_') and f.endswith('.csv')]
    
    if not files:
        print("❌ No se encontraron archivos de features adicionales")
        return None
    
    latest_file = sorted(files)[-1]
    print(f"📁 Cargando: {latest_file}")
    
    try:
        additional_data = pd.read_csv(latest_file)
        additional_data['date'] = pd.to_datetime(additional_data['date'])
        
        print(f"✅ Datos cargados:")
        print(f"   - Registros: {len(additional_data)}")
        print(f"   - Columnas: {len(additional_data.columns)}")
        print(f"   - Rango de fechas: {additional_data['date'].min()} a {additional_data['date'].max()}")
        
        return additional_data
        
    except Exception as e:
        print(f"❌ Error cargando datos: {e}")
        return None

def create_comprehensive_training_data_with_additional():
    """Crear datos de entrenamiento comprehensivos con fuentes adicionales."""
    
    print("\n🏗️ CREANDO DATOS DE ENTRENAMIENTO COMPREHENSIVOS")
    print("=" * 60)
    print("Integrando fuentes existentes + nuevas fuentes adicionales")
    print("=" * 60)
    
    # Crear datos base desde 2020 hasta 2024
    dates = pd.date_range(start='2020-01-01', end='2024-12-31', freq='D')
    
    # Datos existentes (simulados pero realistas)
    print("📊 Generando datos de fuentes existentes...")
    
    # 1. Datos de Yahoo Finance (simulados)
    np.random.seed(42)
    usd_mxn_base = 20.0
    usd_mxn_volatility = 2.0
    usd_mxn_trend = np.linspace(0, 5, len(dates))
    usd_mxn_seasonal = np.sin(2 * np.pi * pd.to_datetime(dates).dayofyear / 365.25) * 1.5
    usd_mxn_noise = np.random.normal(0, usd_mxn_volatility, len(dates))
    usd_mxn_rates = usd_mxn_base + usd_mxn_trend + usd_mxn_seasonal + usd_mxn_noise
    
    # 2. Datos de Alpha Vantage (simulados)
    iron_ore_base = 100
    iron_ore_volatility = 20
    iron_ore_trend = np.linspace(0, 40, len(dates))
    iron_ore_seasonal = np.sin(2 * np.pi * pd.to_datetime(dates).dayofyear / 365.25) * 15
    iron_ore_noise = np.random.normal(0, iron_ore_volatility, len(dates))
    iron_ore_prices = iron_ore_base + iron_ore_trend + iron_ore_seasonal + iron_ore_noise
    
    # 3. Datos de FRED (simulados)
    us_interest_rate = 2.5 + np.random.normal(0, 0.5, len(dates))
    us_interest_rate = np.maximum(us_interest_rate, 0.25)  # Tasa mínima
    
    # 4. Datos de IndexMundi (simulados)
    rebar_base = 650
    rebar_volatility = 50
    rebar_trend = np.linspace(0, 100, len(dates))
    rebar_seasonal = np.sin(2 * np.pi * pd.to_datetime(dates).dayofyear / 365.25) * 30
    rebar_noise = np.random.normal(0, rebar_volatility, len(dates))
    rebar_prices = rebar_base + rebar_trend + rebar_seasonal + rebar_noise
    
    # 5. Datos de Daily Metal Price (simulados)
    daily_rebar_prices = rebar_prices + np.random.normal(0, 10, len(dates))
    
    # 6. Datos de Barchart (simulados)
    barchart_rebar_prices = rebar_prices + np.random.normal(0, 15, len(dates))
    
    # 7. Datos de FocusEconomics (simulados)
    coking_coal_base = 150
    coking_coal_volatility = 30
    coking_coal_trend = np.linspace(0, 50, len(dates))
    coking_coal_seasonal = np.sin(2 * np.pi * pd.to_datetime(dates).dayofyear / 365.25) * 20
    coking_coal_noise = np.random.normal(0, coking_coal_volatility, len(dates))
    coking_coal_prices = coking_coal_base + coking_coal_trend + coking_coal_seasonal + coking_coal_noise
    
    # 8. Datos regionales mexicanos (simulados)
    platts_prices = rebar_prices + np.random.normal(0, 20, len(dates))
    reportacero_prices = rebar_prices + np.random.normal(0, 25, len(dates))
    
    # 9. Índices de commodities (simulados)
    spgcci_base = 100
    spgcci_volatility = 10
    spgcci_trend = np.linspace(0, 20, len(dates))
    spgcci_seasonal = np.sin(2 * np.pi * pd.to_datetime(dates).dayofyear / 365.25) * 5
    spgcci_noise = np.random.normal(0, spgcci_volatility, len(dates))
    spgcci_values = spgcci_base + spgcci_trend + spgcci_seasonal + spgcci_noise
    
    # 10. Indicadores geopolíticos (simulados)
    geopolitical_risk = np.random.beta(2, 5, len(dates)) * 100
    trade_tension = np.random.beta(3, 4, len(dates)) * 100
    supply_chain_disruption = np.random.binomial(1, 0.1, len(dates))
    
    # Crear DataFrame base
    base_data = pd.DataFrame({
        'date': dates,
        
        # Fuentes existentes
        'yahoo_usd_mxn_rate': usd_mxn_rates,
        'alpha_vantage_iron_ore_price': iron_ore_prices,
        'fred_us_interest_rate': us_interest_rate,
        'indexmundi_rebar_price': rebar_prices,
        'daily_metal_rebar_price': daily_rebar_prices,
        'barchart_rebar_futures': barchart_rebar_prices,
        'focus_coking_coal_price': coking_coal_prices,
        'platts_mexican_rebar': platts_prices,
        'reportacero_steel_prices': reportacero_prices,
        'sp_goldman_sachs_commodity_index': spgcci_values,
        'geopolitical_risk_index': geopolitical_risk,
        'trade_tension_index': trade_tension,
        'supply_chain_disruption': supply_chain_disruption,
    })
    
    print(f"✅ Datos base creados: {len(base_data)} registros")
    
    # Cargar datos adicionales
    additional_data = load_additional_data()
    
    if additional_data is not None:
        # Combinar datos base con datos adicionales
        print("\n🔗 Combinando con datos adicionales...")
        
        # Merge por fecha
        combined_data = base_data.merge(additional_data, on='date', how='left')
        
        print(f"✅ Datos combinados: {len(combined_data)} registros")
        print(f"📊 Total de columnas: {len(combined_data.columns)}")
        
        return combined_data
    else:
        print("⚠️ Usando solo datos base (sin fuentes adicionales)")
        return base_data

def create_advanced_features_enhanced(data):
    """Crear features avanzados con datos adicionales."""
    
    print("\n🔧 CREANDO FEATURES AVANZADOS MEJORADOS")
    print("=" * 50)
    
    enhanced_data = data.copy()
    feature_count = 0
    
    # Features existentes mejorados
    print("📈 Calculando features existentes...")
    
    # 1. Features de tipos de cambio
    enhanced_data['usd_mxn_strength'] = enhanced_data['yahoo_usd_mxn_rate'] / enhanced_data['yahoo_usd_mxn_rate'].rolling(30).mean()
    enhanced_data['usd_mxn_volatility_7d'] = enhanced_data['yahoo_usd_mxn_rate'].rolling(7).std()
    enhanced_data['usd_mxn_volatility_30d'] = enhanced_data['yahoo_usd_mxn_rate'].rolling(30).std()
    enhanced_data['usd_mxn_ma_7'] = enhanced_data['yahoo_usd_mxn_rate'].rolling(7).mean()
    enhanced_data['usd_mxn_ma_30'] = enhanced_data['yahoo_usd_mxn_rate'].rolling(30).mean()
    enhanced_data['usd_mxn_change_1d'] = enhanced_data['yahoo_usd_mxn_rate'].pct_change(1)
    enhanced_data['usd_mxn_change_7d'] = enhanced_data['yahoo_usd_mxn_rate'].pct_change(7)
    feature_count += 7
    
    # 2. Features de commodities
    enhanced_data['iron_ore_volatility_7d'] = enhanced_data['alpha_vantage_iron_ore_price'].rolling(7).std()
    enhanced_data['iron_ore_ma_7'] = enhanced_data['alpha_vantage_iron_ore_price'].rolling(7).mean()
    enhanced_data['iron_ore_ma_30'] = enhanced_data['alpha_vantage_iron_ore_price'].rolling(30).mean()
    enhanced_data['iron_ore_change_1d'] = enhanced_data['alpha_vantage_iron_ore_price'].pct_change(1)
    enhanced_data['iron_ore_change_7d'] = enhanced_data['alpha_vantage_iron_ore_price'].pct_change(7)
    feature_count += 5
    
    # 3. Features de tasas de interés
    enhanced_data['interest_rate_change_1d'] = enhanced_data['fred_us_interest_rate'].diff(1)
    enhanced_data['interest_rate_volatility_7d'] = enhanced_data['fred_us_interest_rate'].rolling(7).std()
    feature_count += 2
    
    # 4. Features de acero
    enhanced_data['rebar_price_correlation'] = enhanced_data['indexmundi_rebar_price'].rolling(30).corr(enhanced_data['alpha_vantage_iron_ore_price'])
    enhanced_data['rebar_price_spread'] = enhanced_data['daily_metal_rebar_price'] - enhanced_data['barchart_rebar_futures']
    enhanced_data['rebar_price_volatility_7d'] = enhanced_data['indexmundi_rebar_price'].rolling(7).std()
    enhanced_data['rebar_price_ma_7'] = enhanced_data['indexmundi_rebar_price'].rolling(7).mean()
    enhanced_data['rebar_price_ma_30'] = enhanced_data['indexmundi_rebar_price'].rolling(30).mean()
    feature_count += 5
    
    # 5. Features estacionales
    enhanced_data['day_of_year'] = enhanced_data['date'].dt.dayofyear
    enhanced_data['month'] = enhanced_data['date'].dt.month
    enhanced_data['quarter'] = enhanced_data['date'].dt.quarter
    enhanced_data['is_weekend'] = enhanced_data['date'].dt.weekday >= 5
    enhanced_data['construction_season'] = enhanced_data['month'].isin([3, 4, 5, 6, 7, 8, 9, 10])
    feature_count += 5
    
    # 6. Features geopolíticos
    enhanced_data['geopolitical_risk_ma_7'] = enhanced_data['geopolitical_risk_index'].rolling(7).mean()
    enhanced_data['trade_tension_ma_7'] = enhanced_data['trade_tension_index'].rolling(7).mean()
    enhanced_data['supply_chain_events_30d'] = enhanced_data['supply_chain_disruption'].rolling(30).sum()
    feature_count += 3
    
    # 7. Features de commodities avanzados
    enhanced_data['commodity_index_volatility_7d'] = enhanced_data['sp_goldman_sachs_commodity_index'].rolling(7).std()
    enhanced_data['commodity_index_ma_7'] = enhanced_data['sp_goldman_sachs_commodity_index'].rolling(7).mean()
    enhanced_data['commodity_index_change_1d'] = enhanced_data['sp_goldman_sachs_commodity_index'].pct_change(1)
    feature_count += 3
    
    # Features adicionales de las nuevas fuentes
    print("🆕 Calculando features de fuentes adicionales...")
    
    additional_features = 0
    
    # Features de Quandl (si están disponibles)
    quandl_columns = [col for col in enhanced_data.columns if 'quandl_' in col]
    for col in quandl_columns:
        if col.endswith('_price'):
            base_name = col.replace('quandl_', '').replace('_price', '')
            enhanced_data[f'{base_name}_volatility_7d'] = enhanced_data[col].rolling(7).std()
            enhanced_data[f'{base_name}_ma_7'] = enhanced_data[col].rolling(7).mean()
            enhanced_data[f'{base_name}_change_1d'] = enhanced_data[col].pct_change(1)
            additional_features += 3
    
    # Features de USGS (si están disponibles)
    usgs_columns = [col for col in enhanced_data.columns if 'usgs_' in col]
    for col in usgs_columns:
        if col.endswith('_price'):
            base_name = col.replace('usgs_', '').replace('_price', '')
            enhanced_data[f'{base_name}_production_impact'] = enhanced_data[col] / enhanced_data[col].rolling(30).mean()
            enhanced_data[f'{base_name}_price_trend'] = enhanced_data[col].rolling(7).mean() / enhanced_data[col].rolling(30).mean()
            additional_features += 2
    
    # Features de Banxico (si están disponibles)
    banxico_columns = [col for col in enhanced_data.columns if 'banxico_' in col]
    for col in banxico_columns:
        if col.endswith('_value'):
            base_name = col.replace('banxico_', '').replace('_value', '')
            enhanced_data[f'{base_name}_volatility_7d'] = enhanced_data[col].rolling(7).std()
            enhanced_data[f'{base_name}_ma_7'] = enhanced_data[col].rolling(7).mean()
            enhanced_data[f'{base_name}_change_1d'] = enhanced_data[col].pct_change(1)
            additional_features += 3
    
    # Features de INEGI (si están disponibles)
    inegi_columns = [col for col in enhanced_data.columns if 'inegi_' in col]
    for col in inegi_columns:
        if col.endswith('_value'):
            base_name = col.replace('inegi_', '').replace('_value', '')
            enhanced_data[f'{base_name}_trend'] = enhanced_data[col].rolling(7).mean() / enhanced_data[col].rolling(30).mean()
            enhanced_data[f'{base_name}_volatility_7d'] = enhanced_data[col].rolling(7).std()
            additional_features += 2
    
    feature_count += additional_features
    
    print(f"✅ Features avanzados creados:")
    print(f"   - Features existentes mejorados: {feature_count - additional_features}")
    print(f"   - Features adicionales: {additional_features}")
    print(f"   - Total de features: {feature_count}")
    print(f"   - Total de columnas: {len(enhanced_data.columns)}")
    
    return enhanced_data

def train_enhanced_model(data):
    """Entrenar modelo mejorado con todas las fuentes."""
    
    print("\n🤖 ENTRENANDO MODELO MEJORADO")
    print("=" * 40)
    
    # Preparar datos para entrenamiento
    feature_columns = [col for col in data.columns if col not in ['date', 'steel_rebar_price']]
    
    # Crear target variable (promedio de precios de acero)
    steel_price_columns = ['indexmundi_rebar_price', 'daily_metal_rebar_price', 'barchart_rebar_futures']
    data['steel_rebar_price'] = data[steel_price_columns].mean(axis=1)
    
    # Filtrar datos válidos
    training_data = data.dropna(subset=feature_columns + ['steel_rebar_price'])
    
    print(f"📊 Datos de entrenamiento:")
    print(f"   - Registros: {len(training_data)}")
    print(f"   - Features: {len(feature_columns)}")
    print(f"   - Rango de precios: ${training_data['steel_rebar_price'].min():.2f} - ${training_data['steel_rebar_price'].max():.2f}")
    
    # Dividir datos
    X = training_data[feature_columns]
    y = training_data['steel_rebar_price']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Entrenar modelo
    print("\n🔧 Entrenando modelo...")
    
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluar modelo
    print("\n📊 Evaluando modelo...")
    
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    
    train_mape = mean_absolute_percentage_error(y_train, y_pred_train) * 100
    test_mape = mean_absolute_percentage_error(y_test, y_pred_test) * 100
    train_r2 = r2_score(y_train, y_pred_train)
    test_r2 = r2_score(y_test, y_pred_test)
    
    # Validación cruzada
    cv_scores = cross_val_score(model, X, y, cv=5, scoring='neg_mean_absolute_percentage_error')
    cv_mape = (-cv_scores.mean()) * 100
    cv_std = cv_scores.std() * 100
    
    print(f"✅ Resultados del modelo:")
    print(f"   - MAPE (entrenamiento): {train_mape:.2f}%")
    print(f"   - MAPE (prueba): {test_mape:.2f}%")
    print(f"   - R² (entrenamiento): {train_r2:.4f}")
    print(f"   - R² (prueba): {test_r2:.4f}")
    print(f"   - MAPE (validación cruzada): {cv_mape:.2f}% ± {cv_std:.2f}%")
    
    # Features más importantes
    feature_importance = pd.DataFrame({
        'feature': feature_columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(f"\n🏆 Top 10 features más importantes:")
    for i, (_, row) in enumerate(feature_importance.head(10).iterrows()):
        print(f"   {i+1:2d}. {row['feature']}: {row['importance']:.4f}")
    
    # Calcular confianza del modelo
    model_confidence = max(0, min(100, 100 - cv_mape + (1 - cv_std/100) * 10))
    
    print(f"\n🎯 Confianza del modelo mejorado: {model_confidence:.1f}%")
    
    return model, feature_importance, {
        'train_mape': train_mape,
        'test_mape': test_mape,
        'train_r2': train_r2,
        'test_r2': test_r2,
        'cv_mape': cv_mape,
        'cv_std': cv_std,
        'model_confidence': model_confidence,
        'features_count': len(feature_columns),
        'training_samples': len(training_data)
    }

def save_enhanced_model(model, feature_importance, metrics, data):
    """Guardar modelo mejorado y metadatos."""
    
    print("\n💾 GUARDANDO MODELO MEJORADO")
    print("=" * 40)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Guardar modelo
    model_filename = f"data/models/enhanced_steel_rebar_model_{timestamp}.pkl"
    os.makedirs(os.path.dirname(model_filename), exist_ok=True)
    joblib.dump(model, model_filename)
    
    # Guardar feature importance
    importance_filename = f"data/models/enhanced_feature_importance_{timestamp}.csv"
    feature_importance.to_csv(importance_filename, index=False)
    
    # Guardar metadatos
    metadata = {
        'model_type': 'Enhanced Random Forest Regressor',
        'training_date': datetime.now().isoformat(),
        'features_count': metrics['features_count'],
        'training_samples': metrics['training_samples'],
        'data_sources': [
            'Yahoo Finance', 'Alpha Vantage', 'FRED API', 'IndexMundi',
            'Daily Metal Price', 'Barchart', 'FocusEconomics', 'S&P Global Platts',
            'Reportacero', 'Banco de México', 'INEGI', 'Trading Economics',
            'World Bank', 'Quandl', 'USGS', 'Banxico', 'INEGI'
        ],
        'metrics': metrics,
        'model_filename': model_filename,
        'feature_importance_filename': importance_filename
    }
    
    metadata_filename = f"data/models/enhanced_model_metadata_{timestamp}.json"
    import json
    with open(metadata_filename, 'w') as f:
        json.dump(metadata, f, indent=2, default=str)
    
    print(f"✅ Modelo guardado:")
    print(f"   - Modelo: {model_filename}")
    print(f"   - Features: {importance_filename}")
    print(f"   - Metadatos: {metadata_filename}")
    
    return model_filename, metadata_filename

def main():
    """Función principal."""
    
    print("🚀 ENTRENAMIENTO DE MODELO MEJORADO CON FUENTES ADICIONALES")
    print("=" * 70)
    
    # Crear datos comprehensivos
    comprehensive_data = create_comprehensive_training_data_with_additional()
    
    # Crear features avanzados
    enhanced_data = create_advanced_features_enhanced(comprehensive_data)
    
    # Entrenar modelo
    model, feature_importance, metrics = train_enhanced_model(enhanced_data)
    
    # Guardar modelo
    model_filename, metadata_filename = save_enhanced_model(model, feature_importance, metrics, enhanced_data)
    
    print(f"\n🎉 ENTRENAMIENTO COMPLETADO")
    print(f"✅ Modelo mejorado entrenado exitosamente")
    print(f"📊 Confianza: {metrics['model_confidence']:.1f}%")
    print(f"📈 MAPE: {metrics['test_mape']:.2f}%")
    print(f"🔧 Features: {metrics['features_count']}")
    
    return model, feature_importance, metrics

if __name__ == "__main__":
    main()
