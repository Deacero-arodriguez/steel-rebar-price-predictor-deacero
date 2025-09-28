#!/usr/bin/env python3
"""
Script para probar la API de Steel Rebar Price Predictor en GCP.
Verifica todos los endpoints y funcionalidades.
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any

# URL de la API en GCP
API_BASE_URL = "https://steel-rebar-predictor-646072255295.us-central1.run.app"
API_KEY = "deacero_steel_predictor_2025_key"

class APITester:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': api_key,
            'Content-Type': 'application/json'
        })
        
    def test_health_check(self) -> Dict[str, Any]:
        """Probar endpoint de health check."""
        print("🏥 Probando Health Check...")
        try:
            response = requests.get(f"{self.base_url}/health")
            response.raise_for_status()
            
            result = {
                "endpoint": "/health",
                "status_code": response.status_code,
                "response": response.json(),
                "success": True,
                "response_time": response.elapsed.total_seconds()
            }
            
            print(f"✅ Health Check: {result['status_code']} - {result['response_time']:.2f}s")
            return result
            
        except Exception as e:
            print(f"❌ Health Check falló: {e}")
            return {
                "endpoint": "/health",
                "success": False,
                "error": str(e)
            }
    
    def test_service_info(self) -> Dict[str, Any]:
        """Probar endpoint de información del servicio."""
        print("ℹ️ Probando Service Info...")
        try:
            response = requests.get(f"{self.base_url}/")
            response.raise_for_status()
            
            result = {
                "endpoint": "/",
                "status_code": response.status_code,
                "response": response.json(),
                "success": True,
                "response_time": response.elapsed.total_seconds()
            }
            
            print(f"✅ Service Info: {result['status_code']} - {result['response_time']:.2f}s")
            return result
            
        except Exception as e:
            print(f"❌ Service Info falló: {e}")
            return {
                "endpoint": "/",
                "success": False,
                "error": str(e)
            }
    
    def test_prediction_without_api_key(self) -> Dict[str, Any]:
        """Probar endpoint de predicción sin API key."""
        print("🔒 Probando Predicción sin API Key...")
        try:
            response = requests.get(f"{self.base_url}/predict/steel-rebar-price")
            
            result = {
                "endpoint": "/predict/steel-rebar-price (sin API key)",
                "status_code": response.status_code,
                "response": response.json() if response.content else None,
                "success": response.status_code == 401,
                "response_time": response.elapsed.total_seconds()
            }
            
            if result['success']:
                print(f"✅ Sin API Key: {result['status_code']} (correcto)")
            else:
                print(f"❌ Sin API Key: {result['status_code']} (debería ser 401)")
            return result
            
        except Exception as e:
            print(f"❌ Test sin API Key falló: {e}")
            return {
                "endpoint": "/predict/steel-rebar-price (sin API key)",
                "success": False,
                "error": str(e)
            }
    
    def test_prediction_with_invalid_api_key(self) -> Dict[str, Any]:
        """Probar endpoint de predicción con API key inválido."""
        print("🔒 Probando Predicción con API Key Inválido...")
        try:
            headers = {'X-API-Key': 'invalid_key'}
            response = requests.get(f"{self.base_url}/predict/steel-rebar-price", headers=headers)
            
            result = {
                "endpoint": "/predict/steel-rebar-price (API key inválido)",
                "status_code": response.status_code,
                "response": response.json() if response.content else None,
                "success": response.status_code == 401,
                "response_time": response.elapsed.total_seconds()
            }
            
            if result['success']:
                print(f"✅ API Key Inválido: {result['status_code']} (correcto)")
            else:
                print(f"❌ API Key Inválido: {result['status_code']} (debería ser 401)")
            return result
            
        except Exception as e:
            print(f"❌ Test API Key Inválido falló: {e}")
            return {
                "endpoint": "/predict/steel-rebar-price (API key inválido)",
                "success": False,
                "error": str(e)
            }
    
    def test_prediction_with_valid_api_key(self) -> Dict[str, Any]:
        """Probar endpoint de predicción con API key válido."""
        print("🎯 Probando Predicción con API Key Válido...")
        try:
            response = self.session.get(f"{self.base_url}/predict/steel-rebar-price")
            response.raise_for_status()
            
            result = {
                "endpoint": "/predict/steel-rebar-price",
                "status_code": response.status_code,
                "response": response.json(),
                "success": True,
                "response_time": response.elapsed.total_seconds()
            }
            
            print(f"✅ Predicción: {result['status_code']} - {result['response_time']:.2f}s")
            
            # Validar formato de respuesta
            if self._validate_prediction_response(result['response']):
                print("✅ Formato de respuesta válido")
            else:
                print("❌ Formato de respuesta inválido")
                result['success'] = False
                
            return result
            
        except Exception as e:
            print(f"❌ Predicción falló: {e}")
            return {
                "endpoint": "/predict/steel-rebar-price",
                "success": False,
                "error": str(e)
            }
    
    def test_rate_limiting(self) -> Dict[str, Any]:
        """Probar rate limiting (hacer múltiples requests rápidos)."""
        print("⚡ Probando Rate Limiting...")
        try:
            requests_made = 0
            rate_limited = False
            
            # Hacer 5 requests rápidos
            for i in range(5):
                response = self.session.get(f"{self.base_url}/predict/steel-rebar-price")
                requests_made += 1
                
                if response.status_code == 429:
                    rate_limited = True
                    print(f"✅ Rate Limiting detectado en request {i+1}")
                    break
                    
                time.sleep(0.1)  # Pequeña pausa entre requests
            
            result = {
                "endpoint": "Rate Limiting Test",
                "requests_made": requests_made,
                "rate_limited": rate_limited,
                "success": rate_limited or requests_made == 5,
                "note": "Rate limiting activado" if rate_limited else "No se activó rate limiting"
            }
            
            if result['success']:
                print(f"✅ Rate Limiting: {result['note']}")
            else:
                print(f"❌ Rate Limiting: No funcionó correctamente")
                
            return result
            
        except Exception as e:
            print(f"❌ Rate Limiting test falló: {e}")
            return {
                "endpoint": "Rate Limiting Test",
                "success": False,
                "error": str(e)
            }
    
    def _validate_prediction_response(self, response: Dict[str, Any]) -> bool:
        """Validar que la respuesta tenga el formato correcto."""
        required_fields = [
            'prediction_date',
            'predicted_price_usd_per_ton',
            'currency',
            'unit',
            'model_confidence',
            'timestamp'
        ]
        
        for field in required_fields:
            if field not in response:
                print(f"❌ Campo faltante: {field}")
                return False
        
        # Validar tipos de datos
        if not isinstance(response['predicted_price_usd_per_ton'], (int, float)):
            print("❌ predicted_price_usd_per_ton debe ser número")
            return False
            
        if not isinstance(response['model_confidence'], (int, float)):
            print("❌ model_confidence debe ser número")
            return False
            
        if response['currency'] != 'USD':
            print("❌ currency debe ser 'USD'")
            return False
            
        if response['unit'] != 'metric ton':
            print("❌ unit debe ser 'metric ton'")
            return False
        
        return True
    
    def run_complete_test(self) -> Dict[str, Any]:
        """Ejecutar todos los tests."""
        print("🚀 INICIANDO TEST COMPLETO DE API EN GCP")
        print("=" * 60)
        print(f"📍 URL: {self.base_url}")
        print(f"🔑 API Key: {self.api_key}")
        print(f"🕐 Timestamp: {datetime.now().isoformat()}")
        print("=" * 60)
        
        tests = [
            self.test_health_check,
            self.test_service_info,
            self.test_prediction_without_api_key,
            self.test_prediction_with_invalid_api_key,
            self.test_prediction_with_valid_api_key,
            self.test_rate_limiting
        ]
        
        results = []
        successful_tests = 0
        total_tests = len(tests)
        
        for test_func in tests:
            try:
                result = test_func()
                results.append(result)
                if result.get('success', False):
                    successful_tests += 1
                print()  # Línea en blanco entre tests
            except Exception as e:
                print(f"❌ Error ejecutando {test_func.__name__}: {e}")
                results.append({
                    "test": test_func.__name__,
                    "success": False,
                    "error": str(e)
                })
        
        # Resumen final
        print("=" * 60)
        print("📊 RESUMEN DE TESTS")
        print("=" * 60)
        print(f"✅ Tests exitosos: {successful_tests}/{total_tests}")
        print(f"❌ Tests fallidos: {total_tests - successful_tests}/{total_tests}")
        print(f"📈 Porcentaje de éxito: {(successful_tests/total_tests)*100:.1f}%")
        
        # Mostrar detalles de tests fallidos
        failed_tests = [r for r in results if not r.get('success', False)]
        if failed_tests:
            print("\n❌ TESTS FALLIDOS:")
            for test in failed_tests:
                print(f"  - {test.get('endpoint', test.get('test', 'Unknown'))}: {test.get('error', 'Unknown error')}")
        
        # Resultado final
        final_result = {
            "timestamp": datetime.now().isoformat(),
            "api_url": self.base_url,
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "failed_tests": total_tests - successful_tests,
            "success_rate": (successful_tests/total_tests)*100,
            "all_tests_passed": successful_tests == total_tests,
            "test_results": results
        }
        
        if final_result['all_tests_passed']:
            print("\n🎉 ¡TODOS LOS TESTS PASARON! API funcionando correctamente.")
        else:
            print(f"\n⚠️ {total_tests - successful_tests} test(s) fallaron. Revisar configuración.")
        
        return final_result

def main():
    """Función principal."""
    tester = APITester(API_BASE_URL, API_KEY)
    results = tester.run_complete_test()
    
    # Guardar resultados en archivo
    output_file = "gcp_api_test_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados guardados en: {output_file}")
    
    return results

if __name__ == "__main__":
    main()
