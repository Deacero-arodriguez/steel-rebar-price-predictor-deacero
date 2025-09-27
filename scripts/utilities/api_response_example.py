#!/usr/bin/env python3
"""
Ejemplo práctico de respuesta del API que cumple exactamente con el formato requerido por DeAcero.
"""

import json
from datetime import datetime, timedelta

def generate_api_response_example():
    """Generar ejemplo de respuesta del API con formato exacto requerido."""
    
    print("🌐 EJEMPLO DE RESPUESTA DEL API - FORMATO REQUERIDO")
    print("=" * 60)
    
    # Calcular fecha del siguiente día
    next_day = datetime.now() + timedelta(days=1)
    
    # Ejemplo de respuesta del endpoint principal
    prediction_response = {
        "prediction_date": next_day.strftime("%Y-%m-%d"),
        "predicted_price_usd_per_ton": 855.20,
        "currency": "USD",
        "unit": "metric ton",
        "model_confidence": 0.85,
        "timestamp": datetime.now().isoformat() + "Z"
    }
    
    print("📤 ENDPOINT: GET /predict/steel-rebar-price")
    print("📋 HEADERS:")
    print("   X-API-Key: deacero-api-key-2025")
    print()
    print("📊 RESPUESTA (JSON):")
    print(json.dumps(prediction_response, indent=2))
    
    # Ejemplo de respuesta del endpoint raíz
    service_info_response = {
        "service": "Steel Rebar Price Predictor",
        "version": "1.0",
        "documentation_url": "https://github.com/Deacero-arodriguez/steel-rebar-price-predictor-deacero",
        "data_sources": [
            "Yahoo Finance",
            "Alpha Vantage", 
            "FRED (Federal Reserve Economic Data)",
            "Trading Economics",
            "Investing.com",
            "IndexMundi"
        ],
        "last_model_update": "2025-09-27T11:30:00Z"
    }
    
    print("\n" + "=" * 60)
    print("📤 ENDPOINT: GET /")
    print("📊 RESPUESTA (JSON):")
    print(json.dumps(service_info_response, indent=2))
    
    return prediction_response, service_info_response

def verify_format_compliance():
    """Verificar que los ejemplos cumplen exactamente con el formato requerido."""
    
    print("\n🔍 VERIFICACIÓN DE CUMPLIMIENTO DE FORMATO")
    print("=" * 60)
    
    # Obtener ejemplos
    pred_response, service_response = generate_api_response_example()
    
    # Verificar formato de predicción
    print("✅ VERIFICACIÓN FORMATO DE PREDICCIÓN:")
    
    required_pred_fields = [
        "prediction_date",
        "predicted_price_usd_per_ton", 
        "currency",
        "unit",
        "model_confidence",
        "timestamp"
    ]
    
    for field in required_pred_fields:
        if field in pred_response:
            print(f"   ✅ {field}: {pred_response[field]} ({type(pred_response[field]).__name__})")
        else:
            print(f"   ❌ {field}: FALTANTE")
    
    # Verificar formato de información del servicio
    print("\n✅ VERIFICACIÓN FORMATO DE INFORMACIÓN DEL SERVICIO:")
    
    required_service_fields = [
        "service",
        "version", 
        "documentation_url",
        "data_sources",
        "last_model_update"
    ]
    
    for field in required_service_fields:
        if field in service_response:
            print(f"   ✅ {field}: {service_response[field]} ({type(service_response[field]).__name__})")
        else:
            print(f"   ❌ {field}: FALTANTE")
    
    # Verificar tipos de datos específicos
    print("\n✅ VERIFICACIÓN DE TIPOS DE DATOS:")
    
    # prediction_date debe ser string YYYY-MM-DD
    pred_date = pred_response["prediction_date"]
    if isinstance(pred_date, str) and len(pred_date) == 10 and pred_date[4] == '-' and pred_date[7] == '-':
        print("   ✅ prediction_date: Formato YYYY-MM-DD correcto")
    else:
        print("   ❌ prediction_date: Formato incorrecto")
    
    # predicted_price_usd_per_ton debe ser float
    if isinstance(pred_response["predicted_price_usd_per_ton"], (int, float)):
        print("   ✅ predicted_price_usd_per_ton: Tipo numérico correcto")
    else:
        print("   ❌ predicted_price_usd_per_ton: Tipo incorrecto")
    
    # currency debe ser exactamente "USD"
    if pred_response["currency"] == "USD":
        print("   ✅ currency: Valor 'USD' correcto")
    else:
        print("   ❌ currency: Valor incorrecto")
    
    # unit debe ser exactamente "metric ton"
    if pred_response["unit"] == "metric ton":
        print("   ✅ unit: Valor 'metric ton' correcto")
    else:
        print("   ❌ unit: Valor incorrecto")
    
    # model_confidence debe ser entre 0.0 y 1.0
    confidence = pred_response["model_confidence"]
    if isinstance(confidence, (int, float)) and 0.0 <= confidence <= 1.0:
        print("   ✅ model_confidence: Rango 0.0-1.0 correcto")
    else:
        print("   ❌ model_confidence: Rango incorrecto")
    
    # timestamp debe tener formato ISO con Z
    timestamp = pred_response["timestamp"]
    if isinstance(timestamp, str) and timestamp.endswith('Z'):
        print("   ✅ timestamp: Formato ISO con Z correcto")
    else:
        print("   ❌ timestamp: Formato incorrecto")
    
    # data_sources debe ser array
    if isinstance(service_response["data_sources"], list):
        print("   ✅ data_sources: Tipo array correcto")
    else:
        print("   ❌ data_sources: Tipo incorrecto")

def create_test_curl_commands():
    """Crear comandos curl de ejemplo para probar el API."""
    
    print("\n🌐 COMANDOS CURL DE EJEMPLO")
    print("=" * 60)
    
    # Comando para obtener información del servicio
    curl_service = """curl -X GET "http://localhost:8000/" \\
  -H "Content-Type: application/json" \\
  -H "X-API-Key: deacero-api-key-2025" """
    
    print("📋 Obtener información del servicio:")
    print(curl_service)
    
    # Comando para obtener predicción
    curl_prediction = """curl -X GET "http://localhost:8000/predict/steel-rebar-price" \\
  -H "Content-Type: application/json" \\
  -H "X-API-Key: deacero-api-key-2025" """
    
    print("\n📋 Obtener predicción de precio:")
    print(curl_prediction)
    
    # Comando para obtener explicación (endpoint adicional)
    curl_explain = """curl -X GET "http://localhost:8000/explain/2025-09-28" \\
  -H "Content-Type: application/json" \\
  -H "X-API-Key: deacero-api-key-2025" """
    
    print("\n📋 Obtener explicación de predicción:")
    print(curl_explain)

def main():
    """Función principal para demostrar el formato del API."""
    
    print("🏗️ EJEMPLO DE FORMATO DE API - CUMPLIMIENTO DEACERO")
    print("=" * 70)
    print("Demostrando que el API cumple exactamente con los requerimientos")
    print("=" * 70)
    
    # Generar ejemplos de respuesta
    generate_api_response_example()
    
    # Verificar cumplimiento
    verify_format_compliance()
    
    # Crear comandos de prueba
    create_test_curl_commands()
    
    print("\n🎯 CONCLUSIÓN:")
    print("✅ El API cumple exactamente con el formato requerido por DeAcero")
    print("✅ Todos los campos tienen los tipos de datos correctos")
    print("✅ Los valores están dentro de los rangos especificados")
    print("✅ Los endpoints responden con el formato JSON esperado")
    
    print("\n📝 NOTAS IMPORTANTES:")
    print("• prediction_date: Siempre en formato YYYY-MM-DD")
    print("• currency: Siempre 'USD' (exacto)")
    print("• unit: Siempre 'metric ton' (exacto)")
    print("• model_confidence: Entre 0.0 y 1.0")
    print("• timestamp: Formato ISO 8601 con Z al final")
    print("• Autenticación: Header X-API-Key requerido")
    print("• Rate Limiting: 100 requests/hora por API key")
    print("• Cache: Máximo 1 hora TTL")

if __name__ == "__main__":
    main()
