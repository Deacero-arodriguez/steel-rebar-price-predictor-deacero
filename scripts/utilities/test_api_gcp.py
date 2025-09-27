#!/usr/bin/env python3
"""
Script de Test para API de Steel Rebar Predictor en GCP
Realiza 10 llamadas a la API desplegada en Google Cloud Platform
"""

import asyncio
import aiohttp
import time
import json
from datetime import datetime
from typing import List, Dict, Any
import statistics
import sys
import os

# Configuración
API_KEY = "deacero_steel_predictor_2025_key"
# URL de la API en GCP - actualizar con tu URL real de Cloud Run
API_BASE_URL = "https://steel-rebar-predictor-[PROJECT-ID]-uc.a.run.app"  # Reemplazar [PROJECT-ID] con tu project ID

# Headers para las requests
HEADERS = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json",
    "User-Agent": "DeAcero-Test-Script/1.0"
}

class APITester:
    """Clase para realizar tests de la API en GCP."""
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.results = []
        
    async def make_single_request(self, session: aiohttp.ClientSession, request_id: int) -> Dict[str, Any]:
        """Realizar una sola llamada a la API."""
        
        start_time = time.time()
        
        try:
            # Endpoint de predicción principal
            url = f"{self.base_url}/predict/steel-rebar-price"
            
            async with session.get(url, headers=HEADERS) as response:
                end_time = time.time()
                response_time = end_time - start_time
                
                # Obtener el contenido de la respuesta
                response_text = await response.text()
                
                result = {
                    "request_id": request_id,
                    "timestamp": datetime.now().isoformat(),
                    "status_code": response.status,
                    "response_time_ms": round(response_time * 1000, 2),
                    "success": response.status == 200,
                    "url": url,
                    "headers": dict(response.headers)
                }
                
                # Intentar parsear JSON si la respuesta es exitosa
                if response.status == 200:
                    try:
                        response_data = json.loads(response_text)
                        result["response_data"] = response_data
                        result["predicted_price"] = response_data.get("predicted_price_usd_per_ton")
                        result["confidence"] = response_data.get("model_confidence")
                        result["prediction_date"] = response_data.get("prediction_date")
                    except json.JSONDecodeError:
                        result["response_text"] = response_text
                        result["parse_error"] = "Failed to parse JSON response"
                else:
                    result["error_response"] = response_text
                
                return result
                
        except asyncio.TimeoutError:
            return {
                "request_id": request_id,
                "timestamp": datetime.now().isoformat(),
                "status_code": 0,
                "response_time_ms": round((time.time() - start_time) * 1000, 2),
                "success": False,
                "error": "Request timeout",
                "url": url
            }
        except Exception as e:
            return {
                "request_id": request_id,
                "timestamp": datetime.now().isoformat(),
                "status_code": 0,
                "response_time_ms": round((time.time() - start_time) * 1000, 2),
                "success": False,
                "error": str(e),
                "url": url
            }
    
    async def test_health_endpoint(self, session: aiohttp.ClientSession) -> Dict[str, Any]:
        """Test del endpoint de health check."""
        
        start_time = time.time()
        
        try:
            url = f"{self.base_url}/health"
            
            async with session.get(url, timeout=10) as response:
                end_time = time.time()
                response_time = end_time - start_time
                
                response_text = await response.text()
                
                result = {
                    "endpoint": "health",
                    "timestamp": datetime.now().isoformat(),
                    "status_code": response.status,
                    "response_time_ms": round(response_time * 1000, 2),
                    "success": response.status == 200,
                    "url": url
                }
                
                if response.status == 200:
                    try:
                        result["health_data"] = json.loads(response_text)
                    except json.JSONDecodeError:
                        result["response_text"] = response_text
                else:
                    result["error_response"] = response_text
                
                return result
                
        except Exception as e:
            return {
                "endpoint": "health",
                "timestamp": datetime.now().isoformat(),
                "status_code": 0,
                "success": False,
                "error": str(e),
                "url": url
            }
    
    async def test_service_info(self, session: aiohttp.ClientSession) -> Dict[str, Any]:
        """Test del endpoint de información del servicio."""
        
        start_time = time.time()
        
        try:
            url = f"{self.base_url}/"
            
            async with session.get(url, timeout=10) as response:
                end_time = time.time()
                response_time = end_time - start_time
                
                response_text = await response.text()
                
                result = {
                    "endpoint": "service_info",
                    "timestamp": datetime.now().isoformat(),
                    "status_code": response.status,
                    "response_time_ms": round(response_time * 1000, 2),
                    "success": response.status == 200,
                    "url": url
                }
                
                if response.status == 200:
                    try:
                        result["service_data"] = json.loads(response_text)
                    except json.JSONDecodeError:
                        result["response_text"] = response_text
                else:
                    result["error_response"] = response_text
                
                return result
                
        except Exception as e:
            return {
                "endpoint": "service_info",
                "timestamp": datetime.now().isoformat(),
                "status_code": 0,
                "success": False,
                "error": str(e),
                "url": url
            }
    
    async def run_test_suite(self, num_requests: int = 10) -> Dict[str, Any]:
        """Ejecutar la suite completa de tests."""
        
        print(f"🚀 Iniciando test de {num_requests} llamadas a la API en GCP")
        print(f"📍 URL Base: {self.base_url}")
        print(f"🔑 API Key: {self.api_key[:20]}...")
        print("-" * 60)
        
        # Configurar timeout y conexiones
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        connector = aiohttp.TCPConnector(limit=10, limit_per_host=5)
        
        async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
            
            # 1. Test de endpoints básicos
            print("🔍 Probando endpoints básicos...")
            health_result = await self.test_health_endpoint(session)
            service_info_result = await self.test_service_info(session)
            
            print(f"   Health Check: {'✅' if health_result['success'] else '❌'} "
                  f"({health_result['response_time_ms']}ms)")
            print(f"   Service Info: {'✅' if service_info_result['success'] else '❌'} "
                  f"({service_info_result['response_time_ms']}ms)")
            
            # 2. Test de predicciones (10 llamadas)
            print(f"\n📊 Realizando {num_requests} llamadas de predicción...")
            
            start_time = time.time()
            
            # Crear tareas para las llamadas concurrentes
            tasks = []
            for i in range(num_requests):
                task = self.make_single_request(session, i + 1)
                tasks.append(task)
            
            # Ejecutar todas las llamadas
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            total_time = time.time() - start_time
            
            # Procesar resultados
            successful_requests = []
            failed_requests = []
            
            for result in results:
                if isinstance(result, Exception):
                    failed_requests.append({
                        "error": str(result),
                        "timestamp": datetime.now().isoformat()
                    })
                elif result["success"]:
                    successful_requests.append(result)
                else:
                    failed_requests.append(result)
            
            # Generar estadísticas
            response_times = [r["response_time_ms"] for r in successful_requests]
            predictions = [r.get("predicted_price") for r in successful_requests if r.get("predicted_price")]
            confidences = [r.get("confidence") for r in successful_requests if r.get("confidence")]
            
            stats = {
                "test_summary": {
                    "total_requests": num_requests,
                    "successful_requests": len(successful_requests),
                    "failed_requests": len(failed_requests),
                    "success_rate": len(successful_requests) / num_requests * 100,
                    "total_test_time": round(total_time, 2)
                },
                "response_time_stats": {
                    "min_ms": round(min(response_times), 2) if response_times else 0,
                    "max_ms": round(max(response_times), 2) if response_times else 0,
                    "avg_ms": round(statistics.mean(response_times), 2) if response_times else 0,
                    "median_ms": round(statistics.median(response_times), 2) if response_times else 0,
                    "p95_ms": round(statistics.quantiles(response_times, n=20)[18], 2) if len(response_times) >= 20 else 0
                },
                "prediction_stats": {
                    "avg_predicted_price": round(statistics.mean(predictions), 2) if predictions else 0,
                    "min_predicted_price": round(min(predictions), 2) if predictions else 0,
                    "max_predicted_price": round(max(predictions), 2) if predictions else 0,
                    "avg_confidence": round(statistics.mean(confidences), 3) if confidences else 0
                },
                "endpoint_tests": {
                    "health_check": health_result,
                    "service_info": service_info_result
                },
                "detailed_results": {
                    "successful_requests": successful_requests,
                    "failed_requests": failed_requests
                }
            }
            
            return stats
    
    def print_results(self, stats: Dict[str, Any]):
        """Imprimir resultados del test de forma legible."""
        
        print("\n" + "="*60)
        print("📋 RESUMEN DEL TEST DE API EN GCP")
        print("="*60)
        
        summary = stats["test_summary"]
        print(f"🎯 Total de requests: {summary['total_requests']}")
        print(f"✅ Requests exitosos: {summary['successful_requests']}")
        print(f"❌ Requests fallidos: {summary['failed_requests']}")
        print(f"📈 Tasa de éxito: {summary['success_rate']:.1f}%")
        print(f"⏱️  Tiempo total: {summary['total_test_time']}s")
        
        print(f"\n🚀 ESTADÍSTICAS DE TIEMPO DE RESPUESTA")
        print("-" * 40)
        rt_stats = stats["response_time_stats"]
        print(f"   Mínimo: {rt_stats['min_ms']}ms")
        print(f"   Máximo: {rt_stats['max_ms']}ms")
        print(f"   Promedio: {rt_stats['avg_ms']}ms")
        print(f"   Mediana: {rt_stats['median_ms']}ms")
        print(f"   P95: {rt_stats['p95_ms']}ms")
        
        print(f"\n💰 ESTADÍSTICAS DE PREDICCIONES")
        print("-" * 40)
        pred_stats = stats["prediction_stats"]
        print(f"   Precio promedio: ${pred_stats['avg_predicted_price']} USD/ton")
        print(f"   Rango: ${pred_stats['min_predicted_price']} - ${pred_stats['max_predicted_price']} USD/ton")
        print(f"   Confianza promedio: {pred_stats['avg_confidence']:.3f}")
        
        print(f"\n🔍 ENDPOINTS BÁSICOS")
        print("-" * 40)
        health = stats["endpoint_tests"]["health_check"]
        service = stats["endpoint_tests"]["service_info"]
        print(f"   Health Check: {'✅' if health['success'] else '❌'} ({health['response_time_ms']}ms)")
        print(f"   Service Info: {'✅' if service['success'] else '❌'} ({service['response_time_ms']}ms)")
        
        # Mostrar detalles de errores si los hay
        if stats["detailed_results"]["failed_requests"]:
            print(f"\n❌ DETALLES DE ERRORES")
            print("-" * 40)
            for i, error in enumerate(stats["detailed_results"]["failed_requests"][:3], 1):
                print(f"   Error {i}: {error.get('error', 'Unknown error')}")
                if error.get('status_code'):
                    print(f"      Status: {error['status_code']}")
    
    def save_results(self, stats: Dict[str, Any], filename: str = None):
        """Guardar resultados en archivo JSON."""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"api_test_results_{timestamp}.json"
        
        filepath = os.path.join("data", "predictions", filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Resultados guardados en: {filepath}")
        return filepath

async def main():
    """Función principal."""
    
    # Verificar que se proporcione la URL de la API
    if len(sys.argv) > 1:
        api_url = sys.argv[1]
    else:
        # Intentar obtener la URL del entorno o usar la por defecto
        api_url = os.getenv('GCP_API_URL', API_BASE_URL)
        
        if "[PROJECT-ID]" in api_url:
            print("❌ Error: Debes proporcionar la URL completa de tu API en GCP")
            print("   Uso: python test_api_gcp.py https://tu-api-url.a.run.app")
            print("   O configura la variable de entorno GCP_API_URL")
            return
    
    # Crear instancia del tester
    tester = APITester(api_url, API_KEY)
    
    try:
        # Ejecutar tests
        stats = await tester.run_test_suite(10)
        
        # Mostrar resultados
        tester.print_results(stats)
        
        # Guardar resultados
        tester.save_results(stats)
        
        # Determinar si el test fue exitoso
        success_rate = stats["test_summary"]["success_rate"]
        if success_rate >= 90:
            print(f"\n🎉 TEST EXITOSO: {success_rate:.1f}% de éxito")
            sys.exit(0)
        elif success_rate >= 70:
            print(f"\n⚠️  TEST PARCIALMENTE EXITOSO: {success_rate:.1f}% de éxito")
            sys.exit(1)
        else:
            print(f"\n❌ TEST FALLIDO: Solo {success_rate:.1f}% de éxito")
            sys.exit(2)
            
    except KeyboardInterrupt:
        print("\n⏹️  Test interrumpido por el usuario")
        sys.exit(3)
    except Exception as e:
        print(f"\n💥 Error inesperado: {e}")
        sys.exit(4)

if __name__ == "__main__":
    # Configurar encoding para Windows
    if sys.platform == "win32":
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    
    # Ejecutar test
    asyncio.run(main())
