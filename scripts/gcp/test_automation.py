#!/usr/bin/env python3
"""
Script para probar los endpoints de automatización del sistema
"""

import requests
import json
from datetime import datetime
import time

def test_automation_endpoints():
    """Probar todos los endpoints de automatización."""
    
    production_url = "https://steel-rebar-predictor-646072255295.us-central1.run.app"
    api_key = "deacero_steel_predictor_2025_key"
    headers = {"X-API-Key": api_key, "Content-Type": "application/json"}
    
    print("🤖 PRUEBA DE ENDPOINTS DE AUTOMATIZACIÓN")
    print("=" * 60)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 URL: {production_url}")
    print(f"🔑 API Key: {api_key[:20]}...")
    print()
    
    results = {}
    
    # Test 1: Verificar estado de automatización
    print("🔍 TEST 1: Estado de Automatización")
    print("-" * 50)
    
    try:
        response = requests.get(
            f"{production_url}/automation/status",
            headers=headers,
            timeout=15
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ SUCCESS!")
            print(f"   🟢 Estado del sistema: {data.get('system_status', 'N/A')}")
            
            automation_endpoints = data.get('automation_endpoints', {})
            print(f"   📊 Endpoints disponibles:")
            for endpoint, info in automation_endpoints.items():
                status = info.get('status', 'unknown')
                print(f"      {endpoint}: {status}")
            
            scheduled_jobs = data.get('scheduled_jobs', {})
            print(f"   ⏰ Jobs programados:")
            for job, info in scheduled_jobs.items():
                schedule = info.get('schedule', 'N/A')
                status = info.get('status', 'N/A')
                print(f"      {job}: {schedule} ({status})")
            
            results['automation_status'] = True
        else:
            print(f"   ❌ Error: {response.status_code}")
            results['automation_status'] = False
            
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        results['automation_status'] = False
    
    print()
    
    # Test 2: Actualización de datos
    print("📊 TEST 2: Actualización de Datos")
    print("-" * 50)
    
    try:
        response = requests.post(
            f"{production_url}/update-data",
            headers=headers,
            timeout=30
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ SUCCESS!")
            print(f"   📊 Fuentes actualizadas: {data.get('sources_updated', 'N/A')}")
            print(f"   💾 Cache actualizado: {data.get('cache_updated', 'N/A')}")
            print(f"   ⏰ Timestamp: {data.get('timestamp', 'N/A')}")
            
            data_sources = data.get('data_sources', {})
            print(f"   📈 Detalles por fuente:")
            for source, info in data_sources.items():
                records = info.get('records', 'N/A')
                status = info.get('status', 'N/A')
                print(f"      {source}: {records} registros ({status})")
            
            results['update_data'] = True
        else:
            print(f"   ❌ Error: {response.status_code}")
            try:
                error_data = response.json()
                print(f"      Detalles: {error_data}")
            except:
                print(f"      Texto: {response.text[:100]}...")
            results['update_data'] = False
            
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        results['update_data'] = False
    
    print()
    
    # Test 3: Reentrenamiento del modelo
    print("🤖 TEST 3: Reentrenamiento del Modelo")
    print("-" * 50)
    
    try:
        response = requests.post(
            f"{production_url}/retrain-model",
            headers=headers,
            timeout=60  # Más tiempo para reentrenamiento
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ SUCCESS!")
            
            training_data = data.get('training_data', {})
            print(f"   📊 Datos de entrenamiento:")
            print(f"      Total registros: {training_data.get('total_records', 'N/A')}")
            print(f"      Features: {training_data.get('features', 'N/A')}")
            print(f"      Muestras entrenamiento: {training_data.get('training_samples', 'N/A')}")
            
            training_metrics = data.get('training_metrics', {})
            print(f"   📈 Métricas de entrenamiento:")
            print(f"      MAPE: {training_metrics.get('mape', 'N/A')}%")
            print(f"      R²: {training_metrics.get('r2_score', 'N/A')}")
            print(f"      Tiempo entrenamiento: {training_metrics.get('training_time_minutes', 'N/A')} min")
            
            validation_result = data.get('validation_result', {})
            print(f"   ✅ Validación:")
            print(f"      Modelo aceptado: {validation_result.get('model_accepted', 'N/A')}")
            print(f"      Mejora: {validation_result.get('improvement', 'N/A')}")
            
            deployment_result = data.get('deployment_result', {})
            print(f"   🚀 Despliegue:")
            print(f"      Estado: {deployment_result.get('status', 'N/A')}")
            print(f"      Versión: {deployment_result.get('model_version', 'N/A')}")
            
            results['retrain_model'] = True
        else:
            print(f"   ❌ Error: {response.status_code}")
            try:
                error_data = response.json()
                print(f"      Detalles: {error_data}")
            except:
                print(f"      Texto: {response.text[:100]}...")
            results['retrain_model'] = False
            
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        results['retrain_model'] = False
    
    print()
    
    # Test 4: Monitoreo de rendimiento
    print("📊 TEST 4: Monitoreo de Rendimiento")
    print("-" * 50)
    
    try:
        response = requests.post(
            f"{production_url}/monitor-performance",
            headers=headers,
            timeout=30
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ SUCCESS!")
            
            performance_metrics = data.get('performance_metrics', {})
            
            api_perf = performance_metrics.get('api_performance', {})
            print(f"   🌐 Rendimiento de API:")
            print(f"      Tiempo respuesta: {api_perf.get('avg_response_time_ms', 'N/A')} ms")
            print(f"      Requests/hora: {api_perf.get('requests_per_hour', 'N/A')}")
            print(f"      Tasa éxito: {api_perf.get('success_rate', 'N/A')}%")
            
            model_perf = performance_metrics.get('model_performance', {})
            print(f"   🤖 Rendimiento del modelo:")
            print(f"      MAPE actual: {model_perf.get('current_mape', 'N/A')}%")
            print(f"      Confianza: {model_perf.get('confidence_score', 'N/A')}")
            print(f"      Precisión: {model_perf.get('prediction_accuracy', 'N/A')}%")
            
            resource_usage = performance_metrics.get('resource_usage', {})
            print(f"   💻 Uso de recursos:")
            print(f"      CPU: {resource_usage.get('cpu_usage_percent', 'N/A')}%")
            print(f"      Memoria: {resource_usage.get('memory_usage_percent', 'N/A')}%")
            print(f"      Almacenamiento: {resource_usage.get('storage_usage_gb', 'N/A')} GB")
            
            cost_metrics = performance_metrics.get('cost_metrics', {})
            print(f"   💰 Métricas de costo:")
            print(f"      Costo diario: ${cost_metrics.get('daily_cost_usd', 'N/A')} USD")
            print(f"      Proyección mensual: ${cost_metrics.get('monthly_projection_usd', 'N/A')} USD")
            print(f"      Utilización presupuesto: {cost_metrics.get('budget_utilization_percent', 'N/A')}%")
            
            alerts = data.get('alerts', [])
            if alerts:
                print(f"   🚨 Alertas activas:")
                for alert in alerts:
                    alert_type = alert.get('type', 'N/A')
                    severity = alert.get('severity', 'N/A')
                    message = alert.get('message', 'N/A')
                    print(f"      {severity.upper()}: {alert_type} - {message}")
            else:
                print(f"   ✅ Sin alertas activas")
            
            recommendations = data.get('recommendations', [])
            if recommendations:
                print(f"   💡 Recomendaciones:")
                for rec in recommendations:
                    print(f"      - {rec}")
            else:
                print(f"   ✅ Sin recomendaciones")
            
            results['monitor_performance'] = True
        else:
            print(f"   ❌ Error: {response.status_code}")
            try:
                error_data = response.json()
                print(f"      Detalles: {error_data}")
            except:
                print(f"      Texto: {response.text[:100]}...")
            results['monitor_performance'] = False
            
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        results['monitor_performance'] = False
    
    print()
    
    # Resumen final
    print("=" * 60)
    print("📊 RESUMEN DE PRUEBAS DE AUTOMATIZACIÓN")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    
    print(f"🧪 Tests ejecutados: {total_tests}")
    print(f"✅ Tests exitosos: {passed_tests}")
    print(f"❌ Tests fallidos: {total_tests - passed_tests}")
    print(f"📊 Tasa de éxito: {(passed_tests/total_tests)*100:.1f}%")
    print()
    
    print("📋 Detalles por endpoint:")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
    
    print()
    
    if passed_tests == total_tests:
        print("🎉 TODOS LOS TESTS PASARON EXITOSAMENTE")
        print("✅ Sistema de automatización completamente funcional")
    elif passed_tests > 0:
        print("⚠️ ALGUNOS TESTS FALLARON")
        print("📋 Revisar logs y configuración")
    else:
        print("❌ TODOS LOS TESTS FALLARON")
        print("🚨 Sistema de automatización no funcional")
    
    print()
    print("🔗 Próximos pasos:")
    print("   1. Verificar configuración de Cloud Scheduler")
    print("   2. Monitorear logs de ejecución automática")
    print("   3. Configurar alertas de monitoreo")
    print("   4. Revisar métricas de rendimiento")
    
    return results

def main():
    """Función principal."""
    results = test_automation_endpoints()
    
    # Retornar código de salida basado en resultados
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    
    if passed_tests == total_tests:
        print("\n🎉 Pruebas completadas exitosamente")
        return 0
    else:
        print(f"\n⚠️ {total_tests - passed_tests} pruebas fallaron")
        return 1

if __name__ == "__main__":
    exit(main())
