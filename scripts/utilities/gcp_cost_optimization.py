#!/usr/bin/env python3
"""
Script para optimización de costos GCP y monitoreo de presupuesto.
"""

import subprocess
import json
from datetime import datetime, timedelta
import os

class GCPCostOptimizer:
    """Optimizador de costos para GCP."""
    
    def __init__(self, project_id="steel-rebar-predictor-deacero"):
        self.project_id = project_id
        self.billing_account = "01F48F-7401CC-A937E9"
    
    def create_budget_alert(self, budget_amount=5.0):
        """Crear alerta de presupuesto."""
        
        budget_config = {
            "budget": {
                "displayName": "Steel Rebar Predictor Budget",
                "budgetFilter": {
                    "projects": [f"projects/{self.project_id}"]
                },
                "amount": {
                    "specifiedAmount": {
                        "currencyCode": "USD",
                        "units": str(int(budget_amount)),
                        "nanos": int((budget_amount - int(budget_amount)) * 1000000000)
                    }
                },
                "thresholdRules": [
                    {
                        "thresholdPercent": 0.5,  # 50% del presupuesto
                        "spendBasis": "CURRENT_SPEND"
                    },
                    {
                        "thresholdPercent": 0.8,  # 80% del presupuesto
                        "spendBasis": "CURRENT_SPEND"
                    },
                    {
                        "thresholdPercent": 0.95,  # 95% del presupuesto
                        "spendBasis": "CURRENT_SPEND"
                    }
                ]
            }
        }
        
        # Crear archivo temporal
        budget_file = "temp_budget.json"
        with open(budget_file, 'w') as f:
            json.dump(budget_config, f, indent=2)
        
        try:
            # Crear presupuesto
            cmd = [
                "gcloud", "billing", "budgets", "create",
                "--billing-account", self.billing_account,
                "--budget-file", budget_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Presupuesto de ${budget_amount} USD creado exitosamente")
                print("🔔 Alertas configuradas en 50%, 80% y 95% del presupuesto")
            else:
                print(f"❌ Error creando presupuesto: {result.stderr}")
                
        finally:
            # Limpiar archivo temporal
            if os.path.exists(budget_file):
                os.remove(budget_file)
    
    def optimize_cloud_run_config(self):
        """Optimizar configuración de Cloud Run."""
        
        optimizations = [
            {
                "name": "Reducir CPU a 0.5 y memoria a 512Mi",
                "command": [
                    "gcloud", "run", "services", "update", "steel-rebar-predictor",
                    "--region=us-central1",
                    "--cpu=0.5",
                    "--memory=512Mi",
                    "--max-instances=5",
                    "--min-instances=0"
                ]
            },
            {
                "name": "Configurar timeout más corto",
                "command": [
                    "gcloud", "run", "services", "update", "steel-rebar-predictor",
                    "--region=us-central1",
                    "--timeout=30s"
                ]
            }
        ]
        
        print("🔧 Aplicando optimizaciones de Cloud Run...")
        
        for opt in optimizations:
            print(f"\n📝 {opt['name']}...")
            result = subprocess.run(opt['command'], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {opt['name']} aplicado exitosamente")
            else:
                print(f"❌ Error en {opt['name']}: {result.stderr}")
    
    def get_current_usage(self):
        """Obtener uso actual de recursos."""
        
        print("📊 USO ACTUAL DE RECURSOS GCP")
        print("=" * 50)
        
        # Cloud Run
        print("\n🚀 Cloud Run:")
        cmd = ["gcloud", "run", "services", "describe", "steel-rebar-predictor", 
               "--region=us-central1", "--format=table(status.conditions)"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(result.stdout)
        
        # Container Registry
        print("\n📦 Container Registry:")
        cmd = ["gcloud", "container", "images", "list", 
               "--repository=gcr.io/steel-rebar-predictor-deacero"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(result.stdout)
        
        # Cloud Build
        print("\n🏗️ Cloud Build:")
        cmd = ["gcloud", "builds", "list", "--limit=5", 
               "--format=table(id,status,createTime)"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(result.stdout)
    
    def estimate_monthly_cost(self):
        """Estimar costo mensual."""
        
        print("\n💰 ESTIMACIÓN DE COSTOS MENSUALES")
        print("=" * 50)
        
        estimates = {
            "Cloud Run (Optimizado)": {
                "CPU": "0.5 vCPU * 24h * 30d * $0.024/vCPU-h = $8.64",
                "Memory": "512Mi * 24h * 30d * $0.0025/GiB-h = $0.92",
                "Requests": "1000 requests/día * 30d * $0.40/1M requests = $0.01",
                "Subtotal": "$9.57"
            },
            "Container Registry": {
                "Storage": "0.5GB * $0.026/GB/mes = $0.01",
                "Subtotal": "$0.01"
            },
            "Cloud Build": {
                "Builds": "10 builds/mes * $0.003/min = $0.03",
                "Subtotal": "$0.03"
            },
            "TOTAL ESTIMADO": "$9.61"
        }
        
        print("\n📊 COMPARACIÓN DE COSTOS:")
        print("Configuración Actual (1 CPU, 1GiB): ~$18.50/mes")
        print("Configuración Optimizada (0.5 CPU, 512MiB): ~$9.61/mes")
        print("💰 AHORRO: ~$8.89/mes (48% reducción)")
        
        print(f"\n🎯 PRESUPUESTO REQUERIDO: $5.00 USD/mes")
        print(f"📊 COSTO ESTIMADO: $9.61 USD/mes")
        print(f"⚠️ EXCEDENTE: ${9.61 - 5.0:.2f} USD/mes")
        
        print("\n💡 RECOMENDACIONES:")
        print("1. Aplicar optimizaciones de Cloud Run")
        print("2. Configurar presupuesto con alertas")
        print("3. Monitorear uso diariamente")
        print("4. Considerar usar créditos gratuitos de GCP")

def main():
    optimizer = GCPCostOptimizer()
    
    print("🔧 OPTIMIZACIÓN DE COSTOS GCP - STEEL REBAR PREDICTOR")
    print("=" * 60)
    
    # 1. Mostrar uso actual
    optimizer.get_current_usage()
    
    # 2. Estimar costos
    optimizer.estimate_monthly_cost()
    
    # 3. Crear alerta de presupuesto
    print("\n" + "=" * 60)
    response = input("¿Crear alerta de presupuesto de $5 USD? (y/N): ")
    if response.lower() == 'y':
        optimizer.create_budget_alert(budget_amount=5.0)
    
    # 4. Aplicar optimizaciones
    print("\n" + "=" * 60)
    response = input("¿Aplicar optimizaciones de Cloud Run? (y/N): ")
    if response.lower() == 'y':
        optimizer.optimize_cloud_run_config()
    
    print("\n✅ Optimización completada")

if __name__ == "__main__":
    main()
