#!/usr/bin/env python3
"""
Configurador de Fuentes de Datos Reales
Configura y prueba las APIs externas disponibles para el proyecto.
"""

import os
import sys
import requests
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import json
import logging

# Agregar el directorio raíz al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealDataSourcesConfig:
    """Configurador y probador de fuentes de datos reales."""
    
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "sources_tested": [],
            "successful_sources": [],
            "failed_sources": [],
            "api_keys_status": {}
        }
    
    def test_yahoo_finance(self):
        """Probar Yahoo Finance (gratuita, no requiere API key)."""
        logger.info("🔍 Probando Yahoo Finance...")
        
        try:
            # Probar varios símbolos relevantes
            symbols = {
                'USD_MXN': 'USDMXN=X',
                'Iron_Ore': 'IO=F',
                'Steel_Rebar_Shanghai': 'RB.SHF',
                'Hot_Rolled_Coil': 'HR=F'
            }
            
            yahoo_results = {}
            
            for name, symbol in symbols.items():
                try:
                    ticker = yf.Ticker(symbol)
                    data = ticker.history(period="5d")
                    
                    if not data.empty:
                        latest_price = data['Close'].iloc[-1]
                        yahoo_results[name] = {
                            "symbol": symbol,
                            "latest_price": float(latest_price),
                            "records_count": len(data),
                            "status": "success"
                        }
                        logger.info(f"✅ {name} ({symbol}): ${latest_price:.2f}")
                    else:
                        yahoo_results[name] = {
                            "symbol": symbol,
                            "status": "no_data"
                        }
                        logger.warning(f"⚠️ {name} ({symbol}): Sin datos")
                        
                except Exception as e:
                    yahoo_results[name] = {
                        "symbol": symbol,
                        "status": "error",
                        "error": str(e)
                    }
                    logger.error(f"❌ {name} ({symbol}): {e}")
            
            self.results["sources_tested"].append("Yahoo Finance")
            self.results["successful_sources"].append("Yahoo Finance")
            self.results["yahoo_finance"] = yahoo_results
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error general en Yahoo Finance: {e}")
            self.results["failed_sources"].append("Yahoo Finance")
            return False
    
    def test_fred_api(self, api_key=None):
        """Probar FRED API (requiere API key)."""
        logger.info("🔍 Probando FRED API...")
        
        if not api_key:
            logger.warning("⚠️ FRED API key no configurada - usando datos simulados")
            self.results["api_keys_status"]["FRED"] = "not_configured"
            self.results["sources_tested"].append("FRED (simulado)")
            self.results["fred_simulated"] = {
                "status": "simulated",
                "reason": "API key not configured"
            }
            return False
        
        try:
            # Probar series relevantes para México y commodities
            series_to_test = {
                'USD_MXN': 'DEXMXUS',  # USD/MXN Exchange Rate
                'Mexico_CPI': 'MEXCPIALLMINMEI',  # Mexico Consumer Price Index
                'Mexico_Interest_Rate': 'INTGSBMXM193N',  # Mexico Interest Rate
                'US_Interest_Rate': 'FEDFUNDS'  # US Federal Funds Rate
            }
            
            fred_results = {}
            base_url = "https://api.stlouisfed.org/fred/series/observations"
            
            for name, series_id in series_to_test.items():
                try:
                    params = {
                        'series_id': series_id,
                        'api_key': api_key,
                        'file_type': 'json',
                        'limit': 10,
                        'sort_order': 'desc'
                    }
                    
                    response = requests.get(base_url, params=params, timeout=10)
                    response.raise_for_status()
                    
                    data = response.json()
                    
                    if 'observations' in data and data['observations']:
                        latest_obs = data['observations'][0]
                        fred_results[name] = {
                            "series_id": series_id,
                            "latest_value": latest_obs.get('value'),
                            "latest_date": latest_obs.get('date'),
                            "status": "success"
                        }
                        logger.info(f"✅ {name} ({series_id}): {latest_obs.get('value')} ({latest_obs.get('date')})")
                    else:
                        fred_results[name] = {
                            "series_id": series_id,
                            "status": "no_data"
                        }
                        logger.warning(f"⚠️ {name} ({series_id}): Sin datos")
                        
                except Exception as e:
                    fred_results[name] = {
                        "series_id": series_id,
                        "status": "error",
                        "error": str(e)
                    }
                    logger.error(f"❌ {name} ({series_id}): {e}")
            
            self.results["sources_tested"].append("FRED")
            self.results["successful_sources"].append("FRED")
            self.results["api_keys_status"]["FRED"] = "configured"
            self.results["fred_api"] = fred_results
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error general en FRED API: {e}")
            self.results["failed_sources"].append("FRED")
            self.results["api_keys_status"]["FRED"] = "error"
            return False
    
    def test_alpha_vantage_api(self, api_key=None):
        """Probar Alpha Vantage API (requiere API key)."""
        logger.info("🔍 Probando Alpha Vantage API...")
        
        if not api_key:
            logger.warning("⚠️ Alpha Vantage API key no configurada - usando datos simulados")
            self.results["api_keys_status"]["Alpha_Vantage"] = "not_configured"
            self.results["sources_tested"].append("Alpha Vantage (simulado)")
            self.results["alpha_vantage_simulated"] = {
                "status": "simulated",
                "reason": "API key not configured"
            }
            return False
        
        try:
            # Probar funciones relevantes
            functions_to_test = {
                'Steel_Prices': {
                    'function': 'COMMODITY_PRICES',
                    'interval': 'monthly',
                    'datatype': 'json'
                },
                'Exchange_Rates': {
                    'function': 'FX_DAILY',
                    'from_symbol': 'USD',
                    'to_symbol': 'MXN',
                    'datatype': 'json'
                }
            }
            
            av_results = {}
            base_url = "https://www.alphavantage.co/query"
            
            for name, params in functions_to_test.items():
                try:
                    params['apikey'] = api_key
                    
                    response = requests.get(base_url, params=params, timeout=10)
                    response.raise_for_status()
                    
                    data = response.json()
                    
                    if 'Error Message' in data:
                        av_results[name] = {
                            "status": "error",
                            "error": data['Error Message']
                        }
                        logger.error(f"❌ {name}: {data['Error Message']}")
                    elif 'Note' in data:
                        av_results[name] = {
                            "status": "rate_limited",
                            "note": data['Note']
                        }
                        logger.warning(f"⚠️ {name}: Rate limited - {data['Note']}")
                    else:
                        av_results[name] = {
                            "status": "success",
                            "data_keys": list(data.keys())
                        }
                        logger.info(f"✅ {name}: Datos recibidos")
                        
                except Exception as e:
                    av_results[name] = {
                        "status": "error",
                        "error": str(e)
                    }
                    logger.error(f"❌ {name}: {e}")
            
            self.results["sources_tested"].append("Alpha Vantage")
            self.results["successful_sources"].append("Alpha Vantage")
            self.results["api_keys_status"]["Alpha_Vantage"] = "configured"
            self.results["alpha_vantage_api"] = av_results
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error general en Alpha Vantage API: {e}")
            self.results["failed_sources"].append("Alpha Vantage")
            self.results["api_keys_status"]["Alpha Vantage"] = "error"
            return False
    
    def create_env_template(self):
        """Crear template de archivo .env para API keys."""
        env_template = """# API Keys para Fuentes de Datos Externas
# Copia este archivo como .env y configura tus API keys

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
        
        with open('.env.template', 'w') as f:
            f.write(env_template)
        
        logger.info("📝 Template .env.template creado")
        logger.info("🔑 Para activar fuentes reales:")
        logger.info("   1. Copia .env.template a .env")
        logger.info("   2. Obtén API keys de FRED y Alpha Vantage")
        logger.info("   3. Configura las keys en el archivo .env")
    
    def run_full_test(self):
        """Ejecutar prueba completa de todas las fuentes."""
        logger.info("🚀 INICIANDO CONFIGURACIÓN DE FUENTES DE DATOS REALES")
        logger.info("=" * 60)
        
        # Leer API keys del entorno
        fred_key = os.getenv('FRED_API_KEY', '')
        av_key = os.getenv('ALPHA_VANTAGE_API_KEY', '')
        
        # Probar Yahoo Finance (siempre funciona)
        self.test_yahoo_finance()
        
        # Probar FRED API
        self.test_fred_api(fred_key if fred_key else None)
        
        # Probar Alpha Vantage API
        self.test_alpha_vantage_api(av_key if av_key else None)
        
        # Crear template de configuración
        self.create_env_template()
        
        # Generar reporte
        self.generate_report()
        
        return self.results
    
    def generate_report(self):
        """Generar reporte de configuración."""
        logger.info("\n" + "=" * 60)
        logger.info("📊 REPORTE DE CONFIGURACIÓN DE FUENTES")
        logger.info("=" * 60)
        
        logger.info(f"✅ Fuentes exitosas: {len(self.results['successful_sources'])}")
        for source in self.results['successful_sources']:
            logger.info(f"   - {source}")
        
        logger.info(f"❌ Fuentes fallidas: {len(self.results['failed_sources'])}")
        for source in self.results['failed_sources']:
            logger.info(f"   - {source}")
        
        logger.info("\n🔑 Estado de API Keys:")
        for api, status in self.results['api_keys_status'].items():
            status_emoji = "✅" if status == "configured" else "⚠️" if status == "not_configured" else "❌"
            logger.info(f"   {status_emoji} {api}: {status}")
        
        # Guardar resultados
        with open('data_sources_configuration_report.json', 'w') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"\n💾 Reporte guardado en: data_sources_configuration_report.json")
        
        # Recomendaciones
        logger.info("\n🎯 RECOMENDACIONES:")
        if "Yahoo Finance" in self.results['successful_sources']:
            logger.info("✅ Yahoo Finance funcionando - usar para datos básicos")
        
        if self.results['api_keys_status'].get('FRED') == 'not_configured':
            logger.info("🔑 Configurar FRED API key para datos económicos oficiales")
        
        if self.results['api_keys_status'].get('Alpha_Vantage') == 'not_configured':
            logger.info("🔑 Configurar Alpha Vantage API key para datos avanzados")


def main():
    """Función principal."""
    config = RealDataSourcesConfig()
    results = config.run_full_test()
    
    return results


if __name__ == "__main__":
    main()
