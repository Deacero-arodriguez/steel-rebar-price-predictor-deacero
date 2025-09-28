#!/usr/bin/env python3
"""
Train Enhanced Model with Additional Data Sources - Fixed Version
Versión corregida que maneja mejor los datos faltantes.
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

def create_comprehensive_training_data_fixed():
    """Crear datos de entrenamiento comprehensivos con manejo mejorado de datos faltantes."""
    
    print("🏗️ CREANDO DATOS DE ENTRENAMIENTO COMPREHENSIVOS (VERSIÓN CORREGIDA)")
    print("=" * 70)
    
    # Crear datos base desde 2020 hasta 2024
    dates = pd.date_range(start='2020-01-01', end='2024-12-31', freq='D')
    
    print(f"📅 Creando datos para {len(dates)} días (2020-2024)")
    
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
    
    # 11. Datos adicionales simulados (para representar las nuevas fuentes)
    print("🆕 Generando datos adicionales simulados...")
    
    # Datos de Quandl (simulados)
    gold_prices = 1800 + np.random.normal(0, 100, len(dates))
    silver_prices = 25 + np.random.normal(0, 3, len(dates))
    
    # Datos de USGS (simulados)
    usgs_iron_ore_production = np.random.normal(1000, 100, len(dates))
    usgs_steel_production = np.random.normal(800, 80, len(dates))
    usgs_coal_production = np.random.normal(600, 60, len(dates))
    
    # Datos de Banxico (simulados)
    banxico_inflation = 4.0 + np.random.normal(0, 1, len(dates))
    banxico_gdp_growth = 2.5 + np.random.normal(0, 0.5, len(dates))
    
    # Datos de INEGI (simulados)
    inegi_construction_index = 100 + np.random.normal(0, 5, len(dates))
    inegi_industrial_production = 105 + np.random.normal(0, 3, len(dates))
    inegi_manufacturing_index = 102 + np.random.normal(0, 4, len(dates))
    inegi_employment_index = 98 + np.random.normal(0, 2, len(dates))
    
    # Crear DataFrame completo
    comprehensive_data = pd.DataFrame({
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
        
        # Fuentes adicionales
        'quandl_gold_prices': gold_prices,
        'quandl_silver_prices': silver_prices,
        'usgs_iron_ore_production': usgs_iron_ore_production,
        'usgs_steel_production': usgs_steel_production,
        'usgs_coal_production': usgs_coal_production,
        'banxico_inflation': banxico_inflation,
        'banxico_gdp_growth': banxico_gdp_growth,
        'inegi_construction_index': inegi_construction_index,
        'inegi_industrial_production': inegi_industrial_production,
        'inegi_manufacturing_index': inegi_manufacturing_index,
        'inegi_employment_index': inegi_employment_index,
    })
    
    print(f"✅ Datos comprehensivos creados:")
    print(f"   - Registros: {len(comprehensive_data)}")
    print(f"   - Columnas: {len(comprehensive_data.columns)}")
    print(f"   - Rango de fechas: {comprehensive_data['date'].min()} a {comprehensive_data['date'].max()}")
    
    return comprehensive_data

def create_advanced_features_fixed(data):
    """Crear features avanzados con manejo mejorado de datos faltantes."""
    
    print("\n🔧 CREANDO FEATURES AVANZADOS (VERSIÓN CORREGIDA)")
    print("=" * 60)
    
    enhanced_data = data.copy()
    feature_count = 0
    
    print("📈 Calculando features principales...")
    
    # 1. Features de tipos de cambio
    enhanced_data['usd_mxn_strength'] = enhanced_data['yahoo_usd_mxn_rate'] / enhanced_data['yahoo_usd_mxn_rate'].rolling(30, min_periods=1).mean()
    enhanced_data['usd_mxn_volatility_7d'] = enhanced_data['yahoo_usd_mxn_rate'].rolling(7, min_periods=1).std()
    enhanced_data['usd_mxn_volatility_30d'] = enhanced_data['yahoo_usd_mxn_rate'].rolling(30, min_periods=1).std()
    enhanced_data['usd_mxn_ma_7'] = enhanced_data['yahoo_usd_mxn_rate'].rolling(7, min_periods=1).mean()
    enhanced_data['usd_mxn_ma_30'] = enhanced_data['yahoo_usd_mxn_rate'].rolling(30, min_periods=1).mean()
    enhanced_data['usd_mxn_change_1d'] = enhanced_data['yahoo_usd_mxn_rate'].pct_change(1)
    enhanced_data['usd_mxn_change_7d'] = enhanced_data['yahoo_usd_mxn_rate'].pct_change(7)
    feature_count += 7
    
    # 2. Features de commodities
    enhanced_data['iron_ore_volatility_7d'] = enhanced_data['alpha_vantage_iron_ore_price'].rolling(7, min_periods=1).std()
    enhanced_data['iron_ore_ma_7'] = enhanced_data['alpha_vantage_iron_ore_price'].rolling(7, min_periods=1).mean()
    enhanced_data['iron_ore_ma_30'] = enhanced_data['alpha_vantage_iron_ore_price'].rolling(30, min_periods=1).mean()
    enhanced_data['iron_ore_change_1d'] = enhanced_data['alpha_vantage_iron_ore_price'].pct_change(1)
    enhanced_data['iron_ore_change_7d'] = enhanced_data['alpha_vantage_iron_ore_price'].pct_change(7)
    feature_count += 5
    
    # 3. Features de tasas de interés
    enhanced_data['interest_rate_change_1d'] = enhanced_data['fred_us_interest_rate'].diff(1)
    enhanced_data['interest_rate_volatility_7d'] = enhanced_data['fred_us_interest_rate'].rolling(7, min_periods=1).std()
    feature_count += 2
    
    # 4. Features de acero
    enhanced_data['rebar_price_correlation'] = enhanced_data['indexmundi_rebar_price'].rolling(30, min_periods=1).corr(enhanced_data['alpha_vantage_iron_ore_price'])
    enhanced_data['rebar_price_spread'] = enhanced_data['daily_metal_rebar_price'] - enhanced_data['barchart_rebar_futures']
    enhanced_data['rebar_price_volatility_7d'] = enhanced_data['indexmundi_rebar_price'].rolling(7, min_periods=1).std()
    enhanced_data['rebar_price_ma_7'] = enhanced_data['indexmundi_rebar_price'].rolling(7, min_periods=1).mean()
    enhanced_data['rebar_price_ma_30'] = enhanced_data['indexmundi_rebar_price'].rolling(30, min_periods=1).mean()
    feature_count += 5
    
    # 5. Features estacionales
    enhanced_data['day_of_year'] = enhanced_data['date'].dt.dayofyear
    enhanced_data['month'] = enhanced_data['date'].dt.month
    enhanced_data['quarter'] = enhanced_data['date'].dt.quarter
    enhanced_data['is_weekend'] = enhanced_data['date'].dt.weekday >= 5
    enhanced_data['construction_season'] = enhanced_data['month'].isin([3, 4, 5, 6, 7, 8, 9, 10])
    feature_count += 5
    
    # 6. Features geopolíticos
    enhanced_data['geopolitical_risk_ma_7'] = enhanced_data['geopolitical_risk_index'].rolling(7, min_periods=1).mean()
    enhanced_data['trade_tension_ma_7'] = enhanced_data['trade_tension_index'].rolling(7, min_periods=1).mean()
    enhanced_data['supply_chain_events_30d'] = enhanced_data['supply_chain_disruption'].rolling(30, min_periods=1).sum()
    feature_count += 3
    
    # 7. Features de commodities avanzados
    enhanced_data['commodity_index_volatility_7d'] = enhanced_data['sp_goldman_sachs_commodity_index'].rolling(7, min_periods=1).std()
    enhanced_data['commodity_index_ma_7'] = enhanced_data['sp_goldman_sachs_commodity_index'].rolling(7, min_periods=1).mean()
    enhanced_data['commodity_index_change_1d'] = enhanced_data['sp_goldman_sachs_commodity_index'].pct_change(1)
    feature_count += 3
    
    # 8. Features adicionales
    print("🆕 Calculando features de fuentes adicionales...")
    
    # Features de Quandl
    enhanced_data['gold_volatility_7d'] = enhanced_data['quandl_gold_prices'].rolling(7, min_periods=1).std()
    enhanced_data['gold_ma_7'] = enhanced_data['quandl_gold_prices'].rolling(7, min_periods=1).mean()
    enhanced_data['gold_change_1d'] = enhanced_data['quandl_gold_prices'].pct_change(1)
    enhanced_data['silver_volatility_7d'] = enhanced_data['quandl_silver_prices'].rolling(7, min_periods=1).std()
    enhanced_data['silver_ma_7'] = enhanced_data['quandl_silver_prices'].rolling(7, min_periods=1).mean()
    enhanced_data['silver_change_1d'] = enhanced_data['quandl_silver_prices'].pct_change(1)
    feature_count += 6
    
    # Features de USGS
    enhanced_data['iron_ore_production_impact'] = enhanced_data['usgs_iron_ore_production'] / enhanced_data['usgs_iron_ore_production'].rolling(30, min_periods=1).mean()
    enhanced_data['steel_production_impact'] = enhanced_data['usgs_steel_production'] / enhanced_data['usgs_steel_production'].rolling(30, min_periods=1).mean()
    enhanced_data['coal_production_impact'] = enhanced_data['usgs_coal_production'] / enhanced_data['usgs_coal_production'].rolling(30, min_periods=1).mean()
    feature_count += 3
    
    # Features de Banxico
    enhanced_data['inflation_volatility_7d'] = enhanced_data['banxico_inflation'].rolling(7, min_periods=1).std()
    enhanced_data['inflation_ma_7'] = enhanced_data['banxico_inflation'].rolling(7, min_periods=1).mean()
    enhanced_data['inflation_change_1d'] = enhanced_data['banxico_inflation'].pct_change(1)
    enhanced_data['gdp_growth_volatility_7d'] = enhanced_data['banxico_gdp_growth'].rolling(7, min_periods=1).std()
    enhanced_data['gdp_growth_ma_7'] = enhanced_data['banxico_gdp_growth'].rolling(7, min_periods=1).mean()
    enhanced_data['gdp_growth_change_1d'] = enhanced_data['banxico_gdp_growth'].pct_change(1)
    feature_count += 6
    
    # Features de INEGI
    enhanced_data['construction_trend'] = enhanced_data['inegi_construction_index'].rolling(7, min_periods=1).mean() / enhanced_data['inegi_construction_index'].rolling(30, min_periods=1).mean()
    enhanced_data['industrial_trend'] = enhanced_data['inegi_industrial_production'].rolling(7, min_periods=1).mean() / enhanced_data['inegi_industrial_production'].rolling(30, min_periods=1).mean()
    enhanced_data['manufacturing_trend'] = enhanced_data['inegi_manufacturing_index'].rolling(7, min_periods=1).mean() / enhanced_data['inegi_manufacturing_index'].rolling(30, min_periods=1).mean()
    enhanced_data['employment_trend'] = enhanced_data['inegi_employment_index'].rolling(7, min_periods=1).mean() / enhanced_data['inegi_employment_index'].rolling(30, min_periods=1).mean()
    feature_count += 4
    
    # 9. Features de correlación y ratios
    enhanced_data['gold_silver_ratio'] = enhanced_data['quandl_gold_prices'] / enhanced_data['quandl_silver_prices']
    enhanced_data['rebar_iron_ore_ratio'] = enhanced_data['indexmundi_rebar_price'] / enhanced_data['alpha_vantage_iron_ore_price']
    enhanced_data['coal_iron_ore_ratio'] = enhanced_data['focus_coking_coal_price'] / enhanced_data['alpha_vantage_iron_ore_price']
    feature_count += 3
    
    # 10. Features de volatilidad relativa
    enhanced_data['rebar_volatility_vs_iron_ore'] = enhanced_data['rebar_price_volatility_7d'] / enhanced_data['iron_ore_volatility_7d']
    enhanced_data['usd_mxn_volatility_vs_commodities'] = enhanced_data['usd_mxn_volatility_7d'] / enhanced_data['commodity_index_volatility_7d']
    feature_count += 2
    
    print(f"✅ Features avanzados creados:")
    print(f"   - Total de features: {feature_count}")
    print(f"   - Total de columnas: {len(enhanced_data.columns)}")
    
    # Manejar valores infinitos y NaN
    print("🧹 Limpiando datos...")
    
    # Reemplazar infinitos con NaN
    enhanced_data = enhanced_data.replace([np.inf, -np.inf], np.nan)
    
    # Llenar NaN con valores forward fill y backward fill
    enhanced_data = enhanced_data.fillna(method='ffill').fillna(method='bfill')
    
    # Si aún hay NaN, llenar con la media de la columna
    for col in enhanced_data.select_dtypes(include=[np.number]).columns:
        if enhanced_data[col].isna().any():
            enhanced_data[col] = enhanced_data[col].fillna(enhanced_data[col].mean())
    
    print(f"✅ Datos limpiados:")
    print(f"   - Registros: {len(enhanced_data)}")
    print(f"   - Columnas: {len(enhanced_data.columns)}")
    print(f"   - Valores NaN restantes: {enhanced_data.isna().sum().sum()}")
    
    return enhanced_data

def train_enhanced_model_fixed(data):
    """Entrenar modelo mejorado con manejo robusto de datos."""
    
    print("\n🤖 ENTRENANDO MODELO MEJORADO (VERSIÓN CORREGIDA)")
    print("=" * 60)
    
    # Preparar datos para entrenamiento
    feature_columns = [col for col in data.columns if col not in ['date', 'steel_rebar_price']]
    
    # Crear target variable (promedio de precios de acero)
    steel_price_columns = ['indexmundi_rebar_price', 'daily_metal_rebar_price', 'barchart_rebar_futures']
    data['steel_rebar_price'] = data[steel_price_columns].mean(axis=1)
    
    # Verificar que no hay NaN en el target
    if data['steel_rebar_price'].isna().any():
        print("⚠️ Detectados valores NaN en target variable, llenando...")
        data['steel_rebar_price'] = data['steel_rebar_price'].fillna(data['steel_rebar_price'].mean())
    
    # Filtrar datos válidos
    training_data = data.dropna(subset=feature_columns + ['steel_rebar_price'])
    
    print(f"📊 Datos de entrenamiento:")
    print(f"   - Registros: {len(training_data)}")
    print(f"   - Features: {len(feature_columns)}")
    print(f"   - Rango de precios: ${training_data['steel_rebar_price'].min():.2f} - ${training_data['steel_rebar_price'].max():.2f}")
    
    if len(training_data) == 0:
        print("❌ No hay datos válidos para entrenamiento")
        return None, None, None
    
    # Dividir datos
    X = training_data[feature_columns]
    y = training_data['steel_rebar_price']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(f"📊 División de datos:")
    print(f"   - Entrenamiento: {len(X_train)} registros")
    print(f"   - Prueba: {len(X_test)} registros")
    
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
    
    print(f"\n🏆 Top 15 features más importantes:")
    for i, (_, row) in enumerate(feature_importance.head(15).iterrows()):
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

def save_enhanced_model_fixed(model, feature_importance, metrics, data):
    """Guardar modelo mejorado y metadatos."""
    
    print("\n💾 GUARDANDO MODELO MEJORADO")
    print("=" * 40)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Guardar modelo
    model_filename = f"data/models/enhanced_steel_rebar_model_fixed_{timestamp}.pkl"
    os.makedirs(os.path.dirname(model_filename), exist_ok=True)
    joblib.dump(model, model_filename)
    
    # Guardar feature importance
    importance_filename = f"data/models/enhanced_feature_importance_fixed_{timestamp}.csv"
    feature_importance.to_csv(importance_filename, index=False)
    
    # Guardar metadatos
    metadata = {
        'model_type': 'Enhanced Random Forest Regressor (Fixed)',
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
    
    metadata_filename = f"data/models/enhanced_model_metadata_fixed_{timestamp}.json"
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
    
    print("🚀 ENTRENAMIENTO DE MODELO MEJORADO CON FUENTES ADICIONALES (VERSIÓN CORREGIDA)")
    print("=" * 80)
    
    # Crear datos comprehensivos
    comprehensive_data = create_comprehensive_training_data_fixed()
    
    # Crear features avanzados
    enhanced_data = create_advanced_features_fixed(comprehensive_data)
    
    # Entrenar modelo
    model, feature_importance, metrics = train_enhanced_model_fixed(enhanced_data)
    
    if model is not None:
        # Guardar modelo
        model_filename, metadata_filename = save_enhanced_model_fixed(model, feature_importance, metrics, enhanced_data)
        
        print(f"\n🎉 ENTRENAMIENTO COMPLETADO")
        print(f"✅ Modelo mejorado entrenado exitosamente")
        print(f"📊 Confianza: {metrics['model_confidence']:.1f}%")
        print(f"📈 MAPE: {metrics['test_mape']:.2f}%")
        print(f"🔧 Features: {metrics['features_count']}")
        print(f"📊 Muestras de entrenamiento: {metrics['training_samples']}")
        
        return model, feature_importance, metrics
    else:
        print("❌ Error en el entrenamiento del modelo")
        return None, None, None

if __name__ == "__main__":
    main()
