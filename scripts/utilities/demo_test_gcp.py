#!/usr/bin/env python3
"""
Script de demostración para testing de API en GCP
Simula las llamadas sin necesidad de tener la API desplegada
"""

import asyncio
import aiohttp
import time
import json
import os
from datetime import datetime
from typing import List, Dict, Any
import statistics
import random

class DemoAPITester:
    """Simulador de tests de API para demostración."""
    
    def __init__(self):
        self.results = []
        
    async def simulate_api_call(self, request_id: int) -> Dict[str, Any]:
        """Simular una llamada a la API."""
        
        start_time = time.time()
        
        # Simular tiempo de respuesta variable
        response_time = random.uniform(0.2, 1.5)  # 200ms - 1.5s
        await asyncio.sleep(response_time)
        
        # Simular éxito/fallo ocasional
        success = random.random() > 0.05  # 95% de éxito
        
        end_time = time.time()
        actual_response_time = end_time - start_time
        
        if success:
            # Simular respuesta exitosa
            result = {
                "request_id": request_id,
                "timestamp": datetime.now().isoformat(),
                "status_code": 200,
                "response_time_ms": round(actual_response_time * 1000, 2),
                "success": True,
                "url": "https://steel-rebar-predictor-demo-uc.a.run.app/predict/steel-rebar-price",
                "response_data": {
                    "prediction_date": (datetime.now()).strftime("%Y-%m-%d"),
                    "predicted_price_usd_per_ton": round(random.uniform(850, 920), 2),
                    "currency": "USD",
                    "unit": "metric ton",
                    "model_confidence": round(random.uniform(0.75, 0.95), 3),
                    "timestamp": datetime.now().isoformat() + "Z"
                }
            }
            
            result["predicted_price"] = result["response_data"]["predicted_price_usd_per_ton"]
            result["confidence"] = result["response_data"]["model_confidence"]
            result["prediction_date"] = result["response_data"]["prediction_date"]
            
        else:
            # Simular fallo ocasional
            result = {
                "request_id": request_id,
                "timestamp": datetime.now().isoformat(),
                "status_code": 500,
                "response_time_ms": round(actual_response_time * 1000, 2),
                "success": False,
                "url": "https://steel-rebar-predictor-demo-uc.a.run.app/predict/steel-rebar-price",
                "error": "Simulated server error"
            }
        
        return result
    
    async def simulate_health_check(self) -> Dict[str, Any]:
        """Simular health check."""
        
        start_time = time.time()
        await asyncio.sleep(0.1)  # Simular respuesta rápida
        end_time = time.time()
        
        return {
            "endpoint": "health",
            "timestamp": datetime.now().isoformat(),
            "status_code": 200,
            "response_time_ms": round((end_time - start_time) * 1000, 2),
            "success": True,
            "url": "https://steel-rebar-predictor-demo-uc.a.run.app/health",
            "health_data": {
                "status": "healthy",
                "timestamp": datetime.now().isoformat() + "Z",
                "version": "1.0.0",
                "model_trained": True
            }
        }
    
    async def simulate_service_info(self) -> Dict[str, Any]:
        """Simular service info."""
        
        start_time = time.time()
        await asyncio.sleep(0.05)  # Simular respuesta muy rápida
        end_time = time.time()
        
        return {
            "endpoint": "service_info",
            "timestamp": datetime.now().isoformat(),
            "status_code": 200,
            "response_time_ms": round((end_time - start_time) * 1000, 2),
            "success": True,
            "url": "https://steel-rebar-predictor-demo-uc.a.run.app/",
            "service_data": {
                "service": "Steel Rebar Price Predictor",
                "version": "1.0",
                "documentation_url": "https://github.com/Deacero-arodriguez/steel-rebar-price-predictor-deacero",
                "data_sources": ["Yahoo Finance", "Federal Reserve", "World Bank", "IMF", "OECD"],
                "last_model_update": datetime.now().isoformat()
            }
        }
    
    async def run_demo_test(self, num_requests: int = 10) -> Dict[str, Any]:
        """Ejecutar demo de test."""
        
        print(f"🚀 DEMO: Simulando test de {num_requests} llamadas a la API en GCP")
        print(f"📍 URL Demo: https://steel-rebar-predictor-demo-uc.a.run.app")
        print(f"🔑 API Key: deacero_steel_predictor_2025_key...")
        print("-" * 60)
        
        # 1. Test de endpoints básicos
        print("🔍 Simulando endpoints básicos...")
        health_result = await self.simulate_health_check()
        service_info_result = await self.simulate_service_info()
        
        print(f"   Health Check: {'✅' if health_result['success'] else '❌'} "
              f"({health_result['response_time_ms']}ms)")
        print(f"   Service Info: {'✅' if service_info_result['success'] else '❌'} "
              f"({service_info_result['response_time_ms']}ms)")
        
        # 2. Test de predicciones
        print(f"\n📊 Simulando {num_requests} llamadas de predicción...")
        
        start_time = time.time()
        
        # Crear tareas para las llamadas concurrentes
        tasks = []
        for i in range(num_requests):
            task = self.simulate_api_call(i + 1)
            tasks.append(task)
        
        # Ejecutar todas las llamadas
        results = await asyncio.gather(*tasks)
        
        total_time = time.time() - start_time
        
        # Procesar resultados
        successful_requests = [r for r in results if r["success"]]
        failed_requests = [r for r in results if not r["success"]]
        
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
    
    def print_demo_results(self, stats: Dict[str, Any]):
        """Imprimir resultados del demo."""
        
        print("\n" + "="*60)
        print("📋 DEMO - RESUMEN DEL TEST DE API EN GCP")
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
        
        print(f"\n🎭 NOTA: Este es un DEMO simulando el comportamiento real")
        print(f"   Para tests reales, usa: python test_api_gcp.py [URL_REAL]")
    
    def save_demo_results(self, stats: Dict[str, Any]):
        """Guardar resultados del demo."""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"demo_test_results_{timestamp}.json"
        filepath = os.path.join("data", "predictions", filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Resultados del demo guardados en: {filepath}")

async def main():
    """Función principal del demo."""
    
    print("🎭 DEMO DE TEST DE API EN GCP")
    print("Este script simula el comportamiento del test real")
    print("Para usar con API real, ejecuta: python test_api_gcp.py [URL]")
    print("-" * 60)
    
    # Crear instancia del demo tester
    demo_tester = DemoAPITester()
    
    try:
        # Ejecutar demo
        stats = await demo_tester.run_demo_test(10)
        
        # Mostrar resultados
        demo_tester.print_demo_results(stats)
        
        # Guardar resultados
        demo_tester.save_demo_results(stats)
        
        print(f"\n🎉 DEMO COMPLETADO")
        print(f"   Para usar con tu API real:")
        print(f"   1. Despliega tu API en GCP")
        print(f"   2. Ejecuta: python test_api_gcp.py [TU-URL]")
        
    except KeyboardInterrupt:
        print("\n⏹️  Demo interrumpido por el usuario")
    except Exception as e:
        print(f"\n💥 Error inesperado en demo: {e}")

if __name__ == "__main__":
    asyncio.run(main())
