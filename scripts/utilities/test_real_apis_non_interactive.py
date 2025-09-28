#!/usr/bin/env python3
"""
Test Real APIs - Non-interactive version
Test APIs that don't require keys and check existing configuration
"""

import os
import requests
import json
from datetime import datetime
import time

def test_existing_apis():
    """Test existing API configurations."""
    print("🔍 VERIFICANDO CONFIGURACIÓN EXISTENTE")
    print("=" * 50)
    
    env_file = ".env"
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            content = f.read()
        
        print("📋 APIs configuradas en .env:")
        if "FRED_API_KEY" in content:
            print("✅ FRED_API_KEY: Configurada")
        else:
            print("❌ FRED_API_KEY: No configurada")
            
        if "QUANDL_API_KEY" in content:
            print("✅ QUANDL_API_KEY: Configurada")
        else:
            print("❌ QUANDL_API_KEY: No configurada")
    else:
        print("❌ Archivo .env no encontrado")

def test_fred_api():
    """Test FRED API if key is available."""
    print("\n🏛️ PROBANDO FRED API")
    print("=" * 40)
    
    # Check if API key exists in environment
    fred_key = os.getenv('FRED_API_KEY')
    
    if not fred_key:
        print("⚠️ FRED_API_KEY no encontrada en variables de entorno")
        print("📝 Para configurar: export FRED_API_KEY=your_key")
        return False
    
    try:
        # Test with GDP series (always available)
        url = f"https://api.stlouisfed.org/fred/series?series_id=GDP&api_key={fred_key}&file_type=json"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'seriess' in data and len(data['seriess']) > 0:
                print("✅ FRED API funcionando correctamente")
                print(f"📊 Series disponibles: {len(data['seriess'])}")
                return True
            else:
                print("❌ FRED API responde pero sin datos")
                return False
        else:
            print(f"❌ FRED API error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ FRED API error: {e}")
        return False

def test_world_bank_api():
    """Test World Bank API (no key required)."""
    print("\n🌍 PROBANDO WORLD BANK API")
    print("=" * 40)
    
    try:
        # Test World Bank API - Steel prices
        url = "https://api.worldbank.org/v2/country/all/indicator/PINKST.MTX?format=json&per_page=10"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if len(data) > 1 and len(data[1]) > 0:
                print("✅ World Bank API funcionando correctamente")
                print(f"📊 Datos de acero disponibles: {len(data[1])} registros")
                
                # Show sample data
                sample = data[1][0]
                print(f"📈 Ejemplo: {sample.get('country', {}).get('value', 'N/A')} - {sample.get('date', 'N/A')}")
                return True
            else:
                print("⚠️ World Bank API responde pero sin datos de acero")
                return False
        else:
            print(f"❌ World Bank API error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ World Bank API error: {e}")
        return False

def test_banxico_api():
    """Test Banco de México API (no key required)."""
    print("\n🇲🇽 PROBANDO BANCO DE MÉXICO API")
    print("=" * 40)
    
    try:
        # Test Banxico API - USD/MXN rate
        url = "https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno"
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'Steel-Rebar-Predictor/1.0'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'bmx' in data and 'series' in data['bmx']:
                print("✅ Banco de México API funcionando correctamente")
                series = data['bmx']['series']
                if series and len(series) > 0:
                    print("📊 Datos de USD/MXN disponibles")
                    # Show latest rate
                    latest = series[0].get('datos', [])
                    if latest and len(latest) > 0:
                        rate = latest[0].get('dato', 'N/A')
                        date = latest[0].get('fecha', 'N/A')
                        print(f"💱 Última tasa USD/MXN: {rate} ({date})")
                return True
            else:
                print("⚠️ Banco de México API responde pero sin datos esperados")
                return False
        else:
            print(f"❌ Banco de México API error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Banco de México API error: {e}")
        return False

def test_inegi_api():
    """Test INEGI API (no key required)."""
    print("\n📊 PROBANDO INEGI API")
    print("=" * 40)
    
    try:
        # Test INEGI API - Economic indicators
        url = "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000001/es/0700/false/BIE/2.0/"
        headers = {
            'User-Agent': 'Steel-Rebar-Predictor/1.0'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ INEGI API funcionando correctamente")
            print("📊 Indicadores económicos disponibles")
            return True
        else:
            print(f"❌ INEGI API error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ INEGI API error: {e}")
        return False

def test_yahoo_finance():
    """Test Yahoo Finance (already working)."""
    print("\n📈 PROBANDO YAHOO FINANCE")
    print("=" * 40)
    
    try:
        # Test Yahoo Finance with a simple request
        import yfinance as yf
        
        # Test USD/MXN rate
        ticker = yf.Ticker("USDMXN=X")
        data = ticker.history(period="1d")
        
        if not data.empty:
            print("✅ Yahoo Finance funcionando correctamente")
            latest_price = data['Close'].iloc[-1]
            print(f"💱 USD/MXN actual: {latest_price:.2f}")
            return True
        else:
            print("⚠️ Yahoo Finance responde pero sin datos")
            return False
            
    except Exception as e:
        print(f"❌ Yahoo Finance error: {e}")
        return False

def test_alpha_vantage():
    """Test Alpha Vantage (already working)."""
    print("\n🔮 PROBANDO ALPHA VANTAGE")
    print("=" * 40)
    
    try:
        # Test Alpha Vantage with a simple request
        import requests
        
        # Use a simple endpoint that doesn't require specific symbols
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'Time Series (Daily)' in data:
                print("✅ Alpha Vantage funcionando correctamente")
                print("📊 Datos de series temporales disponibles")
                return True
            else:
                print("⚠️ Alpha Vantage responde pero sin datos esperados")
                return False
        else:
            print(f"❌ Alpha Vantage error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Alpha Vantage error: {e}")
        return False

def main():
    """Main test function."""
    print("🧪 PRUEBA DE APIS REALES - VERSIÓN NO INTERACTIVA")
    print("=" * 60)
    print("Objetivo: Verificar APIs disponibles sin configuración adicional")
    print("Fecha:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 60)
    
    # Check existing configuration
    test_existing_apis()
    
    results = {}
    
    # Test APIs
    results['fred_api'] = test_fred_api()
    results['world_bank_api'] = test_world_bank_api()
    results['banxico_api'] = test_banxico_api()
    results['inegi_api'] = test_inegi_api()
    results['yahoo_finance'] = test_yahoo_finance()
    results['alpha_vantage'] = test_alpha_vantage()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    working_apis = []
    failed_apis = []
    
    for api, status in results.items():
        if status:
            working_apis.append(api)
            print(f"✅ {api.upper()}: Funcionando")
        else:
            failed_apis.append(api)
            print(f"❌ {api.upper()}: No disponible")
    
    print(f"\n📈 APIS FUNCIONANDO: {len(working_apis)}/6")
    print(f"📉 APIS FALLIDAS: {len(failed_apis)}/6")
    
    if len(working_apis) >= 3:
        print("\n🎉 SUFICIENTES APIS DISPONIBLES")
        print("✅ Puedes proceder con la implementación de collectors")
        print("\n🚀 PRÓXIMOS PASOS:")
        print("1. Implementar collectors para APIs funcionando")
        print("2. Crear fallback strategy")
        print("3. Eliminar datos simulados")
    else:
        print("\n⚠️ POCAS APIS DISPONIBLES")
        print("📋 Considera configurar más API keys")
    
    # Save results
    with open('real_apis_test_results.json', 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'results': results,
            'working_apis': working_apis,
            'failed_apis': failed_apis,
            'total_working': len(working_apis),
            'total_failed': len(failed_apis)
        }, f, indent=2)
    
    print(f"\n💾 Resultados guardados en: real_apis_test_results.json")
    
    return results

if __name__ == "__main__":
    main()
