#!/usr/bin/env python3
"""
Script de Test de Estrés para la API de Steel Rebar Price Predictor en GCP.
Simula múltiples usuarios concurrentes haciendo requests a la API.
"""

import asyncio
import aiohttp
import time
import statistics
from datetime import datetime
from typing import List, Dict, Any
import json
import argparse

# URL de la API en GCP
API_BASE_URL = "https://steel-rebar-predictor-646072255295.us-central1.run.app"
API_KEY = "deacero_steel_predictor_2025_key"

class StressTestResults:
    def __init__(self):
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.response_times = []
        self.status_codes = {}
        self.errors = []
        self.start_time = None
        self.end_time = None
        
    def add_result(self, success: bool, response_time: float, status_code: int, error: str = None):
        self.total_requests += 1
        if success:
            self.successful_requests += 1
            self.response_times.append(response_time)
        else:
            self.failed_requests += 1
            if error:
                self.errors.append(error)
        
        self.status_codes[status_code] = self.status_codes.get(status_code, 0) + 1
    
    def get_summary(self) -> Dict[str, Any]:
        duration = (self.end_time - self.start_time).total_seconds() if self.start_time and self.end_time else 0
        
        return {
            "test_duration_seconds": duration,
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "success_rate_percent": (self.successful_requests / self.total_requests * 100) if self.total_requests > 0 else 0,
            "requests_per_second": self.total_requests / duration if duration > 0 else 0,
            "average_response_time_ms": statistics.mean(self.response_times) * 1000 if self.response_times else 0,
            "median_response_time_ms": statistics.median(self.response_times) * 1000 if self.response_times else 0,
            "min_response_time_ms": min(self.response_times) * 1000 if self.response_times else 0,
            "max_response_time_ms": max(self.response_times) * 1000 if self.response_times else 0,
            "p95_response_time_ms": self._percentile(self.response_times, 95) * 1000 if self.response_times else 0,
            "p99_response_time_ms": self._percentile(self.response_times, 99) * 1000 if self.response_times else 0,
            "status_codes": self.status_codes,
            "error_count": len(self.errors),
            "unique_errors": len(set(self.errors))
        }
    
    def _percentile(self, data: List[float], percentile: float) -> float:
        if not data:
            return 0
        sorted_data = sorted(data)
        index = int((percentile / 100) * len(sorted_data))
        return sorted_data[min(index, len(sorted_data) - 1)]

class StressTester:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.results = StressTestResults()
        
    async def make_request(self, session: aiohttp.ClientSession, endpoint: str) -> Dict[str, Any]:
        """Hacer un request individual y medir el tiempo de respuesta."""
        start_time = time.time()
        
        try:
            headers = {'X-API-Key': self.api_key} if endpoint != '/health' else {}
            url = f"{self.base_url}{endpoint}"
            
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as response:
                response_time = time.time() - start_time
                response_text = await response.text()
                
                success = 200 <= response.status_code < 300
                error = None if success else f"HTTP {response.status_code}: {response_text[:200]}"
                
                self.results.add_result(success, response_time, response.status_code, error)
                
                return {
                    "success": success,
                    "response_time": response_time,
                    "status_code": response.status_code,
                    "response_size": len(response_text),
                    "error": error
                }
                
        except asyncio.TimeoutError:
            response_time = time.time() - start_time
            error = "Request timeout (30s)"
            self.results.add_result(False, response_time, 408, error)
            return {
                "success": False,
                "response_time": response_time,
                "status_code": 408,
                "response_size": 0,
                "error": error
            }
        except Exception as e:
            response_time = time.time() - start_time
            error = f"Request failed: {str(e)}"
            self.results.add_result(False, response_time, 0, error)
            return {
                "success": False,
                "response_time": response_time,
                "status_code": 0,
                "response_size": 0,
                "error": error
            }
    
    async def run_concurrent_requests(self, num_requests: int, concurrent_users: int, endpoint: str):
        """Ejecutar múltiples requests concurrentes."""
        print(f"🚀 Iniciando test de estrés...")
        print(f"   📊 Total requests: {num_requests}")
        print(f"   👥 Usuarios concurrentes: {concurrent_users}")
        print(f"   🎯 Endpoint: {endpoint}")
        print(f"   ⏱️  Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.results.start_time = datetime.now()
        
        # Crear semáforo para limitar concurrencia
        semaphore = asyncio.Semaphore(concurrent_users)
        
        async def limited_request(session):
            async with semaphore:
                return await self.make_request(session, endpoint)
        
        # Crear sesión HTTP
        connector = aiohttp.TCPConnector(limit=concurrent_users * 2)
        timeout = aiohttp.ClientTimeout(total=30)
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            # Crear todas las tareas
            tasks = [limited_request(session) for _ in range(num_requests)]
            
            # Ejecutar todas las tareas concurrentemente
            results = await asyncio.gather(*tasks, return_exceptions=True)
        
        self.results.end_time = datetime.now()
        
        # Procesar excepciones
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                self.results.add_result(False, 0, 0, f"Task exception: {str(result)}")
        
        return results
    
    def print_progress(self, completed: int, total: int):
        """Imprimir progreso del test."""
        percentage = (completed / total) * 100
        bar_length = 50
        filled_length = int(bar_length * completed // total)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        print(f'\r🔄 Progreso: |{bar}| {percentage:.1f}% ({completed}/{total})', end='', flush=True)

class StressTestRunner:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
    
    async def run_test_suite(self):
        """Ejecutar suite completa de tests de estrés."""
        print("🧪 STEEL REBAR PRICE PREDICTOR - STRESS TEST SUITE")
        print("=" * 70)
        print(f"🌐 API URL: {self.base_url}")
        print(f"🔑 API Key: {self.api_key}")
        print(f"🕐 Timestamp: {datetime.now().isoformat()}")
        print("=" * 70)
        
        # Definir tests
        tests = [
            {
                "name": "🏥 Health Check - Test Básico",
                "endpoint": "/health",
                "requests": 100,
                "concurrent_users": 10
            },
            {
                "name": "🎯 Prediction - Test Medio",
                "endpoint": "/predict/steel-rebar-price",
                "requests": 200,
                "concurrent_users": 20
            },
            {
                "name": "🔥 Prediction - Test Intenso",
                "endpoint": "/predict/steel-rebar-price",
                "requests": 500,
                "concurrent_users": 50
            },
            {
                "name": "⚡ Prediction - Test Extremo",
                "endpoint": "/predict/steel-rebar-price",
                "requests": 1000,
                "concurrent_users": 100
            }
        ]
        
        all_results = {}
        
        for i, test in enumerate(tests, 1):
            print(f"\n📋 Test {i}/{len(tests)}: {test['name']}")
            print("-" * 50)
            
            tester = StressTester(self.base_url, self.api_key)
            await tester.run_concurrent_requests(
                test["requests"],
                test["concurrent_users"],
                test["endpoint"]
            )
            
            summary = tester.results.get_summary()
            all_results[test["name"]] = summary
            
            # Imprimir resultados del test
            self.print_test_results(test["name"], summary)
            
            # Pausa entre tests
            if i < len(tests):
                print(f"\n⏸️  Pausa de 10 segundos antes del siguiente test...")
                await asyncio.sleep(10)
        
        # Resumen final
        print("\n" + "=" * 70)
        print("📊 RESUMEN FINAL DE STRESS TESTS")
        print("=" * 70)
        
        for test_name, results in all_results.items():
            print(f"\n{test_name}:")
            print(f"  ✅ Tasa de éxito: {results['success_rate_percent']:.1f}%")
            print(f"  🚀 RPS: {results['requests_per_second']:.1f}")
            print(f"  ⏱️  Tiempo promedio: {results['average_response_time_ms']:.1f}ms")
            print(f"  📈 P95: {results['p95_response_time_ms']:.1f}ms")
        
        # Guardar resultados
        output_file = f"stress_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "api_url": self.base_url,
                "test_results": all_results
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Resultados guardados en: {output_file}")
        
        return all_results
    
    def print_test_results(self, test_name: str, results: Dict[str, Any]):
        """Imprimir resultados de un test individual."""
        print(f"\n📈 Resultados de {test_name}:")
        print(f"  ⏱️  Duración: {results['test_duration_seconds']:.1f}s")
        print(f"  📊 Total requests: {results['total_requests']}")
        print(f"  ✅ Exitosos: {results['successful_requests']}")
        print(f"  ❌ Fallidos: {results['failed_requests']}")
        print(f"  📈 Tasa de éxito: {results['success_rate_percent']:.1f}%")
        print(f"  🚀 Requests/segundo: {results['requests_per_second']:.1f}")
        print(f"  ⏱️  Tiempo respuesta promedio: {results['average_response_time_ms']:.1f}ms")
        print(f"  📊 Tiempo respuesta mediano: {results['median_response_time_ms']:.1f}ms")
        print(f"  ⚡ Tiempo mínimo: {results['min_response_time_ms']:.1f}ms")
        print(f"  🐌 Tiempo máximo: {results['max_response_time_ms']:.1f}ms")
        print(f"  📈 P95: {results['p95_response_time_ms']:.1f}ms")
        print(f"  📈 P99: {results['p99_response_time_ms']:.1f}ms")
        
        if results['status_codes']:
            print(f"  🔢 Códigos de estado: {results['status_codes']}")
        
        if results['error_count'] > 0:
            print(f"  ⚠️  Errores: {results['error_count']} ({results['unique_errors']} únicos)")

async def main():
    """Función principal."""
    parser = argparse.ArgumentParser(description='Stress Test para Steel Rebar Price Predictor API')
    parser.add_argument('--url', default=API_BASE_URL, help='URL de la API')
    parser.add_argument('--key', default=API_KEY, help='API Key')
    parser.add_argument('--quick', action='store_true', help='Ejecutar solo test rápido')
    
    args = parser.parse_args()
    
    runner = StressTestRunner(args.url, args.key)
    
    if args.quick:
        print("🏃 Ejecutando test rápido...")
        tester = StressTester(args.url, args.key)
        await tester.run_concurrent_requests(50, 10, "/predict/steel-rebar-price")
        runner.print_test_results("Test Rápido", tester.results.get_summary())
    else:
        await runner.run_test_suite()

if __name__ == "__main__":
    asyncio.run(main())
