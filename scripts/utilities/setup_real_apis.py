#!/usr/bin/env python3
"""
Setup Real APIs - Configure free API keys and test connectivity
Phase 1 of the correction plan: Transition to real data sources only
"""

import os
import requests
import json
from datetime import datetime
import time

def setup_fred_api():
    """Setup FRED API configuration."""
    print("🏛️ CONFIGURANDO FRED API")
    print("=" * 40)
    
    print("📝 INSTRUCCIONES PARA FRED API:")
    print("1. Ve a: https://fred.stlouisfed.org/docs/api/api_key.html")
    print("2. Registra una cuenta gratuita")
    print("3. Genera tu API key gratuita")
    print("4. Copia la API key")
    print("")
    
    api_key = input("🔑 Ingresa tu FRED API key (o presiona Enter para omitir): ").strip()
    
    if api_key:
        # Test the API key
        print("🧪 Probando FRED API...")
        try:
            url = f"https://api.stlouisfed.org/fred/series?series_id=GDP&api_key={api_key}&file_type=json"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print("✅ FRED API funcionando correctamente")
                
                # Save to .env file
                env_content = ""
                env_file = ".env"
                
                if os.path.exists(env_file):
                    with open(env_file, 'r') as f:
                        env_content = f.read()
                
                if "FRED_API_KEY" not in env_content:
                    with open(env_file, 'a') as f:
                        f.write(f"\nFRED_API_KEY={api_key}\n")
                    print("💾 FRED API key guardada en .env")
                else:
                    print("⚠️ FRED API key ya existe en .env")
                
                return True
            else:
                print(f"❌ FRED API error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ FRED API error: {e}")
            return False
    else:
        print("⚠️ FRED API omitida - se usará fallback")
        return False

def setup_quandl_api():
    """Setup Quandl API configuration."""
    print("\n📈 CONFIGURANDO QUANDL API")
    print("=" * 40)
    
    print("📝 INSTRUCCIONES PARA QUANDL API:")
    print("1. Ve a: https://data.nasdaq.com/")
    print("2. Registra una cuenta gratuita")
    print("3. Ve a tu perfil y genera API key")
    print("4. Plan gratuito: 50 requests/día")
    print("")
    
    api_key = input("🔑 Ingresa tu Quandl API key (o presiona Enter para omitir): ").strip()
    
    if api_key:
        # Test the API key
        print("🧪 Probando Quandl API...")
        try:
            url = f"https://data.nasdaq.com/api/v3/datasets/LBMA/GOLD.json?api_key={api_key}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print("✅ Quandl API funcionando correctamente")
                
                # Save to .env file
                env_content = ""
                env_file = ".env"
                
                if os.path.exists(env_file):
                    with open(env_file, 'r') as f:
                        env_content = f.read()
                
                if "QUANDL_API_KEY" not in env_content:
                    with open(env_file, 'a') as f:
                        f.write(f"\nQUANDL_API_KEY={api_key}\n")
                    print("💾 Quandl API key guardada en .env")
                else:
                    print("⚠️ Quandl API key ya existe en .env")
                
                return True
            else:
                print(f"❌ Quandl API error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Quandl API error: {e}")
            return False
    else:
        print("⚠️ Quandl API omitida - se usará fallback")
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
                print("📊 Datos de USD/MXN disponibles")
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
        response = requests.get(url, timeout=10)
        
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

def create_env_template():
    """Create .env.template file with all API configurations."""
    print("\n📝 CREANDO ARCHIVO .env.template")
    print("=" * 40)
    
    template_content = """# Steel Rebar Predictor - Real Data Sources Configuration
# Copy this file to .env and fill in your API keys

# API Keys for Real Data Sources
FRED_API_KEY=your_fred_api_key_here
QUANDL_API_KEY=your_quandl_api_key_here

# Existing Configuration
API_KEY=deacero_steel_predictor_2025_key
REDIS_URL=redis://localhost:6379

# Instructions:
# 1. FRED API: https://fred.stlouisfed.org/docs/api/api_key.html (FREE)
# 2. Quandl API: https://data.nasdaq.com/ (FREE - 50 requests/day)
# 3. World Bank API: No key required
# 4. Banco de México API: No key required  
# 5. INEGI API: No key required
"""
    
    with open('.env.template', 'w') as f:
        f.write(template_content)
    
    print("✅ Archivo .env.template creado")
    print("📋 Instrucciones incluidas para obtener API keys gratuitas")

def main():
    """Main setup function."""
    print("🚀 CONFIGURACIÓN DE APIS REALES - FASE 1")
    print("=" * 60)
    print("Objetivo: Configurar fuentes de datos reales gratuitas")
    print("Fecha:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 60)
    
    results = {
        'fred_api': False,
        'quandl_api': False,
        'world_bank_api': False,
        'banxico_api': False,
        'inegi_api': False
    }
    
    # Setup APIs that require keys
    results['fred_api'] = setup_fred_api()
    results['quandl_api'] = setup_quandl_api()
    
    # Test APIs that don't require keys
    results['world_bank_api'] = test_world_bank_api()
    results['banxico_api'] = test_banxico_api()
    results['inegi_api'] = test_inegi_api()
    
    # Create template file
    create_env_template()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE CONFIGURACIÓN")
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
    
    print(f"\n📈 APIS FUNCIONANDO: {len(working_apis)}/5")
    print(f"📉 APIS FALLIDAS: {len(failed_apis)}/5")
    
    if len(working_apis) >= 3:
        print("\n🎉 SUFICIENTES APIS DISPONIBLES")
        print("✅ Puedes proceder con la implementación de collectors")
    else:
        print("\n⚠️ POCAS APIS DISPONIBLES")
        print("📋 Considera configurar más API keys o usar fallbacks")
    
    # Save results
    with open('api_setup_results.json', 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'results': results,
            'working_apis': working_apis,
            'failed_apis': failed_apis,
            'total_working': len(working_apis),
            'total_failed': len(failed_apis)
        }, f, indent=2)
    
    print(f"\n💾 Resultados guardados en: api_setup_results.json")
    
    return results

if __name__ == "__main__":
    main()
