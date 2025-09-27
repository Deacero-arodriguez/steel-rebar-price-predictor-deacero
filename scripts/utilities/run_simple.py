#!/usr/bin/env python3
"""
Script simplificado para ejecutar la aplicación Steel Rebar Price Predictor localmente.
"""

import sys
import os
from pathlib import Path

# Configurar variables de entorno
os.environ['API_KEY'] = 'deacero_steel_predictor_2025_key'
os.environ['REDIS_URL'] = 'redis://localhost:6379'
os.environ['YAHOO_FINANCE_ENABLED'] = 'true'
os.environ['MODEL_UPDATE_FREQUENCY'] = '24'
os.environ['CACHE_TTL'] = '3600'
os.environ['RATE_LIMIT'] = '100'

# Agregar el directorio app al path
sys.path.append(str(Path(__file__).parent / "app"))

def main():
    """Función principal para ejecutar la aplicación."""
    print("🏗️ Steel Rebar Price Predictor - Ejecución Local Simplificada")
    print("=" * 60)
    
    try:
        import uvicorn
        print("✅ Uvicorn importado correctamente")
        
        # Intentar importar la aplicación
        try:
            from src.app.main import app
            print("✅ Aplicación FastAPI importada correctamente")
        except Exception as e:
            print(f"⚠️ Error importando la aplicación: {e}")
            print("💡 Creando aplicación básica...")
            
            # Crear aplicación básica si hay problemas
            from fastapi import FastAPI
            app = FastAPI(title="Steel Rebar Price Predictor", version="1.0.0")
            
            @app.get("/")
            async def root():
                return {
                    "service": "Steel Rebar Price Predictor",
                    "version": "1.0",
                    "status": "running",
                    "note": "Aplicación básica - algunas funciones pueden no estar disponibles"
                }
            
            @app.get("/health")
            async def health():
                return {"status": "healthy", "timestamp": "2025-01-27T10:00:00Z"}
        
        print("\n🚀 Iniciando servidor...")
        print("📍 URL: http://localhost:8000")
        print("📖 Documentación: http://localhost:8000/docs")
        print("🔑 API Key: deacero_steel_predictor_2025_key")
        print("⏹️ Presiona Ctrl+C para detener")
        print("-" * 50)
        
        # Ejecutar el servidor
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido")
    except Exception as e:
        print(f"❌ Error ejecutando la aplicación: {e}")
        print("💡 Verifica que todas las dependencias estén instaladas correctamente")

if __name__ == "__main__":
    main()
