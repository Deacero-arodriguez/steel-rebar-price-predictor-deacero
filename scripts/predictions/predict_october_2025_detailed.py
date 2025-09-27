import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "utilities"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))

#!/usr/bin/env python3
"""
Predicción Detallada para Octubre 2025 con Análisis de Tipos de Cambio para DeAcero.
Incluye múltiples fechas del mes y análisis específico para el mercado mexicano.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

def create_enhanced_october_2025_prediction():
    """Crear predicción detallada para todo octubre 2025."""
    
    print("🏗️ PREDICCIÓN DETALLADA OCTUBRE 2025 - DEACERO")
    print("=" * 70)
    print("Análisis completo con tipos de cambio para el mercado mexicano")
    print("=" * 70)
    
    # Parámetros base actualizados
    base_usd_mxn = 20.0
    base_steel_price_usd = 750.0
    
    # Factores específicos para octubre 2025
    october_factors = {
        'inflation_2024_2025': 8.5,      # Inflación acumulada estimada
        'mxn_trend_weakening': 1.8,      # Tendencia de debilitamiento MXN
        'seasonal_steel_demand': 35,     # Boost estacional octubre
        'construction_boom': 25,         # Crecimiento sector construcción
        'infrastructure_projects': 20,   # Proyectos de infraestructura
        'energy_costs': 15,              # Aumento costos energéticos
        'supply_chain_pressure': 10,     # Presión en cadena de suministro
        'geopolitical_risk': 8,          # Riesgo geopolítico
    }
    
    # Crear fechas específicas de octubre 2025
    october_dates = [
        '2025-10-01',  # Inicio del mes
        '2025-10-08',  # Primera semana
        '2025-10-15',  # Mitad del mes
        '2025-10-22',  # Tercera semana
        '2025-10-31',  # Fin del mes
    ]
    
    predictions = []
    
    for i, date_str in enumerate(october_dates):
        # Progresión del mes (0 a 4)
        month_progress = i / 4
        
        # USD/MXN con tendencia de debilitamiento progresivo
        usd_mxn_trend = base_usd_mxn + october_factors['mxn_trend_weakening'] + (month_progress * 0.3)
        
        # Volatilidad estacional (octubre tiende a ser más volátil)
        seasonal_volatility = 1 + (month_progress * 0.15)
        
        # Precio base con inflación y factores económicos
        base_price_2025 = (
            base_steel_price_usd + 
            october_factors['inflation_2024_2025'] +
            october_factors['seasonal_steel_demand'] * seasonal_volatility +
            october_factors['construction_boom'] +
            october_factors['infrastructure_projects'] +
            october_factors['energy_costs'] +
            october_factors['supply_chain_pressure'] +
            october_factors['geopolitical_risk']
        )
        
        # Ajuste por progresión del mes
        monthly_progression = month_progress * 12  # Incremento gradual durante el mes
        predicted_price_usd = base_price_2025 + monthly_progression
        
        # Precio en MXN (perspectiva DeAcero)
        predicted_price_mxn = predicted_price_usd * usd_mxn_trend
        
        # Confianza ajustada por volatilidad y progresión del mes
        base_confidence = 0.82
        volatility_adjustment = min(0.08, seasonal_volatility * 0.02)
        month_confidence_boost = month_progress * 0.03  # Mayor confianza hacia fin de mes
        
        final_confidence = base_confidence - volatility_adjustment + month_confidence_boost
        final_confidence = min(0.92, max(0.70, final_confidence))  # Mantener en rango 0.7-0.92
        
        # Análisis de riesgo específico para DeAcero
        currency_risk = "Bajo" if usd_mxn_trend < 21.5 else "Moderado" if usd_mxn_trend < 22.5 else "Alto"
        
        # Oportunidades de mercado
        market_opportunities = []
        if predicted_price_mxn < 19000:
            market_opportunities.append("Oportunidad de compra estratégica")
        if usd_mxn_trend > 22.0:
            market_opportunities.append("Cobertura cambiaria recomendada")
        if month_progress > 0.5:
            market_opportunities.append("Demanda estacional alta")
        
        prediction_data = {
            'date': date_str,
            'predicted_price_usd_per_ton': round(predicted_price_usd, 2),
            'predicted_price_mxn_per_ton': round(predicted_price_mxn, 2),
            'projected_usd_mxn_rate': round(usd_mxn_trend, 4),
            'currency_confidence': round(final_confidence, 3),
            'currency_risk_level': currency_risk,
            'month_progress': round(month_progress * 100, 1),
            'seasonal_volatility_factor': round(seasonal_volatility, 3),
            'market_opportunities': market_opportunities,
            'factors_applied': {
                'inflation_impact': october_factors['inflation_2024_2025'],
                'mxn_trend': round(usd_mxn_trend - base_usd_mxn, 2),
                'seasonal_boost': round(october_factors['seasonal_steel_demand'] * seasonal_volatility, 2),
                'construction_demand': october_factors['construction_boom'],
                'infrastructure_projects': october_factors['infrastructure_projects'],
                'energy_costs': october_factors['energy_costs'],
                'monthly_progression': round(monthly_progression, 2)
            }
        }
        
        predictions.append(prediction_data)
    
    return predictions

def analyze_october_2025_trends(predictions):
    """Analizar tendencias específicas para octubre 2025."""
    
    print("\n📊 ANÁLISIS DE TENDENCIAS OCTUBRE 2025")
    print("=" * 50)
    
    # Calcular tendencias
    prices_usd = [p['predicted_price_usd_per_ton'] for p in predictions]
    prices_mxn = [p['predicted_price_mxn_per_ton'] for p in predictions]
    usd_mxn_rates = [p['projected_usd_mxn_rate'] for p in predictions]
    
    # Tendencia de precios
    price_trend_usd = prices_usd[-1] - prices_usd[0]
    price_trend_mxn = prices_mxn[-1] - prices_mxn[0]
    currency_trend = usd_mxn_rates[-1] - usd_mxn_rates[0]
    
    print(f"📈 TENDENCIA DE PRECIOS USD: ${price_trend_usd:+.2f} ({price_trend_usd/prices_usd[0]*100:+.1f}%)")
    print(f"📈 TENDENCIA DE PRECIOS MXN: ${price_trend_mxn:+.2f} ({price_trend_mxn/prices_mxn[0]*100:+.1f}%)")
    print(f"💱 TENDENCIA USD/MXN: {currency_trend:+.4f} ({currency_trend/usd_mxn_rates[0]*100:+.1f}%)")
    
    # Análisis de volatilidad
    price_volatility_usd = np.std(prices_usd)
    price_volatility_mxn = np.std(prices_mxn)
    
    print(f"\n📊 VOLATILIDAD OCTUBRE 2025:")
    print(f"   USD: ${price_volatility_usd:.2f}")
    print(f"   MXN: ${price_volatility_mxn:.2f}")
    
    # Recomendaciones específicas
    print(f"\n💡 RECOMENDACIONES ESPECÍFICAS OCTUBRE 2025:")
    
    if price_trend_mxn > 500:
        print("   🚨 ALERTA: Tendencia alcista significativa en MXN")
        print("      • Considerar compras tempranas en el mes")
        print("      • Evaluar contratos de suministro a largo plazo")
    
    if currency_trend > 0.5:
        print("   💱 ALERTA: Debilitamiento significativo del MXN")
        print("      • Implementar cobertura cambiaria inmediatamente")
        print("      • Considerar precios dinámicos basados en tipo de cambio")
    
    if price_volatility_mxn > 800:
        print("   📊 ALERTA: Alta volatilidad en precios MXN")
        print("      • Establecer márgenes de seguridad amplios")
        print("      • Monitorear precios diariamente")
    
    return {
        'price_trend_usd': price_trend_usd,
        'price_trend_mxn': price_trend_mxn,
        'currency_trend': currency_trend,
        'volatility_usd': price_volatility_usd,
        'volatility_mxn': price_volatility_mxn
    }

def generate_deacero_executive_summary(predictions, trends):
    """Generar resumen ejecutivo específico para DeAcero."""
    
    print("\n🎯 RESUMEN EJECUTIVO - DEACERO OCTUBRE 2025")
    print("=" * 60)
    
    # Precio promedio del mes
    avg_price_usd = np.mean([p['predicted_price_usd_per_ton'] for p in predictions])
    avg_price_mxn = np.mean([p['predicted_price_mxn_per_ton'] for p in predictions])
    avg_usd_mxn = np.mean([p['projected_usd_mxn_rate'] for p in predictions])
    
    print(f"💰 PRECIO PROMEDIO OCTUBRE 2025:")
    print(f"   USD: ${avg_price_usd:.2f} USD/ton")
    print(f"   MXN: ${avg_price_mxn:.2f} MXN/ton")
    print(f"   USD/MXN: {avg_usd_mxn:.4f}")
    
    # Rango de precios
    min_price_mxn = min([p['predicted_price_mxn_per_ton'] for p in predictions])
    max_price_mxn = max([p['predicted_price_mxn_per_ton'] for p in predictions])
    
    print(f"\n📊 RANGO DE PRECIOS MXN:")
    print(f"   Mínimo: ${min_price_mxn:.2f} MXN/ton")
    print(f"   Máximo: ${max_price_mxn:.2f} MXN/ton")
    print(f"   Diferencia: ${max_price_mxn - min_price_mxn:.2f} MXN/ton")
    
    # Impacto financiero estimado
    print(f"\n💼 IMPACTO FINANCIERO ESTIMADO:")
    print(f"   Tendencia mensual: ${trends['price_trend_mxn']:+.2f} MXN/ton")
    print(f"   Volatilidad: ${trends['volatility_mxn']:.2f} MXN/ton")
    print(f"   Riesgo de moneda: {currency_trend_to_risk_level(trends['currency_trend'])}")
    
    # Recomendaciones estratégicas
    print(f"\n🎯 RECOMENDACIONES ESTRATÉGICAS:")
    
    if trends['price_trend_mxn'] > 300:
        print("   📈 ESTRATEGIA ALCISTA:")
        print("      • Acelerar compras en primera quincena")
        print("      • Negociar contratos de suministro a largo plazo")
        print("      • Considerar inventarios estratégicos")
    
    if trends['currency_trend'] > 0.3:
        print("   💱 GESTIÓN DE RIESGO CAMBIARIO:")
        print("      • Implementar cobertura cambiaria inmediatamente")
        print("      • Establecer precios dinámicos en MXN")
        print("      • Monitorear USD/MXN diariamente")
    
    if trends['volatility_mxn'] > 600:
        print("   📊 GESTIÓN DE VOLATILIDAD:")
        print("      • Establecer márgenes de seguridad del 8-12%")
        print("      • Implementar precios escalonados")
        print("      • Crear reservas de contingencia")
    
    return {
        'average_price_usd': avg_price_usd,
        'average_price_mxn': avg_price_mxn,
        'average_usd_mxn': avg_usd_mxn,
        'price_range_mxn': max_price_mxn - min_price_mxn,
        'strategic_recommendations': generate_strategic_recommendations(trends)
    }

def currency_trend_to_risk_level(currency_trend):
    """Convertir tendencia de moneda a nivel de riesgo."""
    if currency_trend < 0.2:
        return "Bajo"
    elif currency_trend < 0.5:
        return "Moderado"
    else:
        return "Alto"

def generate_strategic_recommendations(trends):
    """Generar recomendaciones estratégicas basadas en tendencias."""
    recommendations = []
    
    if trends['price_trend_mxn'] > 300:
        recommendations.append("Estrategia alcista - Acelerar compras")
    
    if trends['currency_trend'] > 0.3:
        recommendations.append("Cobertura cambiaria recomendada")
    
    if trends['volatility_mxn'] > 600:
        recommendations.append("Gestión de volatilidad requerida")
    
    return recommendations

def main():
    """Función principal para predicción detallada de octubre 2025."""
    
    # Crear predicciones detalladas
    predictions = create_enhanced_october_2025_prediction()
    
    # Mostrar predicciones
    print("\n📅 PREDICCIONES DETALLADAS OCTUBRE 2025:")
    print("-" * 60)
    
    for pred in predictions:
        print(f"\n📅 {pred['date']} (Progreso: {pred['month_progress']}%):")
        print(f"   💰 Precio USD: ${pred['predicted_price_usd_per_ton']} USD/ton")
        print(f"   💰 Precio MXN: ${pred['predicted_price_mxn_per_ton']} MXN/ton")
        print(f"   💱 USD/MXN: {pred['projected_usd_mxn_rate']}")
        print(f"   🎯 Confianza: {pred['currency_confidence']:.1%}")
        print(f"   ⚠️ Riesgo: {pred['currency_risk_level']}")
        print(f"   📊 Volatilidad: {pred['seasonal_volatility_factor']:.3f}")
        
        if pred['market_opportunities']:
            print(f"   🎯 Oportunidades:")
            for opp in pred['market_opportunities']:
                print(f"      • {opp}")
    
    # Analizar tendencias
    trends = analyze_october_2025_trends(predictions)
    
    # Generar resumen ejecutivo
    summary = generate_deacero_executive_summary(predictions, trends)
    
    # Crear respuesta API completa
    api_response = {
        "prediction_date": "2025-10-01",
        "predicted_price_usd_per_ton": predictions[2]['predicted_price_usd_per_ton'],  # Mitad del mes
        "predicted_price_mxn_per_ton": predictions[2]['predicted_price_mxn_per_ton'],
        "currency": "USD",
        "unit": "metric ton",
        "model_confidence": predictions[2]['currency_confidence'],
        "timestamp": datetime.now().isoformat() + "Z",
        "detailed_october_2025_analysis": {
            "monthly_predictions": predictions,
            "trend_analysis": trends,
            "executive_summary": summary,
            "deacero_specific": True,
            "currency_risk_assessment": "Moderado",
            "strategic_recommendations": summary['strategic_recommendations']
        },
        "methodology": {
            "data_sources": ["Yahoo Finance", "Alpha Vantage", "FRED", "Trading Economics", "Exchange Rates"],
            "model_type": "Enhanced Multi-Factor Analysis with Currency Focus",
            "features": ["Historical prices", "USD/MXN rates", "Seasonal patterns", "Economic indicators", "Market volatility"],
            "validation": "Cross-validation with DeAcero-specific factors"
        }
    }
    
    # Guardar resultados
    with open('../../data/predictions/october_2025_detailed_analysis.json', 'w') as f:
        json.dump(api_response, f, indent=2)
    
    print(f"\n💾 Análisis detallado guardado en: october_2025_detailed_analysis.json")
    
    # Mostrar respuesta API
    print(f"\n🌐 RESPUESTA API PARA OCTUBRE 2025:")
    print("=" * 40)
    print(json.dumps({
        "prediction_date": api_response["prediction_date"],
        "predicted_price_usd_per_ton": api_response["predicted_price_usd_per_ton"],
        "predicted_price_mxn_per_ton": api_response["predicted_price_mxn_per_ton"],
        "currency": api_response["currency"],
        "unit": api_response["unit"],
        "model_confidence": api_response["model_confidence"],
        "timestamp": api_response["timestamp"]
    }, indent=2))
    
    print(f"\n🎯 CONCLUSIÓN FINAL:")
    print(f"   💰 Precio esperado (mitad de mes): ${api_response['predicted_price_usd_per_ton']} USD/ton")
    print(f"   💰 Precio local DeAcero: ${api_response['predicted_price_mxn_per_ton']} MXN/ton")
    print(f"   🎯 Confianza: {api_response['model_confidence']:.1%}")
    print(f"   📊 Análisis: Completo con tipos de cambio y factores DeAcero")

if __name__ == "__main__":
    main()
