#!/usr/bin/env python3
"""
Test de la API con Datos Reales
Prueba la nueva funcionalidad de datos reales sin necesidad de API keys.
"""

import requests
import json
from datetime import datetime
import time

def test_real_data_api():
    """Probar la API con datos reales."""
    
    print("🧪 PROBANDO API CON DATOS REALES")
    print("=" * 50)
    
    # URLs para probar
    base_url = "http://localhost:8080"
    
    # Test 1: Health Check
    print("\n1️⃣ Probando Health Check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check: {data['status']}")
            print(f"   Versión: {data.get('version', 'N/A')}")
            print(f"   Data Sources Status: {data.get('data_sources_status', {})}")
        else:
            print(f"❌ Health Check falló: {response.status_code}")
    except Exception as e:
        print(f"❌ Error en Health Check: {e}")
    
    # Test 2: Market Data (requiere API key)
    print("\n2️⃣ Probando Market Data...")
    try:
        headers = {"X-API-Key": "deacero_steel_predictor_2025_key"}
        response = requests.get(f"{base_url}/market-data", headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Market Data: {data['status']}")
            print(f"   Fuentes utilizadas: {data.get('sources_used', [])}")
            
            market_data = data.get('market_data', {})
            if 'data' in market_data:
                print(f"   Datos disponibles: {list(market_data['data'].keys())}")
                
                # Mostrar USD/MXN si está disponible
                if 'usd_mxn_rate' in market_data['data']:
                    rate = market_data['data']['usd_mxn_rate']
                    print(f"   💱 USD/MXN: {rate}")
        else:
            print(f"❌ Market Data falló: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error en Market Data: {e}")
    
    # Test 3: Prediction (requiere API key)
    print("\n3️⃣ Probando Prediction...")
    try:
        headers = {"X-API-Key": "deacero_steel_predictor_2025_key"}
        response = requests.get(f"{base_url}/predict/steel-rebar-price", headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Prediction exitosa")
            print(f"   📅 Fecha: {data.get('prediction_date')}")
            print(f"   💰 Precio: ${data.get('predicted_price_usd_per_ton')} USD/ton")
            print(f"   📊 Confianza: {data.get('model_confidence')}%")
            print(f"   🔄 Ajuste de precio: {data.get('price_adjustment', 0)}")
            print(f"   📈 Fuentes: {data.get('data_sources_used', [])}")
            
            # Mostrar breakdown de confianza
            confidence_breakdown = data.get('confidence_breakdown', {})
            if confidence_breakdown:
                print(f"   📊 Desglose de confianza:")
                for component, value in confidence_breakdown.items():
                    print(f"      - {component}: {value}%")
        else:
            print(f"❌ Prediction falló: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error en Prediction: {e}")
    
    # Test 4: Sin API Key (debe fallar)
    print("\n4️⃣ Probando sin API Key (debe fallar)...")
    try:
        response = requests.get(f"{base_url}/predict/steel-rebar-price", timeout=10)
        if response.status_code == 401:
            print("✅ Sin API Key: Correctamente rechazado (401)")
        else:
            print(f"⚠️ Sin API Key: Status inesperado {response.status_code}")
    except Exception as e:
        print(f"❌ Error en test sin API Key: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 PRUEBAS COMPLETADAS")

def test_external_apis_directly():
    """Probar APIs externas directamente."""
    
    print("\n🌐 PROBANDO APIs EXTERNAS DIRECTAMENTE")
    print("=" * 50)
    
    # Test Yahoo Finance (endpoint directo)
    print("\n📈 Probando Yahoo Finance...")
    try:
        url = "https://query1.finance.yahoo.com/v8/finance/chart/USDMXN=X"
        params = {'interval': '1d', 'range': '5d'}
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'chart' in data and 'result' in data['chart']:
                result = data['chart']['result'][0]
                meta = result.get('meta', {})
                price = meta.get('regularMarketPrice')
                print(f"✅ Yahoo Finance USD/MXN: ${price}")
            else:
                print("⚠️ Yahoo Finance: Estructura de datos inesperada")
        else:
            print(f"⚠️ Yahoo Finance: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Yahoo Finance: {e}")
    
    # Test Alpha Vantage
    print("\n📊 Probando Alpha Vantage...")
    try:
        url = "https://www.alphavantage.co/query"
        params = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': 'IBM',
            'interval': '5min',
            'apikey': 'demo'
        }
        
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if 'Note' in data:
                print(f"✅ Alpha Vantage: {data['Note']}")
            elif 'Time Series (5min)' in data:
                print("✅ Alpha Vantage: Datos recibidos correctamente")
            else:
                print("⚠️ Alpha Vantage: Respuesta inesperada")
        else:
            print(f"⚠️ Alpha Vantage: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Alpha Vantage: {e}")

def main():
    """Función principal."""
    print("🚀 TEST DE API CON DATOS REALES")
    print("=" * 60)
    
    # Probar APIs externas primero
    test_external_apis_directly()
    
    # Probar API local (si está corriendo)
    print("\n🔍 Verificando si la API está corriendo...")
    try:
        response = requests.get("http://localhost:8080/health", timeout=5)
        if response.status_code == 200:
            print("✅ API local detectada - ejecutando tests completos")
            test_real_data_api()
        else:
            print("⚠️ API local no disponible - solo tests externos")
    except:
        print("❌ API local no está corriendo")
        print("\n💡 Para probar la API local:")
        print("   python app_main_with_real_data.py")
        print("   Luego ejecuta este script nuevamente")

if __name__ == "__main__":
    main()
