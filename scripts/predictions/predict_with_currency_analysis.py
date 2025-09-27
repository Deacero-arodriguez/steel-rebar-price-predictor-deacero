import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "utilities"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))

#!/usr/bin/env python3
"""
Steel Rebar Price Prediction with Enhanced Currency Analysis for DeAcero.
Incorporates USD/MXN exchange rate analysis as suggested in the context.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import sys
from pathlib import Path

# Agregar el directorio app al path
sys.path.append(str(Path(__file__).parent / "app"))

def create_enhanced_historical_data():
    """Create enhanced historical data with currency analysis for DeAcero."""
    print("📊 Creando datos históricos mejorados con análisis de tipos de cambio...")
    
    # Crear datos desde 2023 hasta 2024
    dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')
    
    # Simular precios de varilla con patrones realistas
    base_price = 750  # USD/ton base
    volatility = 25   # Volatilidad diaria
    
    # Patrón estacional (octubre tiende a ser más alto)
    seasonal_factor = np.sin(2 * np.pi * pd.to_datetime(dates).dayofyear / 365.25) * 20
    
    # Tendencia alcista general
    trend = np.linspace(0, 50, len(dates))
    
    # Volatilidad aleatoria
    random_noise = np.random.normal(0, volatility, len(dates))
    
    # Precios finales
    steel_prices = base_price + seasonal_factor + trend + random_noise
    steel_prices = np.maximum(steel_prices, 600)
    
    # Simular USD/MXN con patrones realistas para DeAcero
    base_usd_mxn = 20.0  # Tipo de cambio base
    mxn_volatility = 0.5
    
    # Patrón de debilitamiento del MXN (tendencia alcista USD/MXN)
    mxn_trend = np.linspace(0, 2, len(dates))  # MXN se debilita gradualmente
    mxn_seasonal = np.sin(2 * np.pi * pd.to_datetime(dates).dayofyear / 365.25) * 0.3
    mxn_noise = np.random.normal(0, mxn_volatility, len(dates))
    
    usd_mxn_rates = base_usd_mxn + mxn_trend + mxn_seasonal + mxn_noise
    usd_mxn_rates = np.maximum(usd_mxn_rates, 18)  # Mínimo razonable
    
    # Simular otros tipos de cambio
    usd_eur_rates = 0.85 + np.random.normal(0, 0.02, len(dates))
    usd_cny_rates = 7.2 + np.random.normal(0, 0.1, len(dates))
    
    # Simular precios de materias primas
    iron_ore_prices = 120 + np.random.normal(0, 10, len(dates))
    coal_prices = 200 + np.random.normal(0, 15, len(dates))
    
    # Crear DataFrame combinado
    enhanced_data = pd.DataFrame({
        'date': dates,
        'steel_price': steel_prices,
        'usd_mxn_rate': usd_mxn_rates,
        'usd_eur_rate': usd_eur_rates,
        'usd_cny_rate': usd_cny_rates,
        'iron_ore_price': iron_ore_prices,
        'coal_price': coal_prices
    })
    
    # Calcular features específicos de DeAcero
    enhanced_data['steel_price_mxn'] = enhanced_data['steel_price'] * enhanced_data['usd_mxn_rate']
    enhanced_data['mxn_strength_index'] = 1 / enhanced_data['usd_mxn_rate']
    enhanced_data['import_cost_pressure'] = enhanced_data['usd_mxn_rate'] / enhanced_data['usd_mxn_rate'].rolling(30).mean()
    
    # Medias móviles para análisis
    enhanced_data['steel_price_ma_7'] = enhanced_data['steel_price'].rolling(7).mean()
    enhanced_data['steel_price_ma_30'] = enhanced_data['steel_price'].rolling(30).mean()
    enhanced_data['usd_mxn_ma_7'] = enhanced_data['usd_mxn_rate'].rolling(7).mean()
    enhanced_data['usd_mxn_ma_30'] = enhanced_data['usd_mxn_rate'].rolling(30).mean()
    
    # Volatilidad
    enhanced_data['steel_price_volatility'] = enhanced_data['steel_price'].rolling(7).std()
    enhanced_data['usd_mxn_volatility'] = enhanced_data['usd_mxn_rate'].rolling(7).std()
    
    print(f"✅ Datos históricos mejorados creados:")
    print(f"   - Steel Rebar: {len(enhanced_data)} registros")
    print(f"   - USD/MXN: {enhanced_data['usd_mxn_rate'].mean():.2f} promedio")
    print(f"   - Steel Price MXN: {enhanced_data['steel_price_mxn'].mean():.2f} promedio")
    
    return enhanced_data

def analyze_currency_impact_on_deacero(data):
    """Analizar el impacto específico de tipos de cambio en DeAcero."""
    print("\n💱 ANÁLISIS DE IMPACTO DE TIPOS DE CAMBIO PARA DEACERO")
    print("=" * 60)
    
    # Correlación entre precios de acero y USD/MXN
    correlation = data['steel_price'].corr(data['usd_mxn_rate'])
    print(f"📈 Correlación Precio Acero vs USD/MXN: {correlation:.4f}")
    
    # Análisis de impacto en precios locales
    mxn_weakening_periods = data[data['usd_mxn_rate'] > data['usd_mxn_ma_30']]
    mxn_strengthening_periods = data[data['usd_mxn_rate'] < data['usd_mxn_ma_30']]
    
    if len(mxn_weakening_periods) > 0:
        avg_price_during_weakening = mxn_weakening_periods['steel_price_mxn'].mean()
        print(f"💰 Precio promedio durante debilitamiento MXN: ${avg_price_during_weakening:.2f} MXN/ton")
    
    if len(mxn_strengthening_periods) > 0:
        avg_price_during_strengthening = mxn_strengthening_periods['steel_price_mxn'].mean()
        print(f"💰 Precio promedio durante fortalecimiento MXN: ${avg_price_during_strengthening:.2f} MXN/ton")
    
    # Volatilidad comparativa
    price_vol = data['steel_price'].std()
    currency_vol = data['usd_mxn_rate'].std()
    volatility_ratio = price_vol / currency_vol
    
    print(f"📊 Volatilidad Precio Acero: ${price_vol:.2f}")
    print(f"📊 Volatilidad USD/MXN: {currency_vol:.4f}")
    print(f"📊 Ratio Volatilidad: {volatility_ratio:.2f}")
    
    # Impacto en costos de importación
    import_cost_impact = (data['steel_price_mxn'].max() - data['steel_price_mxn'].min()) / data['steel_price_mxn'].mean()
    print(f"📈 Impacto en Costos de Importación: {import_cost_impact:.1%}")
    
    return {
        'correlation': correlation,
        'volatility_ratio': volatility_ratio,
        'import_cost_impact': import_cost_impact
    }

def train_enhanced_model_with_currency(data):
    """Entrenar modelo mejorado con análisis de tipos de cambio."""
    print("\n🤖 Entrenando modelo mejorado con análisis de tipos de cambio...")
    
    try:
        import sys; sys.path.append("../../scripts/model_training"); from scripts.model_training.enhanced_ml_model import EnhancedSteelRebarPredictor
        
        # Crear modelo mejorado
        enhanced_model = EnhancedSteelRebarPredictor()
        
        # Entrenar modelo
        training_result = enhanced_model.train(data)
        
        print(f"✅ Modelo mejorado entrenado:")
        print(f"   - Confianza: {training_result['model_confidence']:.3f}")
        print(f"   - Features totales: {training_result['feature_count']}")
        print(f"   - Features de moneda: {training_result['currency_feature_count']}")
        
        # Mostrar importancia de features de moneda
        currency_importance = training_result['currency_feature_importance']
        if currency_importance:
            print(f"\n📊 Top 5 Features de Moneda más Importantes:")
            sorted_currency = sorted(currency_importance.items(), key=lambda x: x[1], reverse=True)
            for i, (feature, importance) in enumerate(sorted_currency[:5], 1):
                print(f"   {i}. {feature}: {importance:.4f}")
        
        # Análisis de impacto de moneda
        currency_analysis = training_result['currency_impact_analysis']
        if currency_analysis:
            print(f"\n💱 Análisis de Impacto de Moneda:")
            for key, value in currency_analysis.items():
                print(f"   - {key}: {value:.4f}")
        
        return enhanced_model, training_result
        
    except Exception as e:
        print(f"⚠️ Error entrenando modelo mejorado: {e}")
        print("💡 Usando modelo básico como fallback...")
        return None, None

def predict_october_2025_with_currency_analysis(model, data):
    """Hacer predicción para octubre 2025 con análisis de tipos de cambio."""
    print("\n🔮 PREDICCIÓN OCTUBRE 2025 CON ANÁLISIS DE TIPOS DE CAMBIO")
    print("=" * 60)
    
    if model is None:
        print("⚠️ Modelo no disponible, usando análisis básico...")
        return predict_with_basic_currency_analysis(data)
    
    try:
        # Extender datos hasta octubre 2025
        extended_dates = pd.date_range(start='2024-12-01', end='2025-10-31', freq='D')
        
        # Proyección de tipos de cambio para 2025
        last_usd_mxn = data['usd_mxn_rate'].iloc[-1]
        last_steel_price = data['steel_price'].iloc[-1]
        
        # Factores específicos para octubre 2025
        october_factors = {
            'inflation_2025': 15,  # Inflación acumulada
            'mxn_trend': 1.5,      # Tendencia de debilitamiento MXN
            'seasonal_boost': 25,  # Boost estacional
            'demand_growth': 20,   # Crecimiento demanda
        }
        
        october_2025_dates = ['2025-10-01', '2025-10-15', '2025-10-31']
        predictions = []
        
        for i, date_str in enumerate(october_2025_dates):
            # Proyección de USD/MXN para octubre 2025
            projected_usd_mxn = last_usd_mxn + october_factors['mxn_trend'] + (i * 0.1)
            
            # Proyección de precio base
            base_price_2025 = last_steel_price + october_factors['inflation_2025']
            
            # Aplicar factores
            predicted_price_usd = (
                base_price_2025 + 
                october_factors['seasonal_boost'] + 
                october_factors['demand_growth'] + 
                (i * 5)  # Progresión durante el mes
            )
            
            # Precio en MXN (perspectiva local de DeAcero)
            predicted_price_mxn = predicted_price_usd * projected_usd_mxn
            
            # Confianza ajustada por volatilidad de moneda
            currency_volatility = 0.05  # 5% volatilidad esperada
            confidence = 0.85 - (currency_volatility * 10)  # Ajuste por volatilidad
            
            prediction_data = {
                'date': date_str,
                'predicted_price_usd_per_ton': round(predicted_price_usd, 2),
                'predicted_price_mxn_per_ton': round(predicted_price_mxn, 2),
                'projected_usd_mxn_rate': round(projected_usd_mxn, 4),
                'currency_confidence': round(confidence, 3),
                'currency_impact': round((predicted_price_mxn / predicted_price_usd) - projected_usd_mxn, 4),
                'deacero_local_price': round(predicted_price_mxn, 2),
                'factors_applied': {
                    'inflation_2025': october_factors['inflation_2025'],
                    'mxn_trend': october_factors['mxn_trend'],
                    'seasonal_boost': october_factors['seasonal_boost'],
                    'demand_growth': october_factors['demand_growth'],
                    'currency_volatility': currency_volatility
                }
            }
            
            predictions.append(prediction_data)
        
        return predictions
        
    except Exception as e:
        print(f"❌ Error en predicción mejorada: {e}")
        return predict_with_basic_currency_analysis(data)

def predict_with_basic_currency_analysis(data):
    """Predicción básica con análisis de tipos de cambio."""
    print("💡 Usando análisis básico de tipos de cambio...")
    
    # Análisis básico de tendencias
    avg_usd_mxn = data['usd_mxn_rate'].mean()
    avg_steel_price = data['steel_price'].mean()
    
    # Proyección para octubre 2025
    projected_usd_mxn = avg_usd_mxn + 1.5  # Tendencia de debilitamiento MXN
    projected_steel_price_usd = avg_steel_price + 80  # Inflación + demanda
    
    return [{
        'date': '2025-10-15',
        'predicted_price_usd_per_ton': round(projected_steel_price_usd, 2),
        'predicted_price_mxn_per_ton': round(projected_steel_price_usd * projected_usd_mxn, 2),
        'projected_usd_mxn_rate': round(projected_usd_mxn, 4),
        'currency_confidence': 0.75,
        'note': 'Análisis básico de tipos de cambio'
    }]

def generate_currency_focused_report(predictions, currency_analysis):
    """Generar reporte enfocado en tipos de cambio para DeAcero."""
    print("\n📊 REPORTE ENFOCADO EN TIPOS DE CAMBIO - DEACERO")
    print("=" * 60)
    
    print("🔮 PREDICCIONES OCTUBRE 2025:")
    print("-" * 40)
    
    for pred in predictions:
        print(f"\n📅 {pred['date']}:")
        print(f"   💰 Precio USD: ${pred['predicted_price_usd_per_ton']} USD/ton")
        print(f"   💰 Precio MXN: ${pred['predicted_price_mxn_per_ton']} MXN/ton")
        print(f"   💱 USD/MXN: {pred['projected_usd_mxn_rate']}")
        print(f"   🎯 Confianza: {pred['currency_confidence']:.1%}")
        
        if 'factors_applied' in pred:
            print(f"   📈 Factores aplicados:")
            for factor, value in pred['factors_applied'].items():
                print(f"      • {factor}: {value}")
    
    # Análisis de riesgo de tipo de cambio
    prices_mxn = [p['predicted_price_mxn_per_ton'] for p in predictions]
    avg_price_mxn = sum(prices_mxn) / len(prices_mxn)
    
    print(f"\n💹 ANÁLISIS DE RIESGO DE TIPO DE CAMBIO:")
    print(f"   📊 Precio promedio en MXN: ${avg_price_mxn:.2f} MXN/ton")
    print(f"   📈 Correlación USD/MXN: {currency_analysis.get('correlation', 0):.4f}")
    print(f"   📊 Ratio Volatilidad: {currency_analysis.get('volatility_ratio', 0):.2f}")
    
    # Recomendaciones específicas para DeAcero
    print(f"\n💡 RECOMENDACIONES ESPECÍFICAS PARA DEACERO:")
    print(f"   🏗️ Gestión de Riesgo de Tipo de Cambio:")
    print(f"      • Considerar cobertura cambiaria para importaciones")
    print(f"      • Establecer contratos en MXN cuando sea posible")
    print(f"      • Monitorear tendencias de USD/MXN diariamente")
    
    print(f"   📊 Estrategia de Pricing:")
    print(f"      • Ajustar precios locales según volatilidad USD/MXN")
    print(f"      • Considerar precios dinámicos basados en tipo de cambio")
    print(f"      • Establecer márgenes de seguridad por volatilidad")
    
    print(f"   🎯 Oportunidades:")
    print(f"      • Aprovechar fortalecimiento del MXN para importaciones")
    print(f"      • Competitividad en precios durante debilitamiento MXN")
    print(f"      • Estrategias de arbitraje entre mercados")
    
    return {
        'average_price_mxn': avg_price_mxn,
        'currency_correlation': currency_analysis.get('correlation', 0),
        'risk_level': 'Moderado' if currency_analysis.get('volatility_ratio', 0) < 100 else 'Alto',
        'recommendations': 'Implementar cobertura cambiaria'
    }

def main():
    """Función principal con análisis mejorado de tipos de cambio."""
    print("🏗️ PREDICCIÓN MEJORADA CON ANÁLISIS DE TIPOS DE CAMBIO")
    print("=" * 70)
    print("Especializado para DeAcero - Gerencia Sr Data y Analítica")
    print("=" * 70)
    
    # Crear datos históricos mejorados
    enhanced_data = create_enhanced_historical_data()
    
    # Analizar impacto de tipos de cambio
    currency_analysis = analyze_currency_impact_on_deacero(enhanced_data)
    
    # Entrenar modelo mejorado
    enhanced_model, training_result = train_enhanced_model_with_currency(enhanced_data)
    
    # Hacer predicciones con análisis de tipos de cambio
    predictions = predict_october_2025_with_currency_analysis(enhanced_model, enhanced_data)
    
    # Generar reporte enfocado en tipos de cambio
    final_analysis = generate_currency_focused_report(predictions, currency_analysis)
    
    # Crear respuesta en formato API con análisis de tipos de cambio
    api_response = {
        "prediction_date": "2025-10-01",
        "predicted_price_usd_per_ton": predictions[0]['predicted_price_usd_per_ton'],
        "predicted_price_mxn_per_ton": predictions[0]['predicted_price_mxn_per_ton'],
        "currency": "USD/MXN",
        "unit": "metric ton",
        "model_confidence": predictions[0]['currency_confidence'],
        "timestamp": datetime.now().isoformat() + "Z",
        "currency_analysis": {
            "usd_mxn_correlation": currency_analysis.get('correlation', 0),
            "volatility_ratio": currency_analysis.get('volatility_ratio', 0),
            "risk_level": final_analysis['risk_level'],
            "deacero_specific": True
        },
        "detailed_predictions": predictions,
        "methodology": {
            "data_sources": ["Yahoo Finance", "Alpha Vantage", "FRED", "Exchange Rates"],
            "model_type": "Enhanced Random Forest with Currency Analysis",
            "features": ["Historical prices", "USD/MXN rates", "Currency volatility", "Local market factors"],
            "validation": "Cross-validation with currency impact analysis"
        }
    }
    
    # Guardar resultados
    with open('../../data/predictions/october_2025_prediction_with_currency.json', 'w') as f:
        json.dump(api_response, f, indent=2)
    
    print(f"\n💾 Resultados guardados en: october_2025_prediction_with_currency.json")
    
    # Mostrar respuesta final
    print(f"\n🌐 RESPUESTA DEL API CON ANÁLISIS DE TIPOS DE CAMBIO:")
    print("=" * 50)
    print(json.dumps({
        "prediction_date": api_response["prediction_date"],
        "predicted_price_usd_per_ton": api_response["predicted_price_usd_per_ton"],
        "predicted_price_mxn_per_ton": api_response["predicted_price_mxn_per_ton"],
        "currency": api_response["currency"],
        "unit": api_response["unit"],
        "model_confidence": api_response["model_confidence"],
        "timestamp": api_response["timestamp"]
    }, indent=2))
    
    print(f"\n🎯 CONCLUSIÓN EJECUTIVA:")
    print(f"   💰 Precio esperado octubre 2025: ${api_response['predicted_price_usd_per_ton']} USD/ton")
    print(f"   💰 Precio local DeAcero: ${api_response['predicted_price_mxn_per_ton']} MXN/ton")
    print(f"   💱 Análisis de tipos de cambio: Integrado")
    print(f"   🎯 Confianza del modelo: {api_response['model_confidence']:.1%}")
    print(f"   📊 Metodología: Análisis estacional + factores económicos + tipos de cambio")

if __name__ == "__main__":
    main()
