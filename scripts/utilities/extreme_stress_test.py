#!/usr/bin/env python3
"""
Test de estrés extremo para encontrar los límites reales de la API.
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

async def extreme_stress_test():
    """Test de estrés extremo para encontrar límites."""
    print("🔥 EXTREME STRESS TEST - STEEL REBAR PRICE PREDICTOR")
    print("=" * 70)
    print(f"🌐 API URL: {API_BASE_URL}")
    print(f"🕐 Timestamp: {datetime.now().isoformat()}")
    print("=" * 70)
    
    # Test extremo: 2000 requests con 300 usuarios concurrentes
    num_requests = 2000
    concurrent_users = 300
    
    print(f"\n🚀 Test Extremo:")
    print(f"   📊 Requests: {num_requests}")
    print(f"   👥 Concurrentes: {concurrent_users}")
    print(f"   🎯 Endpoint: /predict/steel-rebar-price")
    
    results = []
    start_time = time.time()
    
    async def make_request(session, semaphore):
        async with semaphore:
            request_start = time.time()
            try:
                headers = {'X-API-Key': API_KEY}
                async with session.get(f"{API_BASE_URL}/predict/steel-rebar-price", headers=headers) as response:
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
    
    # Configurar sesión HTTP con límites altos
    connector = aiohttp.TCPConnector(limit=concurrent_users * 5)
    timeout = aiohttp.ClientTimeout(total=120)
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        semaphore = asyncio.Semaphore(concurrent_users)
        
        # Crear tareas
        tasks = [make_request(session, semaphore) for _ in range(num_requests)]
        
        # Ejecutar
        print(f"\n⏳ Ejecutando {num_requests} requests...")
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
    def percentile(data, p):
        if not data:
            return 0
        sorted_data = sorted(data)
        index = int((p / 100) * len(sorted_data))
        return sorted_data[min(index, len(sorted_data) - 1)]
    
    p95 = percentile(response_times, 95) * 1000 if response_times else 0
    p99 = percentile(response_times, 99) * 1000 if response_times else 0
    
    # Códigos de estado
    status_codes = {}
    for result in results:
        code = result.get('status_code', 0)
        status_codes[code] = status_codes.get(code, 0) + 1
    
    # Errores
    errors = [r.get('error', '') for r in failed if 'error' in r]
    unique_errors = len(set(errors))
    
    # Imprimir resultados
    print(f"\n📊 RESULTADOS DEL TEST EXTREMO:")
    print(f"   ⏱️  Duración total: {duration:.2f}s")
    print(f"   📊 Total requests: {len(results)}")
    print(f"   ✅ Exitosos: {len(successful)}")
    print(f"   ❌ Fallidos: {len(failed)}")
    print(f"   📈 Tasa de éxito: {success_rate:.1f}%")
    print(f"   🚀 RPS promedio: {rps:.1f}")
    print(f"   ⏱️  Tiempo promedio: {avg_response_time:.1f}ms")
    print(f"   📊 Tiempo mediano: {median_response_time:.1f}ms")
    print(f"   ⚡ Tiempo mínimo: {min_response_time:.1f}ms")
    print(f"   🐌 Tiempo máximo: {max_response_time:.1f}ms")
    print(f"   📈 P95: {p95:.1f}ms")
    print(f"   📈 P99: {p99:.1f}ms")
    
    if status_codes:
        print(f"   🔢 Códigos de estado: {status_codes}")
    
    if errors:
        print(f"   ⚠️  Errores: {len(errors)} ({unique_errors} únicos)")
        # Mostrar algunos errores de ejemplo
        for error in list(set(errors))[:3]:
            print(f"      - {error}")
    
    # Análisis de rendimiento
    print(f"\n🔍 ANÁLISIS DE RENDIMIENTO:")
    
    if success_rate >= 99:
        print(f"   🏆 EXCELENTE: API manejó {success_rate:.1f}% de éxito en test extremo")
    elif success_rate >= 95:
        print(f"   ✅ BUENO: API manejó {success_rate:.1f}% de éxito en test extremo")
    elif success_rate >= 90:
        print(f"   ⚠️  ACEPTABLE: API manejó {success_rate:.1f}% de éxito en test extremo")
    else:
        print(f"   ❌ PROBLEMAS: API solo manejó {success_rate:.1f}% de éxito en test extremo")
    
    if rps >= 1000:
        print(f"   🚀 ALTO RENDIMIENTO: {rps:.1f} requests/segundo")
    elif rps >= 500:
        print(f"   📈 BUEN RENDIMIENTO: {rps:.1f} requests/segundo")
    else:
        print(f"   📊 RENDIMIENTO MODERADO: {rps:.1f} requests/segundo")
    
    if p95 <= 500:
        print(f"   ⚡ TIEMPO DE RESPUESTA EXCELENTE: P95 = {p95:.1f}ms")
    elif p95 <= 1000:
        print(f"   ✅ TIEMPO DE RESPUESTA BUENO: P95 = {p95:.1f}ms")
    else:
        print(f"   ⚠️  TIEMPO DE RESPUESTA LENTO: P95 = {p95:.1f}ms")
    
    # Guardar resultados
    output_file = f"extreme_stress_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "api_url": API_BASE_URL,
            "test_type": "extreme_stress",
            "parameters": {
                "total_requests": num_requests,
                "concurrent_users": concurrent_users
            },
            "results": {
                "duration_seconds": duration,
                "total_requests": len(results),
                "successful_requests": len(successful),
                "failed_requests": len(failed),
                "success_rate_percent": success_rate,
                "requests_per_second": rps,
                "average_response_time_ms": avg_response_time,
                "median_response_time_ms": median_response_time,
                "min_response_time_ms": min_response_time,
                "max_response_time_ms": max_response_time,
                "p95_response_time_ms": p95,
                "p99_response_time_ms": p99,
                "status_codes": status_codes,
                "error_count": len(errors),
                "unique_errors": unique_errors
            }
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados guardados en: {output_file}")
    
    return {
        "success_rate": success_rate,
        "rps": rps,
        "p95": p95,
        "total_requests": len(results),
        "duration": duration
    }

async def main():
    """Función principal."""
    await extreme_stress_test()

if __name__ == "__main__":
    asyncio.run(main())
