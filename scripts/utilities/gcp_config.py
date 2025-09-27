#!/usr/bin/env python3
"""
Configuración para tests de GCP
"""

import os
from typing import Dict, Any

# Configuración de GCP
GCP_CONFIG = {
    # Reemplazar con tu Project ID real
    "PROJECT_ID": "deacero-steel-predictor",  # Cambiar por tu project ID
    
    # Configuración del servicio
    "SERVICE_NAME": "steel-rebar-predictor",
    "REGION": "us-central1",
    
    # API Key
    "API_KEY": "deacero_steel_predictor_2025_key",
    
    # URLs (se generan automáticamente)
    "SERVICE_URL": None,  # Se genera después del deployment
    
    # Configuración de tests
    "TEST_CONFIG": {
        "NUM_REQUESTS": 10,
        "TIMEOUT_SECONDS": 30,
        "MAX_RETRIES": 3,
        "CONCURRENT_REQUESTS": 5
    }
}

def get_project_id() -> str:
    """Obtener Project ID desde configuración o variable de entorno."""
    
    # Prioridad: variable de entorno > configuración
    return os.getenv('GCP_PROJECT_ID', GCP_CONFIG["PROJECT_ID"])

def get_service_url(project_id: str = None) -> str:
    """Generar URL del servicio Cloud Run."""
    
    if project_id is None:
        project_id = get_project_id()
    
    service_name = GCP_CONFIG["SERVICE_NAME"]
    region = GCP_CONFIG["REGION"]
    
    return f"https://{service_name}-{project_id}-{region}.a.run.app"

def get_api_key() -> str:
    """Obtener API Key."""
    return GCP_CONFIG["API_KEY"]

def get_test_config() -> Dict[str, Any]:
    """Obtener configuración de tests."""
    return GCP_CONFIG["TEST_CONFIG"].copy()

def validate_config() -> bool:
    """Validar configuración."""
    
    project_id = get_project_id()
    
    if project_id == "deacero-steel-predictor":
        print("⚠️  ADVERTENCIA: Usando Project ID por defecto")
        print("   Cambia 'PROJECT_ID' en gcp_config.py por tu Project ID real")
        return False
    
    return True

def print_config():
    """Imprimir configuración actual."""
    
    print("📋 CONFIGURACIÓN DE GCP")
    print("=" * 30)
    print(f"   Project ID: {get_project_id()}")
    print(f"   Service Name: {GCP_CONFIG['SERVICE_NAME']}")
    print(f"   Region: {GCP_CONFIG['REGION']}")
    print(f"   Service URL: {get_service_url()}")
    print(f"   API Key: {get_api_key()[:20]}...")
    print(f"   Test Requests: {GCP_CONFIG['TEST_CONFIG']['NUM_REQUESTS']}")
    
    if not validate_config():
        print("\n⚠️  RECUERDA: Actualizar PROJECT_ID en este archivo")

if __name__ == "__main__":
    print_config()
