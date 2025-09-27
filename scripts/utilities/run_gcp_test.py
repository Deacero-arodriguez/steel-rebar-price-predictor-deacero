#!/usr/bin/env python3
"""
Script simple para ejecutar tests de la API en GCP
Uso: python run_gcp_test.py [URL_DE_LA_API]
"""

import sys
import os
import subprocess

def main():
    """Función principal simplificada."""
    
    print("🧪 TEST DE API EN GCP - Steel Rebar Predictor")
    print("=" * 50)
    
    # Verificar argumentos
    if len(sys.argv) < 2:
        print("❌ Error: Debes proporcionar la URL de la API")
        print("\n📋 OPCIONES DE USO:")
        print("   1. Proporcionar URL directamente:")
        print("      python run_gcp_test.py https://steel-rebar-predictor-[PROJECT-ID]-uc.a.run.app")
        print("\n   2. Usar variable de entorno:")
        print("      set GCP_API_URL=https://tu-api-url.a.run.app")
        print("      python run_gcp_test.py")
        print("\n   3. Deployment completo (incluye build y deploy):")
        print("      python deploy_and_test_gcp.py [PROJECT-ID]")
        return 1
    
    api_url = sys.argv[1]
    
    # Verificar que la URL sea válida
    if not api_url.startswith("https://"):
        print("❌ Error: La URL debe empezar con https://")
        return 1
    
    print(f"🎯 URL de la API: {api_url}")
    print("🚀 Iniciando tests...")
    print("-" * 50)
    
    # Ejecutar el script de test
    test_script = os.path.join(os.path.dirname(__file__), "test_api_gcp.py")
    
    if not os.path.exists(test_script):
        print(f"❌ Error: No se encontró el script de test en {test_script}")
        return 1
    
    try:
        # Ejecutar el test
        result = subprocess.run([
            sys.executable, test_script, api_url
        ], capture_output=False)
        
        print("\n" + "=" * 50)
        
        if result.returncode == 0:
            print("🎉 TESTS COMPLETADOS EXITOSAMENTE")
            print("   ✅ Todas las pruebas pasaron")
        elif result.returncode == 1:
            print("⚠️  TESTS COMPLETADOS CON ADVERTENCIAS")
            print("   ⚠️  Algunas pruebas fallaron, pero el servicio funciona")
        elif result.returncode == 2:
            print("❌ TESTS FALLARON")
            print("   ❌ Múltiples fallos en las pruebas")
        else:
            print("💥 ERROR INESPERADO EN LOS TESTS")
            print(f"   💥 Código de error: {result.returncode}")
        
        return result.returncode
        
    except FileNotFoundError:
        print("❌ Error: Python no encontrado en el PATH")
        return 1
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrumpidos por el usuario")
        return 3
    except Exception as e:
        print(f"💥 Error inesperado: {e}")
        return 4

if __name__ == "__main__":
    sys.exit(main())
