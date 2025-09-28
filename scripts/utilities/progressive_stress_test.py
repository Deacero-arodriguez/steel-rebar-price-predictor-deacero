#!/usr/bin/env python3
"""
Test de estrés progresivo para la API de Steel Rebar Price Predictor.
Aumenta gradualmente la carga para encontrar los límites de la API.
"""

import asyncio
import aiohttp
import time
import statistics
from datetime import datetime
import json

# URL de la API en GCP
API_BASE_URL = "https://steel-rebar-predictor-646072255295.us-central1.run.app"
API_KEY = "deacero_steel_predictor_2025_key"

class ProgressiveStressTester:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        
    async def run_stress_level(self, level_name: str, num_requests: int, concurrent_users: int, endpoint: str = "/predict/steel-rebar-price"):
        """Ejecutar un nivel específico de estrés."""
        print(f"\n🔥 {level_name}")
        print(f"   📊 Requests: {num_requests}")
        print(f"   👥 Concurrentes: {concurrent_users}")
        print(f"   🎯 Endpoint: {endpoint}")
        
        results = []
        start_time = time.time()
        
        async def make_request(session, semaphore):
            async with semaphore:
                request_start = time.time()
                try:
                    headers = {'X-API-Key': self.api_key} if endpoint != '/health' else {}
                    async with session.get(f"{self.base_url}{endpoint}", headers=headers) as response:
                        response_time = time.time() - request_start
                        text = await response.text()
                        
                        result = {
                            'success': response.status == 200,
                            'status_code': response.status,
                            'response_time': response_time,
                            'response_size': len(text),
                            'timestamp': request_start
                        }
                        results.append(result)
                        
                except Exception as e:
                    response_time = time.time() - request_start
                    result = {
                        'success': False,
                        'status_code': 0,
                        'response_time': response_time,
                        'error': str(e),
                        'timestamp': request_start
                    }
                    results.append(result)
        
        # Configurar sesión HTTP
        connector = aiohttp.TCPConnector(limit=concurrent_users * 3)
        timeout = aiohttp.ClientTimeout(total=60)
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            semaphore = asyncio.Semaphore(concurrent_users)
            
            # Crear tareas
            tasks = [make_request(session, semaphore) for _ in range(num_requests)]
            
            # Ejecutar
            await asyncio.gather(*tasks)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Analizar resultados
        successful = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]
        
        response_times = [r['response_time'] for r in successful]
        
        # Calcular métricas
        success_rate = len(successful) / len(results) * 100 if results else 0
        rps = len(results) / duration if duration > 0 else 0
        
        avg_response_time = statistics.mean(response_times) * 1000 if response_times else 0
        median_response_time = statistics.median(response_times) * 1000 if response_times else 0
        min_response_time = min(response_times) * 1000 if response_times else 0
        max_response_time = max(response_times) * 1000 if response_times else 0
        
        # P95 y P99
        p95 = self._percentile(response_times, 95) * 1000 if response_times else 0
        p99 = self._percentile(response_times, 99) * 1000 if response_times else 0
        
        # Códigos de estado
        status_codes = {}
        for result in results:
            code = result.get('status_code', 0)
            status_codes[code] = status_codes.get(code, 0) + 1
        
        # Errores únicos
        errors = [r.get('error', '') for r in failed if 'error' in r]
        unique_errors = len(set(errors))
        
        summary = {
            'level_name': level_name,
            'duration_seconds': duration,
            'total_requests': len(results),
            'successful_requests': len(successful),
            'failed_requests': len(failed),
            'success_rate_percent': success_rate,
            'requests_per_second': rps,
            'average_response_time_ms': avg_response_time,
            'median_response_time_ms': median_response_time,
            'min_response_time_ms': min_response_time,
            'max_response_time_ms': max_response_time,
            'p95_response_time_ms': p95,
            'p99_response_time_ms': p99,
            'status_codes': status_codes,
            'error_count': len(errors),
            'unique_errors': unique_errors
        }
        
        # Imprimir resultados
        print(f"   ⏱️  Duración: {duration:.2f}s")
        print(f"   ✅ Exitosos: {len(successful)}")
        print(f"   ❌ Fallidos: {len(failed)}")
        print(f"   📈 Tasa de éxito: {success_rate:.1f}%")
        print(f"   🚀 RPS: {rps:.1f}")
        print(f"   ⏱️  Tiempo promedio: {avg_response_time:.1f}ms")
        print(f"   📈 P95: {p95:.1f}ms")
        print(f"   📈 P99: {p99:.1f}ms")
        
        if status_codes:
            print(f"   🔢 Códigos: {status_codes}")
        
        if errors:
            print(f"   ⚠️  Errores: {len(errors)} ({unique_errors} únicos)")
        
        return summary
    
    def _percentile(self, data, percentile):
        if not data:
            return 0
        sorted_data = sorted(data)
        index = int((percentile / 100) * len(sorted_data))
        return sorted_data[min(index, len(sorted_data) - 1)]
    
    async def run_progressive_test(self):
        """Ejecutar test progresivo completo."""
        print("🚀 STEEL REBAR PRICE PREDICTOR - PROGRESSIVE STRESS TEST")
        print("=" * 70)
        print(f"🌐 API URL: {self.base_url}")
        print(f"🔑 API Key: {self.api_key}")
        print(f"🕐 Timestamp: {datetime.now().isoformat()}")
        print("=" * 70)
        
        # Definir niveles de estrés progresivos
        stress_levels = [
            {
                "name": "🟢 Test Básico",
                "requests": 50,
                "concurrent": 10,
                "endpoint": "/health"
            },
            {
                "name": "🟡 Test Ligero",
                "requests": 100,
                "concurrent": 20,
                "endpoint": "/predict/steel-rebar-price"
            },
            {
                "name": "🟠 Test Medio",
                "requests": 200,
                "concurrent": 40,
                "endpoint": "/predict/steel-rebar-price"
            },
            {
                "name": "🔴 Test Intenso",
                "requests": 500,
                "concurrent": 80,
                "endpoint": "/predict/steel-rebar-price"
            },
            {
                "name": "🔥 Test Extremo",
                "requests": 1000,
                "concurrent": 150,
                "endpoint": "/predict/steel-rebar-price"
            }
        ]
        
        all_results = []
        
        for i, level in enumerate(stress_levels, 1):
            print(f"\n📋 Nivel {i}/{len(stress_levels)}")
            
            result = await self.run_stress_level(
                level["name"],
                level["requests"],
                level["concurrent"],
                level["endpoint"]
            )
            
            all_results.append(result)
            
            # Verificar si debemos continuar
            if result['success_rate_percent'] < 95:
                print(f"\n⚠️  Tasa de éxito baja ({result['success_rate_percent']:.1f}%)")
                print("🛑 Considerando detener el test...")
                
                # Preguntar si continuar (en un entorno real, podrías automatizar esto)
                if result['success_rate_percent'] < 80:
                    print("🛑 Tasa de éxito muy baja, deteniendo test")
                    break
            
            # Pausa entre niveles
            if i < len(stress_levels):
                print(f"\n⏸️  Pausa de 15 segundos antes del siguiente nivel...")
                await asyncio.sleep(15)
        
        # Resumen final
        print("\n" + "=" * 70)
        print("📊 RESUMEN FINAL DEL TEST PROGRESIVO")
        print("=" * 70)
        
        for result in all_results:
            print(f"\n{result['level_name']}:")
            print(f"  📈 Tasa de éxito: {result['success_rate_percent']:.1f}%")
            print(f"  🚀 RPS: {result['requests_per_second']:.1f}")
            print(f"  ⏱️  Tiempo promedio: {result['average_response_time_ms']:.1f}ms")
            print(f"  📈 P95: {result['p95_response_time_ms']:.1f}ms")
        
        # Análisis de rendimiento
        print(f"\n🔍 ANÁLISIS DE RENDIMIENTO:")
        
        # Encontrar el mejor rendimiento
        best_rps = max([r['requests_per_second'] for r in all_results])
        best_result = next(r for r in all_results if r['requests_per_second'] == best_rps)
        print(f"  🏆 Mejor RPS: {best_rps:.1f} ({best_result['level_name']})")
        
        # Encontrar el punto de quiebre
        for i, result in enumerate(all_results):
            if result['success_rate_percent'] < 95:
                print(f"  ⚠️  Punto de quiebre: {result['level_name']} ({result['success_rate_percent']:.1f}%)")
                if i > 0:
                    previous = all_results[i-1]
                    print(f"  📊 RPS en quiebre: {result['requests_per_second']:.1f}")
                    print(f"  📊 RPS estable anterior: {previous['requests_per_second']:.1f}")
                break
        else:
            print(f"  ✅ API mantuvo >95% de éxito en todos los niveles")
        
        # Guardar resultados
        output_file = f"progressive_stress_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "api_url": self.base_url,
                "test_results": all_results,
                "summary": {
                    "best_rps": best_rps,
                    "best_level": best_result['level_name'],
                    "total_levels_tested": len(all_results)
                }
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Resultados guardados en: {output_file}")
        
        return all_results

async def main():
    """Función principal."""
    tester = ProgressiveStressTester(API_BASE_URL, API_KEY)
    await tester.run_progressive_test()

if __name__ == "__main__":
    asyncio.run(main())
