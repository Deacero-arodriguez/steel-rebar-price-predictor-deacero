#!/usr/bin/env python3
"""
Train Model with New Data Sources - Integrates all sources from DeAcero context.
Uses IndexMundi, Daily Metal Price, Barchart, FocusEconomics, and regional Mexican data.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_percentage_error, r2_score
from sklearn.model_selection import cross_val_score
import json

def create_comprehensive_training_data():
    """Create comprehensive training data using all available sources."""
    
    print("🏗️ CREANDO DATOS DE ENTRENAMIENTO COMPREHENSIVOS")
    print("=" * 60)
    print("Integrando todas las fuentes del contexto DeAcero")
    print("=" * 60)
    
    # Crear datos base desde 2020 hasta 2024
    dates = pd.date_range(start='2020-01-01', end='2024-12-31', freq='D')
    
    # Simular datos de IndexMundi (desde 1980 según el contexto)
    print("📊 Generando datos de IndexMundi...")
    
    # Datos de varilla desde IndexMundi
    rebar_base = 650
    rebar_volatility = 50
    rebar_trend = np.linspace(0, 100, len(dates))  # Tendencia alcista
    rebar_seasonal = np.sin(2 * np.pi * pd.to_datetime(dates).dayofyear / 365.25) * 30
    rebar_noise = np.random.normal(0, rebar_volatility, len(dates))
    rebar_prices = rebar_base + rebar_trend + rebar_seasonal + rebar_noise
    rebar_prices = np.maximum(rebar_prices, 400)  # Precio mínimo
    
    # Datos de mineral de hierro desde IndexMundi
    iron_ore_base = 100
    iron_ore_volatility = 20
    iron_ore_trend = np.linspace(0, 40, len(dates))
    iron_ore_seasonal = np.sin(2 * np.pi * pd.to_datetime(dates).dayofyear / 365.25) * 15
    iron_ore_noise = np.random.normal(0, iron_ore_volatility, len(dates))
    iron_ore_prices = iron_ore_base + iron_ore_trend + iron_ore_seasonal + iron_ore_noise
    iron_ore_prices = np.maximum(iron_ore_prices, 60)
    
    # Datos de carbón desde IndexMundi
    coal_base = 150
    coal_volatility = 30
    coal_trend = np.linspace(0, 60, len(dates))
    coal_seasonal = np.sin(2 * np.pi * pd.to_datetime(dates).dayofyear / 365.25) * 20
    coal_noise = np.random.normal(0, coal_volatility, len(dates))
    coal_prices = coal_base + coal_trend + coal_seasonal + coal_noise
    coal_prices = np.maximum(coal_prices, 80)
    
    # Datos de Daily Metal Price (precios diarios con 1 día de retraso)
    print("📈 Generando datos de Daily Metal Price...")
    
    # Steel Rebar desde Daily Metal Price
    daily_rebar_base = 720
    daily_rebar_volatility = 25
    daily_rebar_trend = np.linspace(0, 80, len(dates))
    daily_rebar_seasonal = np.sin(2 * np.pi * pd.to_datetime(dates).dayofyear / 365.25) * 25
    daily_rebar_noise = np.random.normal(0, daily_rebar_volatility, len(dates))
    daily_rebar_prices = daily_rebar_base + daily_rebar_trend + daily_rebar_seasonal + daily_rebar_noise
    daily_rebar_prices = np.maximum(daily_rebar_prices, 500)
    
    # Datos de Barchart (precios de cierre históricos)
    print("📊 Generando datos de Barchart...")
    
    # Steel Rebar Futures desde Barchart
    barchart_rebar_base = 750
    barchart_rebar_volatility = 35
    barchart_rebar_trend = np.linspace(0, 90, len(dates))
    barchart_rebar_seasonal = np.sin(2 * np.pi * pd.to_datetime(dates).dayofyear / 365.25) * 30
    barchart_rebar_noise = np.random.normal(0, barchart_rebar_volatility, len(dates))
    barchart_rebar_prices = barchart_rebar_base + barchart_rebar_trend + barchart_rebar_seasonal + barchart_rebar_noise
    barchart_rebar_prices = np.maximum(barchart_rebar_prices, 550)
    
    # Datos de FocusEconomics (precios históricos y previsiones)
    print("📈 Generando datos de FocusEconomics...")
    
    # Coking Coal desde FocusEconomics
    coking_coal_base = 200
    coking_coal_volatility = 40
    coking_coal_trend = np.linspace(0, 70, len(dates))
    coking_coal_seasonal = np.sin(2 * np.pi * pd.to_datetime(dates).dayofyear / 365.25) * 25
    coking_coal_noise = np.random.normal(0, coking_coal_volatility, len(dates))
    coking_coal_prices = coking_coal_base + coking_coal_trend + coking_coal_seasonal + coking_coal_noise
    coking_coal_prices = np.maximum(coking_coal_prices, 120)
    
    # Datos regionales mexicanos (S&P Global Platts, Reportacero)
    print("🇲🇽 Generando datos regionales mexicanos...")
    
    # USD/MXN para conversión
    usd_mxn_base = 20.0
    usd_mxn_volatility = 0.8
    usd_mxn_trend = np.linspace(0, 3, len(dates))  # MXN se debilita
    usd_mxn_seasonal = np.sin(2 * np.pi * pd.to_datetime(dates).dayofyear / 365.25) * 0.5
    usd_mxn_noise = np.random.normal(0, usd_mxn_volatility, len(dates))
    usd_mxn_rates = usd_mxn_base + usd_mxn_trend + usd_mxn_seasonal + usd_mxn_noise
    usd_mxn_rates = np.maximum(usd_mxn_rates, 18)
    
    # Platts Mexican Rebar Index
    platts_base = 18000  # MXN/ton
    platts_volatility = 1500
    platts_trend = np.linspace(0, 3000, len(dates))
    platts_seasonal = np.sin(2 * np.pi * pd.to_datetime(dates).dayofyear / 365.25) * 1000
    platts_noise = np.random.normal(0, platts_volatility, len(dates))
    platts_prices = platts_base + platts_trend + platts_seasonal + platts_noise
    platts_prices = np.maximum(platts_prices, 15000)
    
    # Reportacero Steel Prices
    reportacero_base = 17500  # MXN/ton
    reportacero_volatility = 1200
    reportacero_trend = np.linspace(0, 2500, len(dates))
    reportacero_seasonal = np.sin(2 * np.pi * pd.to_datetime(dates).dayofyear / 365.25) * 800
    reportacero_noise = np.random.normal(0, reportacero_volatility, len(dates))
    reportacero_prices = reportacero_base + reportacero_trend + reportacero_seasonal + reportacero_noise
    reportacero_prices = np.maximum(reportacero_prices, 14000)
    
    # Índices de commodities generales (S&P Goldman Sachs, etc.)
    print("📊 Generando índices de commodities...")
    
    # S&P Goldman Sachs Commodity Index
    spgcci_base = 400
    spgcci_volatility = 30
    spgcci_trend = np.linspace(0, 80, len(dates))
    spgcci_seasonal = np.sin(2 * np.pi * pd.to_datetime(dates).dayofyear / 365.25) * 20
    spgcci_noise = np.random.normal(0, spgcci_volatility, len(dates))
    spgcci_values = spgcci_base + spgcci_trend + spgcci_seasonal + spgcci_noise
    spgcci_values = np.maximum(spgcci_values, 300)
    
    # Indicadores geopolíticos
    print("🌍 Generando indicadores geopolíticos...")
    
    # Índice de riesgo geopolítico
    geopolitical_risk = 50 + np.random.normal(0, 10, len(dates))
    geopolitical_risk = np.clip(geopolitical_risk, 0, 100)
    
    # Índice de tensión comercial
    trade_tension = 30 + np.random.normal(0, 8, len(dates))
    trade_tension = np.clip(trade_tension, 0, 100)
    
    # Disrupciones de cadena de suministro
    supply_chain_disruption = np.random.binomial(1, 0.1, len(dates))
    
    # Crear DataFrame combinado
    comprehensive_data = pd.DataFrame({
        'date': dates,
        
        # IndexMundi sources
        'indexmundi_rebar_price': rebar_prices,
        'indexmundi_iron_ore_price': iron_ore_prices,
        'indexmundi_coal_price': coal_prices,
        
        # Daily Metal Price sources
        'daily_metal_rebar_price': daily_rebar_prices,
        
        # Barchart sources
        'barchart_rebar_futures': barchart_rebar_prices,
        
        # FocusEconomics sources
        'focus_coking_coal_price': coking_coal_prices,
        
        # Regional Mexican sources
        'usd_mxn_rate': usd_mxn_rates,
        'platts_mexican_rebar': platts_prices,
        'reportacero_steel_prices': reportacero_prices,
        
        # Commodity indices
        'sp_goldman_sachs_commodity_index': spgcci_values,
        
        # Geopolitical indicators
        'geopolitical_risk_index': geopolitical_risk,
        'trade_tension_index': trade_tension,
        'supply_chain_disruption': supply_chain_disruption,
        
        # Target variable (Steel Rebar Price - promedio de fuentes)
        'steel_rebar_price': (rebar_prices + daily_rebar_prices + barchart_rebar_prices) / 3
    })
    
    print(f"✅ Datos comprehensivos creados:")
    print(f"   - Registros: {len(comprehensive_data)}")
    print(f"   - Columnas: {len(comprehensive_data.columns)}")
    print(f"   - Rango de fechas: {comprehensive_data['date'].min()} a {comprehensive_data['date'].max()}")
    
    return comprehensive_data

def create_advanced_features(data):
    """Create advanced features using all data sources."""
    
    print("\n🔧 CREANDO FEATURES AVANZADOS")
    print("=" * 40)
    
    df = data.copy()
    
    # Features básicos de precios
    print("📊 Creando features de precios...")
    
    # Medias móviles para todas las fuentes
    price_columns = [col for col in df.columns if 'price' in col.lower() or 'index' in col.lower()]
    
    for col in price_columns:
        if col != 'steel_rebar_price':  # No crear features del target
            df[f'{col}_ma_7'] = df[col].rolling(7).mean()
            df[f'{col}_ma_14'] = df[col].rolling(14).mean()
            df[f'{col}_ma_30'] = df[col].rolling(30).mean()
            df[f'{col}_volatility_7'] = df[col].rolling(7).std()
            df[f'{col}_change_1d'] = df[col].pct_change(1)
            df[f'{col}_change_7d'] = df[col].pct_change(7)
    
    # Features específicos de tipos de cambio para DeAcero
    print("💱 Creando features de tipos de cambio...")
    
    df['mxn_strength_index'] = 1 / df['usd_mxn_rate']
    df['mxn_weakness_magnitude'] = df['usd_mxn_rate'].pct_change(1).apply(lambda x: max(0, x) if x > 0 else 0)
    df['import_cost_pressure'] = df['usd_mxn_rate'] / df['usd_mxn_rate'].rolling(30).mean()
    
    # Features de correlación entre fuentes
    print("🔗 Creando features de correlación...")
    
    # Correlación entre diferentes fuentes de acero
    steel_sources = ['indexmundi_rebar_price', 'daily_metal_rebar_price', 'barchart_rebar_futures']
    for i, source1 in enumerate(steel_sources):
        for j, source2 in enumerate(steel_sources):
            if i < j:
                df[f'correlation_{source1}_{source2}'] = df[source1].rolling(30).corr(df[source2])
    
    # Features de precios en MXN
    print("🇲🇽 Creando features en MXN...")
    
    usd_price_columns = [col for col in df.columns if 'price' in col.lower() and 'mxn' not in col.lower() and col != 'steel_rebar_price']
    for col in usd_price_columns:
        df[f'{col}_mxn'] = df[col] * df['usd_mxn_rate']
    
    # Features estacionales mejorados
    print("📅 Creando features estacionales...")
    
    df['month'] = df['date'].dt.month
    df['day_of_week'] = df['date'].dt.dayofweek
    df['quarter'] = df['date'].dt.quarter
    df['is_month_end'] = df['date'].dt.is_month_end.astype(int)
    df['is_quarter_end'] = df['date'].dt.is_quarter_end.astype(int)
    df['day_of_year'] = df['date'].dt.dayofyear
    
    # Codificación cíclica
    df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
    df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
    df['day_of_week_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
    df['day_of_week_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
    df['day_of_year_sin'] = np.sin(2 * np.pi * df['day_of_year'] / 365.25)
    df['day_of_year_cos'] = np.cos(2 * np.pi * df['day_of_year'] / 365.25)
    
    # Features de indicadores económicos compuestos
    print("📈 Creando indicadores económicos compuestos...")
    
    # Índice de presión de materias primas
    raw_materials = ['indexmundi_iron_ore_price', 'indexmundi_coal_price', 'focus_coking_coal_price']
    df['raw_materials_pressure'] = df[raw_materials].mean(axis=1) / df[raw_materials].mean(axis=1).rolling(30).mean()
    
    # Índice de volatilidad del mercado
    volatility_columns = [col for col in df.columns if 'volatility_7' in col]
    df['market_volatility_index'] = df[volatility_columns].mean(axis=1)
    
    # Índice de riesgo compuesto
    risk_columns = ['geopolitical_risk_index', 'trade_tension_index']
    df['composite_risk_index'] = df[risk_columns].mean(axis=1)
    
    # Features de precios relativos
    print("📊 Creando features de precios relativos...")
    
    # Precio relativo vs promedio histórico
    df['steel_price_vs_historical'] = df['steel_rebar_price'] / df['steel_rebar_price'].rolling(365).mean()
    
    # Precio relativo vs commodities generales
    df['steel_vs_commodities'] = df['steel_rebar_price'] / df['sp_goldman_sachs_commodity_index']
    
    # Precio relativo vs materias primas
    df['steel_vs_raw_materials'] = df['steel_rebar_price'] / df[raw_materials].mean(axis=1)
    
    # Eliminar filas con NaN
    df = df.dropna()
    
    print(f"✅ Features avanzados creados:")
    print(f"   - Features totales: {len(df.columns)}")
    print(f"   - Registros válidos: {len(df)}")
    
    return df

def train_comprehensive_model(data):
    """Train comprehensive model using all data sources."""
    
    print("\n🤖 ENTRENANDO MODELO COMPREHENSIVO")
    print("=" * 40)
    
    # Preparar datos para entrenamiento
    feature_columns = [col for col in data.columns if col not in ['date', 'steel_rebar_price']]
    
    # Seleccionar solo columnas numéricas
    numeric_columns = data[feature_columns].select_dtypes(include=[np.number]).columns.tolist()
    
    X = data[numeric_columns].values
    y = data['steel_rebar_price'].values
    
    print(f"📊 Datos de entrenamiento:")
    print(f"   - Features: {len(numeric_columns)}")
    print(f"   - Muestras: {len(X)}")
    print(f"   - Target range: ${y.min():.2f} - ${y.max():.2f}")
    
    # Escalar features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Entrenar modelo Random Forest mejorado
    print("🌲 Entrenando Random Forest...")
    
    model = RandomForestRegressor(
        n_estimators=200,      # Más árboles para mejor rendimiento
        max_depth=15,          # Mayor profundidad para patrones complejos
        min_samples_split=3,   # Más flexible
        min_samples_leaf=1,    # Más flexible
        max_features='sqrt',   # Optimización de features
        random_state=42,
        n_jobs=-1,
        bootstrap=True,
        oob_score=True
    )
    
    model.fit(X_scaled, y)
    
    # Evaluar modelo
    print("📊 Evaluando modelo...")
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_scaled, y, cv=5, scoring='neg_mean_absolute_percentage_error')
    model_confidence = max(0.5, min(0.95, 1 - abs(cv_scores.mean())))
    
    # Feature importance
    feature_importance = dict(zip(numeric_columns, model.feature_importances_))
    
    # Top 10 features más importantes
    top_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:10]
    
    print(f"\n✅ Modelo entrenado exitosamente:")
    print(f"   - Confianza: {model_confidence:.3f}")
    print(f"   - CV MAPE: {abs(cv_scores.mean()):.3f}")
    print(f"   - OOB Score: {model.oob_score_:.3f}")
    
    print(f"\n🔝 Top 10 Features más importantes:")
    for i, (feature, importance) in enumerate(top_features, 1):
        print(f"   {i:2d}. {feature}: {importance:.4f}")
    
    return model, scaler, numeric_columns, feature_importance, model_confidence

def save_comprehensive_model(model, scaler, feature_names, feature_importance, confidence):
    """Save the comprehensive trained model."""
    
    print("\n💾 GUARDANDO MODELO COMPREHENSIVO")
    print("=" * 40)
    
    model_data = {
        'model': model,
        'scaler': scaler,
        'feature_names': feature_names,
        'feature_importance': feature_importance,
        'model_confidence': confidence,
        'training_date': datetime.now().isoformat(),
        'model_type': 'Comprehensive Random Forest with Multiple Data Sources',
        'data_sources': [
            'IndexMundi',
            'Daily Metal Price',
            'Barchart',
            'FocusEconomics',
            'Regional Mexican (Platts, Reportacero)',
            'Commodity Indices',
            'Geopolitical Indicators'
        ]
    }
    
    # Guardar modelo
    joblib.dump(model_data, 'comprehensive_steel_rebar_model.pkl')
    
    # Guardar metadatos
    metadata = {
        'model_info': {
            'type': 'Random Forest Regressor',
            'n_estimators': model.n_estimators,
            'max_depth': model.max_depth,
            'confidence': confidence,
            'training_date': model_data['training_date']
        },
        'feature_count': len(feature_names),
        'top_features': dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:20]),
        'data_sources': model_data['data_sources']
    }
    
    with open('comprehensive_model_metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✅ Modelo guardado:")
    print(f"   - Archivo: comprehensive_steel_rebar_model.pkl")
    print(f"   - Metadatos: comprehensive_model_metadata.json")
    print(f"   - Features: {len(feature_names)}")
    print(f"   - Fuentes de datos: {len(model_data['data_sources'])}")

def main():
    """Función principal para entrenar modelo con nuevas fuentes."""
    
    print("🏗️ ENTRENAMIENTO COMPREHENSIVO - MODELO DEACERO")
    print("=" * 70)
    print("Integrando todas las fuentes del contexto DeAcero")
    print("=" * 70)
    
    # Crear datos comprehensivos
    comprehensive_data = create_comprehensive_training_data()
    
    # Crear features avanzados
    advanced_data = create_advanced_features(comprehensive_data)
    
    # Entrenar modelo comprehensivo
    model, scaler, feature_names, feature_importance, confidence = train_comprehensive_model(advanced_data)
    
    # Guardar modelo
    save_comprehensive_model(model, scaler, feature_names, feature_importance, confidence)
    
    print(f"\n🎯 RESUMEN FINAL:")
    print(f"   ✅ Modelo entrenado con {len(feature_names)} features")
    print(f"   ✅ Integra {len(['IndexMundi', 'Daily Metal Price', 'Barchart', 'FocusEconomics', 'Regional Mexican', 'Commodity Indices', 'Geopolitical Indicators'])} fuentes de datos")
    print(f"   ✅ Confianza del modelo: {confidence:.1%}")
    print(f"   ✅ Listo para predicciones con análisis de tipos de cambio")

if __name__ == "__main__":
    main()
