#!/usr/bin/env python3
"""
Script para verificar el formato exacto de respuesta de la API
"""

import requests
import json

def check_api_response_format():
    """Verificar el formato de respuesta de la API."""
    
    api_url = "https://steel-rebar-predictor-646072255295.us-central1.run.app"
    api_key = "deacero_steel_predictor_2025_key"
    
    print("🔍 Verificando formato de respuesta de la API...")
    print(f"URL: {api_url}")
    print()
    
    try:
        headers = {"X-API-Key": api_key}
        
        # Verificar endpoint raíz
        print("📋 Endpoint raíz (GET /):")
        response = requests.get(f"{api_url}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Formato correcto:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(f"❌ Error: {response.status_code}")
        
        print("\n" + "="*60 + "\n")
        
        # Verificar endpoint de predicción
        print("🎯 Endpoint de predicción (GET /predict/steel-rebar-price):")
        response = requests.get(f"{api_url}/predict/steel-rebar-price", headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Formato correcto:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            # Verificar campos requeridos según el contexto técnico
            required_fields = [
                "prediction_date",
                "predicted_price_usd_per_ton", 
                "currency",
                "unit",
                "model_confidence",
                "timestamp"
            ]
            
            print("\n🔍 Verificación de campos requeridos:")
            for field in required_fields:
                if field in data:
                    print(f"✅ {field}: {data[field]}")
                else:
                    print(f"❌ {field}: FALTANTE")
                    
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_api_response_format()
