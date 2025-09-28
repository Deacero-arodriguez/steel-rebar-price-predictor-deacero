#!/usr/bin/env python3
"""
Test Simple de APIs Reales - Versión sin problemas de certificados SSL
"""

import requests
import json
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_apis_with_requests():
    """Probar APIs usando requests directamente (sin yfinance)."""
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "tests_performed": [],
        "successful_tests": [],
        "failed_tests": []
    }
    
    logger.info("🔍 Probando APIs externas con requests...")
    
    # Test 1: FRED API (sin API key para verificar estructura)
    logger.info("\n📊 Probando FRED API...")
    try:
        # Usar endpoint público para verificar conectividad
        url = "https://api.stlouisfed.org/fred/categories"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            logger.info("✅ FRED API: Conectividad OK")
            results["tests_performed"].append("FRED API Connectivity")
            results["successful_tests"].append("FRED API Connectivity")
        else:
            logger.warning(f"⚠️ FRED API: Status {response.status_code}")
            results["failed_tests"].append("FRED API Connectivity")
            
    except Exception as e:
        logger.error(f"❌ FRED API: {e}")
        results["failed_tests"].append("FRED API Connectivity")
    
    # Test 2: Alpha Vantage API (sin API key para verificar estructura)
    logger.info("\n📈 Probando Alpha Vantage API...")
    try:
        url = "https://www.alphavantage.co/query"
        params = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': 'IBM',
            'interval': '5min',
            'apikey': 'demo'  # API key de demostración
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'Note' in data:
                logger.info("✅ Alpha Vantage API: Conectividad OK (rate limited en demo)")
                results["tests_performed"].append("Alpha Vantage API Connectivity")
                results["successful_tests"].append("Alpha Vantage API Connectivity")
            elif 'Time Series (5min)' in data:
                logger.info("✅ Alpha Vantage API: Datos recibidos correctamente")
                results["tests_performed"].append("Alpha Vantage API Data")
                results["successful_tests"].append("Alpha Vantage API Data")
            else:
                logger.warning("⚠️ Alpha Vantage API: Respuesta inesperada")
                results["failed_tests"].append("Alpha Vantage API Data")
        else:
            logger.warning(f"⚠️ Alpha Vantage API: Status {response.status_code}")
            results["failed_tests"].append("Alpha Vantage API Connectivity")
            
    except Exception as e:
        logger.error(f"❌ Alpha Vantage API: {e}")
        results["failed_tests"].append("Alpha Vantage API Connectivity")
    
    # Test 3: Yahoo Finance API (usando endpoint directo)
    logger.info("\n💰 Probando Yahoo Finance (endpoint directo)...")
    try:
        # Usar endpoint público de Yahoo Finance
        url = "https://query1.finance.yahoo.com/v8/finance/chart/USDMXN=X"
        params = {
            'interval': '1d',
            'range': '5d'
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'chart' in data and 'result' in data['chart']:
                logger.info("✅ Yahoo Finance: Datos de USD/MXN recibidos")
                results["tests_performed"].append("Yahoo Finance USD/MXN")
                results["successful_tests"].append("Yahoo Finance USD/MXN")
                
                # Extraer precio actual
                result = data['chart']['result'][0]
                if 'meta' in result:
                    current_price = result['meta'].get('regularMarketPrice', 'N/A')
                    logger.info(f"   Precio actual USD/MXN: {current_price}")
            else:
                logger.warning("⚠️ Yahoo Finance: Estructura de datos inesperada")
                results["failed_tests"].append("Yahoo Finance USD/MXN")
        else:
            logger.warning(f"⚠️ Yahoo Finance: Status {response.status_code}")
            results["failed_tests"].append("Yahoo Finance USD/MXN")
            
    except Exception as e:
        logger.error(f"❌ Yahoo Finance: {e}")
        results["failed_tests"].append("Yahoo Finance USD/MXN")
    
    # Test 4: Commodity API (usando endpoint público)
    logger.info("\n🏭 Probando Commodity API...")
    try:
        # Usar API pública de commodities
        url = "https://api.metals.live/v1/spot"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            logger.info("✅ Commodity API: Datos recibidos")
            results["tests_performed"].append("Commodity API")
            results["successful_tests"].append("Commodity API")
        else:
            logger.warning(f"⚠️ Commodity API: Status {response.status_code}")
            results["failed_tests"].append("Commodity API")
            
    except Exception as e:
        logger.error(f"❌ Commodity API: {e}")
        results["failed_tests"].append("Commodity API")
    
    # Generar reporte
    logger.info("\n" + "=" * 50)
    logger.info("📊 REPORTE DE CONECTIVIDAD")
    logger.info("=" * 50)
    logger.info(f"✅ Tests exitosos: {len(results['successful_tests'])}")
    for test in results['successful_tests']:
        logger.info(f"   - {test}")
    
    logger.info(f"❌ Tests fallidos: {len(results['failed_tests'])}")
    for test in results['failed_tests']:
        logger.info(f"   - {test}")
    
    # Guardar resultados
    with open('api_connectivity_test.json', 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    logger.info(f"\n💾 Resultados guardados en: api_connectivity_test.json")
    
    return results

if __name__ == "__main__":
    test_apis_with_requests()
