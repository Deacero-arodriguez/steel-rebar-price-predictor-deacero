#!/usr/bin/env python3
"""
Test de estrés simple para diagnosticar problemas con la API.
"""

import asyncio
import aiohttp
import time
import statistics
from datetime import datetime

# URL de la API en GCP
API_BASE_URL = "https://steel-rebar-predictor-646072255295.us-central1.run.app"
API_KEY = "deacero_steel_predictor_2025_key"

async def test_single_request():
    """Test de un solo request para verificar conectividad."""
    print("🔍 Probando conectividad básica...")
    
    try:
        async with aiohttp.ClientSession() as session:
            # Test health check
            print("🏥 Probando health check...")
            async with session.get(f"{API_BASE_URL}/health") as response:
                print(f"   Status: {response.status}")
                text = await response.text()
                print(f"   Response: {text[:200]}...")
            
            # Test prediction
            print("🎯 Probando prediction...")
            headers = {'X-API-Key': API_KEY}
            async with session.get(f"{API_BASE_URL}/predict/steel-rebar-price", headers=headers) as response:
                print(f"   Status: {response.status}")
                text = await response.text()
                print(f"   Response: {text[:200]}...")
                
    except Exception as e:
        print(f"❌ Error: {e}")

async def stress_test_simple(num_requests=10, concurrent=5):
    """Test de estrés simple."""
    print(f"\n🚀 Iniciando test de estrés simple...")
    print(f"   📊 Requests: {num_requests}")
    print(f"   👥 Concurrentes: {concurrent}")
    
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
                        'response_size': len(text)
                    }
                    results.append(result)
                    print(f"✅ Request: {response.status} - {response_time:.3f}s")
                    
            except Exception as e:
                response_time = time.time() - request_start
                result = {
                    'success': False,
                    'status_code': 0,
                    'response_time': response_time,
                    'error': str(e)
                }
                results.append(result)
                print(f"❌ Request falló: {e}")
    
    # Crear sesión y semáforo
    connector = aiohttp.TCPConnector(limit=concurrent * 2)
    timeout = aiohttp.ClientTimeout(total=30)
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        semaphore = asyncio.Semaphore(concurrent)
        
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
    
    print(f"\n📊 RESULTADOS:")
    print(f"   ⏱️  Duración total: {duration:.2f}s")
    print(f"   📊 Total requests: {len(results)}")
    print(f"   ✅ Exitosos: {len(successful)}")
    print(f"   ❌ Fallidos: {len(failed)}")
    print(f"   📈 Tasa de éxito: {len(successful)/len(results)*100:.1f}%")
    print(f"   🚀 RPS: {len(results)/duration:.1f}")
    
    if response_times:
        print(f"   ⏱️  Tiempo promedio: {statistics.mean(response_times)*1000:.1f}ms")
        print(f"   📊 Tiempo mediano: {statistics.median(response_times)*1000:.1f}ms")
        print(f"   ⚡ Tiempo mínimo: {min(response_times)*1000:.1f}ms")
        print(f"   🐌 Tiempo máximo: {max(response_times)*1000:.1f}ms")
    
    if failed:
        print(f"   ⚠️  Errores:")
        for error in failed[:5]:  # Mostrar solo los primeros 5 errores
            print(f"      - {error.get('error', f'Status {error.get('status_code', 'unknown')}')}")

async def main():
    """Función principal."""
    print("🧪 STEEL REBAR PRICE PREDICTOR - STRESS TEST SIMPLE")
    print("=" * 60)
    print(f"🌐 API URL: {API_BASE_URL}")
    print(f"🔑 API Key: {API_KEY}")
    print(f"🕐 Timestamp: {datetime.now().isoformat()}")
    print("=" * 60)
    
    # Test básico
    await test_single_request()
    
    # Test de estrés
    await stress_test_simple(20, 5)

if __name__ == "__main__":
    asyncio.run(main())
