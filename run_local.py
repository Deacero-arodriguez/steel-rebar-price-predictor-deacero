#!/usr/bin/env python3
"""
Script para ejecutar la aplicación Steel Rebar Price Predictor localmente.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_requirements():
    """Verificar que los requerimientos estén instalados."""
    print("🔍 Verificando requerimientos...")
    
    try:
        import fastapi
        import uvicorn
        import pandas
        import sklearn
        import redis
        print("✅ Todas las dependencias están instaladas")
        return True
    except ImportError as e:
        print(f"❌ Falta dependencia: {e}")
        print("💡 Ejecuta: pip install -r requirements.txt")
        return False

def setup_environment():
    """Configurar variables de entorno."""
    print("⚙️ Configurando variables de entorno...")
    
    env_vars = {
        'API_KEY': 'deacero_steel_predictor_2025_key',
        'REDIS_URL': 'redis://localhost:6379',
        'YAHOO_FINANCE_ENABLED': 'true',
        'MODEL_UPDATE_FREQUENCY': '24',
        'CACHE_TTL': '3600',
        'RATE_LIMIT': '100'
    }
    
    for key, value in env_vars.items():
        os.environ[key] = value
    
    print("✅ Variables de entorno configuradas")

def check_redis():
    """Verificar si Redis está disponible."""
    print("🔍 Verificando conexión a Redis...")
    
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        r.ping()
        print("✅ Redis está disponible")
        return True
    except Exception as e:
        print(f"⚠️ Redis no está disponible: {e}")
        print("💡 La aplicación usará cache en memoria como fallback")
        return False

def run_tests():
    """Ejecutar tests básicos."""
    print("🧪 Ejecutando tests...")
    
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 'tests/', '-v', '--tb=short'
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print("✅ Tests pasaron correctamente")
        else:
            print("⚠️ Algunos tests fallaron:")
            print(result.stdout)
            print(result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error ejecutando tests: {e}")
        return False

def start_server():
    """Iniciar el servidor de desarrollo."""
    print("🚀 Iniciando servidor de desarrollo...")
    print("📍 URL: http://localhost:8000")
    print("📖 Documentación: http://localhost:8000/docs")
    print("🔑 API Key: deacero_steel_predictor_2025_key")
    print("⏹️ Presiona Ctrl+C para detener")
    print("-" * 50)
    
    try:
        import uvicorn
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido")
    except Exception as e:
        print(f"❌ Error iniciando servidor: {e}")

def main():
    """Función principal."""
    print("🏗️ Steel Rebar Price Predictor - Ejecución Local")
    print("=" * 50)
    
    # Cambiar al directorio del proyecto
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # Verificar requerimientos
    if not check_requirements():
        sys.exit(1)
    
    # Configurar entorno
    setup_environment()
    
    # Verificar Redis
    check_redis()
    
    # Preguntar si ejecutar tests
    run_tests_choice = input("\n¿Ejecutar tests antes de iniciar? (y/N): ").lower()
    if run_tests_choice in ['y', 'yes', 'sí', 'si']:
        if not run_tests():
            continue_choice = input("¿Continuar a pesar de los tests fallidos? (y/N): ").lower()
            if continue_choice not in ['y', 'yes', 'sí', 'si']:
                sys.exit(1)
    
    # Iniciar servidor
    start_server()

if __name__ == "__main__":
    main()
