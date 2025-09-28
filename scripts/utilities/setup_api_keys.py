#!/usr/bin/env python3
"""
Configurador de API Keys Gratuitas
Guía paso a paso para obtener y configurar API keys gratuitas.
"""

import os
import requests
import json
from datetime import datetime

def setup_api_keys():
    """Configurar API keys paso a paso."""
    
    print("🔑 CONFIGURACIÓN DE API KEYS GRATUITAS")
    print("=" * 50)
    
    # Verificar archivo .env existente
    env_file = ".env"
    env_exists = os.path.exists(env_file)
    
    if env_exists:
        print(f"✅ Archivo {env_file} encontrado")
        with open(env_file, 'r') as f:
            content = f.read()
            
        # Verificar keys existentes
        fred_configured = "FRED_API_KEY=" in content and "your_fred_api_key_here" not in content
        av_configured = "ALPHA_VANTAGE_API_KEY=" in content and "your_alpha_vantage_api_key_here" not in content
        
        print(f"🔍 FRED API Key: {'✅ Configurada' if fred_configured else '❌ No configurada'}")
        print(f"🔍 Alpha Vantage API Key: {'✅ Configurada' if av_configured else '❌ No configurada'}")
        
        if fred_configured and av_configured:
            print("\n🎉 ¡Todas las API keys están configuradas!")
            return True
    
    print("\n📋 PASOS PARA OBTENER API KEYS GRATUITAS:")
    print("-" * 50)
    
    # FRED API
    print("\n1️⃣ FRED API (Federal Reserve Economic Data)")
    print("   🌐 URL: https://fred.stlouisfed.org/docs/api/api_key.html")
    print("   📧 Registro: Gratuito, solo email")
    print("   ⏱️ Tiempo: 2-3 minutos")
    print("   📊 Datos: USD/MXN, tasas de interés, indicadores económicos")
    
    # Alpha Vantage API
    print("\n2️⃣ Alpha Vantage API")
    print("   🌐 URL: https://www.alphavantage.co/support/#api-key")
    print("   📧 Registro: Gratuito, solo email")
    print("   ⏱️ Tiempo: 1-2 minutos")
    print("   📊 Datos: Commodities, FX rates, stock prices")
    print("   ⚠️ Limitación: 25 requests/día en plan gratuito")
    
    # Crear archivo .env si no existe
    if not env_exists:
        print(f"\n📝 Creando archivo {env_file}...")
        env_content = """# API Keys para Fuentes de Datos Externas
# Reemplaza los valores 'your_xxx_api_key_here' con tus API keys reales

# FRED API Key (Federal Reserve Economic Data)
# Registro gratuito en: https://fred.stlouisfed.org/docs/api/api_key.html
FRED_API_KEY=your_fred_api_key_here

# Alpha Vantage API Key
# Registro gratuito en: https://www.alphavantage.co/support/#api-key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key_here

# Configuración de la aplicación
API_KEY=deacero_steel_predictor_2025_key
REDIS_URL=redis://localhost:6379

# Configuración de GCP (opcional)
GOOGLE_CLOUD_PROJECT=your_project_id
"""
        
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print(f"✅ Archivo {env_file} creado")
    
    print(f"\n🔧 INSTRUCCIONES DE CONFIGURACIÓN:")
    print("-" * 50)
    print(f"1. Edita el archivo {env_file}")
    print(f"2. Reemplaza 'your_fred_api_key_here' con tu FRED API key")
    print(f"3. Reemplaza 'your_alpha_vantage_api_key_here' con tu Alpha Vantage API key")
    print(f"4. Guarda el archivo")
    print(f"5. Ejecuta: python scripts/utilities/configure_real_data_sources.py")
    
    return False

def test_configured_keys():
    """Probar las API keys configuradas."""
    print("\n🧪 PROBANDO API KEYS CONFIGURADAS...")
    print("-" * 50)
    
    # Leer variables de entorno
    fred_key = os.getenv('FRED_API_KEY', '')
    av_key = os.getenv('ALPHA_VANTAGE_API_KEY', '')
    
    if not fred_key or fred_key == 'your_fred_api_key_here':
        print("❌ FRED API key no configurada")
    else:
        print("✅ FRED API key configurada")
        
        # Probar FRED API
        try:
            url = "https://api.stlouisfed.org/fred/series/observations"
            params = {
                'series_id': 'DEXMXUS',  # USD/MXN Exchange Rate
                'api_key': fred_key,
                'file_type': 'json',
                'limit': 1,
                'sort_order': 'desc'
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'observations' in data and data['observations']:
                    latest = data['observations'][0]
                    print(f"   📊 USD/MXN más reciente: {latest.get('value')} ({latest.get('date')})")
                else:
                    print("   ⚠️ No se encontraron datos")
            else:
                print(f"   ❌ Error HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    if not av_key or av_key == 'your_alpha_vantage_api_key_here':
        print("❌ Alpha Vantage API key no configurada")
    else:
        print("✅ Alpha Vantage API key configurada")
        
        # Probar Alpha Vantage API
        try:
            url = "https://www.alphavantage.co/query"
            params = {
                'function': 'TIME_SERIES_INTRADAY',
                'symbol': 'IBM',
                'interval': '5min',
                'apikey': av_key,
                'datatype': 'json'
            }
            
            response = requests.get(url, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if 'Error Message' in data:
                    print(f"   ❌ Error: {data['Error Message']}")
                elif 'Note' in data:
                    print(f"   ⚠️ Rate limited: {data['Note']}")
                elif 'Time Series (5min)' in data:
                    print("   ✅ API funcionando correctamente")
                else:
                    print("   ⚠️ Respuesta inesperada")
            else:
                print(f"   ❌ Error HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

def create_env_from_template():
    """Crear archivo .env desde template si no existe."""
    if not os.path.exists('.env'):
        if os.path.exists('.env.template'):
            print("📋 Copiando .env.template a .env...")
            with open('.env.template', 'r') as f:
                content = f.read()
            
            with open('.env', 'w') as f:
                f.write(content)
            
            print("✅ Archivo .env creado desde template")
        else:
            print("❌ No se encontró .env.template")
            return False
    
    return True

def main():
    """Función principal."""
    print("🚀 CONFIGURADOR DE API KEYS PARA FUENTES DE DATOS REALES")
    print("=" * 60)
    
    # Crear .env si no existe
    if not create_env_from_template():
        return
    
    # Configurar API keys
    keys_configured = setup_api_keys()
    
    if keys_configured:
        # Probar keys configuradas
        test_configured_keys()
        
        print("\n🎉 ¡CONFIGURACIÓN COMPLETADA!")
        print("Ahora puedes usar la API con datos reales:")
        print("python app_main_with_real_data.py")
    else:
        print("\n📝 SIGUIENTES PASOS:")
        print("1. Obtén tus API keys gratuitas")
        print("2. Configúralas en el archivo .env")
        print("3. Ejecuta este script nuevamente para probar")

if __name__ == "__main__":
    main()
