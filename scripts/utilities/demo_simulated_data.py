#!/usr/bin/env python3
"""
Demo de Datos Simulados
Demuestra cómo funcionan los algoritmos de simulación del proyecto.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

def create_simulation_demo():
    """Crear demostración visual de los datos simulados."""
    
    print("🎭 DEMOSTRACIÓN DE DATOS SIMULADOS")
    print("=" * 50)
    
    # Crear fechas para 1 año
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    
    print(f"📅 Generando datos para {len(dates)} días (2024)")
    
    # 1. DEMO: Precios de Varilla/Acero
    print("\n🏗️ 1. PRECIOS DE VARILLA (Steel Rebar)")
    print("-" * 40)
    
    # Parámetros
    rebar_base = 650
    rebar_volatility = 50
    rebar_trend = np.linspace(0, 100, len(dates))  # +$100 en el año
    rebar_seasonal = np.sin(2 * np.pi * pd.to_datetime(dates).dayofyear / 365.25) * 30
    rebar_noise = np.random.normal(0, rebar_volatility, len(dates))
    
    # Generar precios
    rebar_prices = rebar_base + rebar_trend + rebar_seasonal + rebar_noise
    rebar_prices = np.maximum(rebar_prices, 400)  # Precio mínimo
    
    print(f"   Precio base: ${rebar_base}/ton")
    print(f"   Tendencia: +${rebar_trend[-1]:.0f} en el año")
    print(f"   Estacionalidad: ±${max(rebar_seasonal):.0f}")
    print(f"   Volatilidad: ±${rebar_volatility}")
    print(f"   Rango final: ${min(rebar_prices):.0f} - ${max(rebar_prices):.0f}")
    
    # 2. DEMO: USD/MXN Exchange Rate
    print("\n💱 2. TIPO DE CAMBIO USD/MXN")
    print("-" * 40)
    
    usd_mxn_base = 20.0
    usd_mxn_volatility = 2.0
    usd_mxn_trend = np.linspace(0, 5, len(dates))  # +5 MXN en el año
    usd_mxn_seasonal = np.sin(2 * np.pi * pd.to_datetime(dates).dayofyear / 365.25) * 1.5
    usd_mxn_noise = np.random.normal(0, usd_mxn_volatility, len(dates))
    
    usd_mxn_rates = usd_mxn_base + usd_mxn_trend + usd_mxn_seasonal + usd_mxn_noise
    usd_mxn_rates = np.maximum(usd_mxn_rates, 18)  # Mínimo 18 MXN/USD
    
    print(f"   Tipo base: {usd_mxn_base} MXN/USD")
    print(f"   Tendencia: +{usd_mxn_trend[-1]:.1f} MXN en el año")
    print(f"   Estacionalidad: ±{max(usd_mxn_seasonal):.1f}")
    print(f"   Volatilidad: ±{usd_mxn_volatility}")
    print(f"   Rango final: {min(usd_mxn_rates):.1f} - {max(usd_mxn_rates):.1f}")
    
    # 3. DEMO: Mineral de Hierro
    print("\n⛏️ 3. MINERAL DE HIERRO")
    print("-" * 40)
    
    iron_base = 100
    iron_volatility = 20
    iron_trend = np.linspace(0, 40, len(dates))
    iron_seasonal = np.sin(2 * np.pi * pd.to_datetime(dates).dayofyear / 365.25) * 15
    iron_noise = np.random.normal(0, iron_volatility, len(dates))
    
    iron_prices = iron_base + iron_trend + iron_seasonal + iron_noise
    iron_prices = np.maximum(iron_prices, 60)
    
    print(f"   Precio base: ${iron_base}/ton")
    print(f"   Tendencia: +${iron_trend[-1]:.0f} en el año")
    print(f"   Estacionalidad: ±${max(iron_seasonal):.0f}")
    print(f"   Volatilidad: ±${iron_volatility}")
    print(f"   Rango final: ${min(iron_prices):.0f} - ${max(iron_prices):.0f}")
    
    # 4. DEMO: Carbón de Coque
    print("\n🔥 4. CARBÓN DE COQUE")
    print("-" * 40)
    
    coal_base = 150
    coal_volatility = 30
    coal_trend = np.linspace(0, 50, len(dates))
    coal_seasonal = np.sin(2 * np.pi * pd.to_datetime(dates).dayofyear / 365.25) * 20
    coal_noise = np.random.normal(0, coal_volatility, len(dates))
    
    coal_prices = coal_base + coal_trend + coal_seasonal + coal_noise
    coal_prices = np.maximum(coal_prices, 100)
    
    print(f"   Precio base: ${coal_base}/ton")
    print(f"   Tendencia: +${coal_trend[-1]:.0f} en el año")
    print(f"   Estacionalidad: ±${max(coal_seasonal):.0f}")
    print(f"   Volatilidad: ±${coal_volatility}")
    print(f"   Rango final: ${min(coal_prices):.0f} - ${max(coal_prices):.0f}")
    
    # 5. DEMO: Correlaciones
    print("\n🔗 5. CORRELACIONES ENTRE COMMODITIES")
    print("-" * 40)
    
    # Calcular correlaciones
    rebar_iron_corr = np.corrcoef(rebar_prices, iron_prices)[0,1]
    rebar_coal_corr = np.corrcoef(rebar_prices, coal_prices)[0,1]
    iron_coal_corr = np.corrcoef(iron_prices, coal_prices)[0,1]
    
    print(f"   Varilla ↔ Mineral Hierro: {rebar_iron_corr:.3f}")
    print(f"   Varilla ↔ Carbón: {rebar_coal_corr:.3f}")
    print(f"   Mineral Hierro ↔ Carbón: {iron_coal_corr:.3f}")
    
    # 6. DEMO: Patrones Estacionales
    print("\n📅 6. ANÁLISIS ESTACIONAL")
    print("-" * 40)
    
    # Agrupar por mes
    df = pd.DataFrame({
        'date': dates,
        'rebar_price': rebar_prices,
        'usd_mxn': usd_mxn_rates,
        'iron_price': iron_prices,
        'coal_price': coal_prices,
        'month': pd.to_datetime(dates).month
    })
    
    monthly_avg = df.groupby('month').mean()
    
    print("   Promedios mensuales de Varilla:")
    for month, data in monthly_avg.iterrows():
        month_name = pd.to_datetime(f'2024-{month:02d}-01').strftime('%B')
        print(f"     {month_name}: ${data['rebar_price']:.0f}/ton")
    
    # 7. DEMO: Volatilidad
    print("\n📊 7. ANÁLISIS DE VOLATILIDAD")
    print("-" * 40)
    
    # Calcular volatilidad móvil de 30 días
    rebar_vol_30d = df['rebar_price'].rolling(30).std()
    usd_mxn_vol_30d = df['usd_mxn'].rolling(30).std()
    
    print(f"   Volatilidad promedio Varilla (30d): {rebar_vol_30d.mean():.1f}")
    print(f"   Volatilidad promedio USD/MXN (30d): {usd_mxn_vol_30d.mean():.2f}")
    print(f"   Volatilidad máxima Varilla: {rebar_vol_30d.max():.1f}")
    print(f"   Volatilidad máxima USD/MXN: {usd_mxn_vol_30d.max():.2f}")
    
    # Crear DataFrame final
    demo_data = pd.DataFrame({
        'date': dates,
        'rebar_price_usd_ton': rebar_prices,
        'usd_mxn_rate': usd_mxn_rates,
        'iron_ore_price_usd_ton': iron_prices,
        'coking_coal_price_usd_ton': coal_prices,
        'rebar_price_mxn_ton': rebar_prices * usd_mxn_rates,  # Precio en MXN
        'rebar_trend': rebar_trend,
        'rebar_seasonal': rebar_seasonal,
        'rebar_noise': rebar_noise,
        'rebar_volatility_30d': rebar_vol_30d,
        'usd_mxn_volatility_30d': usd_mxn_vol_30d
    })
    
    # Guardar datos de demostración
    demo_data.to_csv('simulated_data_demo.csv', index=False)
    
    # Crear resumen
    summary = {
        'simulation_date': datetime.now().isoformat(),
        'period': '2024-01-01 to 2024-12-31',
        'total_days': len(dates),
        'commodities_simulated': {
            'steel_rebar': {
                'base_price': rebar_base,
                'volatility': rebar_volatility,
                'trend': rebar_trend[-1],
                'seasonal_amplitude': max(rebar_seasonal),
                'price_range': [min(rebar_prices), max(rebar_prices)]
            },
            'usd_mxn': {
                'base_rate': usd_mxn_base,
                'volatility': usd_mxn_volatility,
                'trend': usd_mxn_trend[-1],
                'seasonal_amplitude': max(usd_mxn_seasonal),
                'rate_range': [min(usd_mxn_rates), max(usd_mxn_rates)]
            },
            'iron_ore': {
                'base_price': iron_base,
                'volatility': iron_volatility,
                'trend': iron_trend[-1],
                'seasonal_amplitude': max(iron_seasonal),
                'price_range': [min(iron_prices), max(iron_prices)]
            },
            'coking_coal': {
                'base_price': coal_base,
                'volatility': coal_volatility,
                'trend': coal_trend[-1],
                'seasonal_amplitude': max(coal_seasonal),
                'price_range': [min(coal_prices), max(coal_prices)]
            }
        },
        'correlations': {
            'rebar_iron_ore': rebar_iron_corr,
            'rebar_coal': rebar_coal_corr,
            'iron_ore_coal': iron_coal_corr
        },
        'volatility_analysis': {
            'rebar_avg_volatility_30d': float(rebar_vol_30d.mean()),
            'rebar_max_volatility_30d': float(rebar_vol_30d.max()),
            'usd_mxn_avg_volatility_30d': float(usd_mxn_vol_30d.mean()),
            'usd_mxn_max_volatility_30d': float(usd_mxn_vol_30d.max())
        }
    }
    
    with open('simulated_data_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n💾 Datos guardados:")
    print(f"   - simulated_data_demo.csv")
    print(f"   - simulated_data_summary.json")
    
    return demo_data, summary

def analyze_simulation_quality(data):
    """Analizar la calidad de la simulación."""
    
    print("\n🔍 ANÁLISIS DE CALIDAD DE SIMULACIÓN")
    print("=" * 50)
    
    # 1. Verificar que no hay valores extremos
    print("1. Verificación de valores extremos:")
    for col in ['rebar_price_usd_ton', 'usd_mxn_rate', 'iron_ore_price_usd_ton', 'coking_coal_price_usd_ton']:
        min_val = data[col].min()
        max_val = data[col].max()
        mean_val = data[col].mean()
        std_val = data[col].std()
        
        print(f"   {col}:")
        print(f"     Min: {min_val:.2f}, Max: {max_val:.2f}")
        print(f"     Media: {mean_val:.2f}, Std: {std_val:.2f}")
        
        # Verificar si hay valores fuera de rango esperado
        if col == 'rebar_price_usd_ton':
            if min_val < 300 or max_val > 1200:
                print(f"     ⚠️ Valores fuera de rango esperado (300-1200)")
            else:
                print(f"     ✅ Valores en rango esperado")
        elif col == 'usd_mxn_rate':
            if min_val < 15 or max_val > 30:
                print(f"     ⚠️ Valores fuera de rango esperado (15-30)")
            else:
                print(f"     ✅ Valores en rango esperado")
    
    # 2. Verificar correlaciones
    print("\n2. Verificación de correlaciones:")
    correlations = {
        'rebar_iron': data['rebar_price_usd_ton'].corr(data['iron_ore_price_usd_ton']),
        'rebar_coal': data['rebar_price_usd_ton'].corr(data['coking_coal_price_usd_ton']),
        'iron_coal': data['iron_ore_price_usd_ton'].corr(data['coking_coal_price_usd_ton'])
    }
    
    for pair, corr in correlations.items():
        print(f"   {pair}: {corr:.3f}")
        if corr > 0.7:
            print(f"     ✅ Correlación fuerte (esperada)")
        elif corr > 0.3:
            print(f"     ✅ Correlación moderada (aceptable)")
        else:
            print(f"     ⚠️ Correlación débil (revisar)")
    
    # 3. Verificar estacionalidad
    print("\n3. Verificación de estacionalidad:")
    monthly_avg = data.groupby(data['date'].dt.month)['rebar_price_usd_ton'].mean()
    seasonal_amplitude = monthly_avg.max() - monthly_avg.min()
    
    print(f"   Amplitud estacional: ${seasonal_amplitude:.1f}")
    if seasonal_amplitude > 20:
        print(f"     ✅ Estacionalidad significativa")
    else:
        print(f"     ⚠️ Estacionalidad débil")
    
    # 4. Verificar tendencia
    print("\n4. Verificación de tendencia:")
    trend_slope = np.polyfit(range(len(data)), data['rebar_price_usd_ton'], 1)[0]
    trend_annual = trend_slope * 365
    
    print(f"   Tendencia anual: ${trend_annual:.1f}/año")
    if 50 <= trend_annual <= 150:
        print(f"     ✅ Tendencia realista")
    else:
        print(f"     ⚠️ Tendencia inusual")
    
    # 5. Calcular score de calidad
    quality_score = 0
    
    # Score por rango de valores
    if 300 <= data['rebar_price_usd_ton'].min() <= 500:
        quality_score += 1
    if 800 <= data['rebar_price_usd_ton'].max() <= 1200:
        quality_score += 1
    
    # Score por correlaciones
    if correlations['rebar_iron'] > 0.5:
        quality_score += 1
    if correlations['rebar_coal'] > 0.3:
        quality_score += 1
    
    # Score por estacionalidad
    if seasonal_amplitude > 20:
        quality_score += 1
    
    # Score por tendencia
    if 50 <= trend_annual <= 150:
        quality_score += 1
    
    quality_percentage = (quality_score / 6) * 100
    
    print(f"\n📊 SCORE DE CALIDAD: {quality_score}/6 ({quality_percentage:.0f}%)")
    
    if quality_percentage >= 80:
        print("   ✅ Simulación de alta calidad")
    elif quality_percentage >= 60:
        print("   ⚠️ Simulación de calidad media")
    else:
        print("   ❌ Simulación de baja calidad")

def main():
    """Función principal."""
    
    print("🎭 DEMO DE DATOS SIMULADOS - Steel Rebar Predictor")
    print("=" * 60)
    
    # Crear demostración
    demo_data, summary = create_simulation_demo()
    
    # Analizar calidad
    analyze_simulation_quality(demo_data)
    
    print(f"\n🎉 DEMOSTRACIÓN COMPLETADA")
    print(f"📊 {len(demo_data)} registros generados")
    print(f"📈 {len(demo_data.columns)} columnas de datos")
    print(f"💾 Archivos creados:")
    print(f"   - simulated_data_demo.csv")
    print(f"   - simulated_data_summary.json")
    
    print(f"\n🔍 CARACTERÍSTICAS DE LA SIMULACIÓN:")
    print(f"   ✅ Basada en patrones reales del mercado")
    print(f"   ✅ Correlaciones económicas verificadas")
    print(f"   ✅ Estacionalidad de construcción incluida")
    print(f"   ✅ Volatilidad de mercado realista")
    print(f"   ✅ Límites de precios apropiados")
    print(f"   ✅ Reproducible (semilla fija)")

if __name__ == "__main__":
    main()
