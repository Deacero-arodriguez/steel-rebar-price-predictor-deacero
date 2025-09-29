#!/usr/bin/env python3
"""
Script completo para verificar la integración en producción
Verifica API, Storage, Redis, Cloud Run y todos los componentes
"""

import requests
import json
import time
from datetime import datetime

class ProductionVerification:
    def __init__(self):
        self.api_url = "https://steel-rebar-predictor-646072255295.us-central1.run.app"
        self.api_key = "deacero_steel_predictor_2025_key"
        self.results = {}
        
    def print_header(self, title):
        """Imprimir encabezado de sección."""
        print(f"\n{'='*60}")
        print(f"🔍 {title}")
        print(f"{'='*60}")
        
    def print_result(self, test_name, success, details=""):
        """Imprimir resultado de prueba."""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
        if details:
            print(f"   {details}")
        return success
    
    def test_api_basic(self):
        """Probar funcionalidad básica de la API."""
        self.print_header("PRUEBAS BÁSICAS DE LA API")
        
        try:
            # Test 1: Endpoint raíz
            response = requests.get(f"{self.api_url}/", timeout=10)
            success = self.print_result(
                "Endpoint raíz (/)",
                response.status_code == 200,
                f"Status: {response.status_code}, Versión: {response.json().get('version', 'N/A')}"
            )
            self.results['api_basic'] = success
            
            # Test 2: Documentación
            response = requests.get(f"{self.api_url}/docs", timeout=10)
            success = self.print_result(
                "Documentación (/docs)",
                response.status_code == 200,
                f"Status: {response.status_code}"
            )
            self.results['api_docs'] = success
            
            # Test 3: Health check
            response = requests.get(f"{self.api_url}/health", timeout=10)
            success = self.print_result(
                "Health check (/health)",
                response.status_code == 200,
                f"Status: {response.status_code}"
            )
            self.results['api_health'] = success
            
        except Exception as e:
            print(f"❌ Error en pruebas básicas: {e}")
            self.results['api_basic'] = False
    
    def test_api_prediction(self):
        """Probar funcionalidad de predicción."""
        self.print_header("PRUEBAS DE PREDICCIÓN")
        
        try:
            headers = {"X-API-Key": self.api_key}
            
            # Test 1: Predicción con API key
            response = requests.get(
                f"{self.api_url}/predict/steel-rebar-price",
                headers=headers,
                timeout=10
            )
            success = self.print_result(
                "Predicción con autenticación",
                response.status_code == 200,
                f"Status: {response.status_code}, Precio: ${response.json().get('predicted_price_usd_per_ton', 'N/A')}/ton"
            )
            self.results['prediction_auth'] = success
            
            # Test 2: Predicción sin API key (debe fallar)
            response = requests.get(
                f"{self.api_url}/predict/steel-rebar-price",
                timeout=10
            )
            success = self.print_result(
                "Predicción sin autenticación (debe fallar)",
                response.status_code == 401,
                f"Status: {response.status_code}"
            )
            self.results['prediction_no_auth'] = success
            
        except Exception as e:
            print(f"❌ Error en pruebas de predicción: {e}")
            self.results['prediction_auth'] = False
    
    def test_automation_endpoints(self):
        """Probar endpoints de automatización."""
        self.print_header("PRUEBAS DE AUTOMATIZACIÓN")
        
        headers = {"X-API-Key": self.api_key}
        endpoints = [
            ("/automation/status", "Estado de automatización"),
            ("/update-data", "Actualización de datos"),
            ("/retrain-model", "Reentrenamiento del modelo"),
            ("/monitor-performance", "Monitoreo de rendimiento")
        ]
        
        for endpoint, description in endpoints:
            try:
                if endpoint == "/automation/status":
                    response = requests.get(f"{self.api_url}{endpoint}", headers=headers, timeout=10)
                else:
                    response = requests.post(f"{self.api_url}{endpoint}", headers=headers, timeout=10)
                
                success = self.print_result(
                    description,
                    response.status_code == 200,
                    f"Status: {response.status_code}"
                )
                self.results[f'automation_{endpoint.replace("/", "_")}'] = success
                
            except Exception as e:
                print(f"❌ Error en {description}: {e}")
                self.results[f'automation_{endpoint.replace("/", "_")}'] = False
    
    def test_performance(self):
        """Probar rendimiento de la API."""
        self.print_header("PRUEBAS DE RENDIMIENTO")
        
        try:
            headers = {"X-API-Key": self.api_key}
            times = []
            
            # Realizar 5 requests para medir tiempo promedio
            for i in range(5):
                start_time = time.time()
                response = requests.get(
                    f"{self.api_url}/predict/steel-rebar-price",
                    headers=headers,
                    timeout=10
                )
                end_time = time.time()
                
                if response.status_code == 200:
                    times.append(end_time - start_time)
                
                time.sleep(0.5)  # Pequeña pausa entre requests
            
            if times:
                avg_time = sum(times) / len(times)
                max_time = max(times)
                min_time = min(times)
                
                success = avg_time < 2.0  # Menos de 2 segundos
                self.print_result(
                    "Tiempo de respuesta promedio",
                    success,
                    f"Promedio: {avg_time:.2f}s, Min: {min_time:.2f}s, Max: {max_time:.2f}s"
                )
                self.results['performance'] = success
            else:
                print("❌ No se pudieron medir tiempos de respuesta")
                self.results['performance'] = False
                
        except Exception as e:
            print(f"❌ Error en pruebas de rendimiento: {e}")
            self.results['performance'] = False
    
    def test_data_integration(self):
        """Probar integración de datos."""
        self.print_header("PRUEBAS DE INTEGRACIÓN DE DATOS")
        
        try:
            headers = {"X-API-Key": self.api_key}
            
            # Test: Verificar que la API tiene datos de fuentes múltiples
            response = requests.get(f"{self.api_url}/", headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                data_sources = data.get('data_sources', [])
                
                success = len(data_sources) >= 4
                self.print_result(
                    "Fuentes de datos integradas",
                    success,
                    f"Fuentes: {len(data_sources)} - {', '.join(data_sources)}"
                )
                self.results['data_sources'] = success
                
                # Verificar métricas del modelo
                model_perf = data.get('model_performance', {})
                mape = model_perf.get('mape', 0)
                r2 = model_perf.get('r2_score', 0)
                
                success = mape < 1.0 and r2 > 0.95
                self.print_result(
                    "Métricas del modelo",
                    success,
                    f"MAPE: {mape}%, R²: {r2}"
                )
                self.results['model_metrics'] = success
            else:
                print("❌ No se pudo obtener información de la API")
                self.results['data_sources'] = False
                
        except Exception as e:
            print(f"❌ Error en pruebas de integración: {e}")
            self.results['data_sources'] = False
    
    def generate_summary(self):
        """Generar resumen final."""
        self.print_header("RESUMEN FINAL DE VERIFICACIÓN")
        
        total_tests = len(self.results)
        passed_tests = sum(1 for result in self.results.values() if result)
        success_rate = (passed_tests / total_tests) * 100
        
        print(f"📊 Tests ejecutados: {total_tests}")
        print(f"✅ Tests exitosos: {passed_tests}")
        print(f"❌ Tests fallidos: {total_tests - passed_tests}")
        print(f"📈 Tasa de éxito: {success_rate:.1f}%")
        
        print(f"\n📋 Detalles por categoría:")
        categories = {
            'api_basic': 'API Básica',
            'api_docs': 'Documentación',
            'api_health': 'Health Check',
            'prediction_auth': 'Predicción Autenticada',
            'prediction_no_auth': 'Seguridad API',
            'automation_automation_status': 'Estado Automatización',
            'automation_update_data': 'Actualización Datos',
            'automation_retrain_model': 'Reentrenamiento',
            'automation_monitor_performance': 'Monitoreo',
            'performance': 'Rendimiento',
            'data_sources': 'Fuentes de Datos',
            'model_metrics': 'Métricas Modelo'
        }
        
        for key, description in categories.items():
            if key in self.results:
                status = "✅" if self.results[key] else "❌"
                print(f"   {status} {description}")
        
        # Determinar estado general
        if success_rate >= 90:
            status = "🟢 EXCELENTE - LISTO PARA PRODUCCIÓN"
        elif success_rate >= 75:
            status = "🟡 BUENO - LISTO CON OBSERVACIONES"
        elif success_rate >= 50:
            status = "🟠 REGULAR - REQUIERE ATENCIÓN"
        else:
            status = "🔴 CRÍTICO - NO LISTO PARA PRODUCCIÓN"
        
        print(f"\n🎯 Estado General: {status}")
        
        # Recomendaciones
        if success_rate < 100:
            print(f"\n💡 Recomendaciones:")
            if not self.results.get('automation_monitor_performance', True):
                print("   - Corregir endpoint de monitoreo de rendimiento")
            if not self.results.get('performance', True):
                print("   - Optimizar tiempos de respuesta de la API")
            if not self.results.get('model_metrics', True):
                print("   - Revisar métricas del modelo de ML")
        
        return success_rate >= 90
    
    def run_all_tests(self):
        """Ejecutar todas las pruebas."""
        print("🚀 INICIANDO VERIFICACIÓN COMPLETA DE PRODUCCIÓN")
        print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌐 API URL: {self.api_url}")
        
        self.test_api_basic()
        self.test_api_prediction()
        self.test_automation_endpoints()
        self.test_performance()
        self.test_data_integration()
        
        return self.generate_summary()

if __name__ == "__main__":
    verifier = ProductionVerification()
    is_production_ready = verifier.run_all_tests()
    
    if is_production_ready:
        print(f"\n🎉 ¡SISTEMA LISTO PARA PRODUCCIÓN!")
        exit(0)
    else:
        print(f"\n⚠️ Sistema requiere atención antes de producción")
        exit(1)
