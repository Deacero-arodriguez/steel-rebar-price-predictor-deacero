#!/usr/bin/env python3
"""
Script para deployar la API en GCP y ejecutar tests automáticamente
"""

import subprocess
import sys
import os
import json
import time
from datetime import datetime
from typing import Dict, Any

class GCPDeploymentTester:
    """Clase para manejar deployment y testing en GCP."""
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.service_name = "steel-rebar-predictor"
        self.region = "us-central1"
        
    def run_command(self, command: str, description: str) -> tuple[bool, str]:
        """Ejecutar comando y retornar resultado."""
        
        print(f"🔧 {description}...")
        print(f"   Comando: {command}")
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutos timeout
            )
            
            if result.returncode == 0:
                print(f"   ✅ {description} completado")
                return True, result.stdout
            else:
                print(f"   ❌ {description} falló")
                print(f"   Error: {result.stderr}")
                return False, result.stderr
                
        except subprocess.TimeoutExpired:
            print(f"   ⏰ {description} timeout (5 minutos)")
            return False, "Command timeout"
        except Exception as e:
            print(f"   💥 Error in {description}: {e}")
            return False, str(e)
    
    def check_gcp_setup(self) -> bool:
        """Verificar configuración de GCP."""
        
        print("🔍 Verificando configuración de GCP...")
        
        # Verificar que gcloud esté instalado
        success, output = self.run_command("gcloud --version", "Verificando gcloud CLI")
        if not success:
            print("❌ gcloud CLI no está instalado o no está en PATH")
            return False
        
        # Verificar autenticación
        success, output = self.run_command("gcloud auth list --filter=status:ACTIVE --format='value(account)'", "Verificando autenticación")
        if not success or not output.strip():
            print("❌ No hay cuentas autenticadas en gcloud")
            print("   Ejecuta: gcloud auth login")
            return False
        
        print(f"   ✅ Autenticado como: {output.strip()}")
        
        # Verificar proyecto
        success, output = self.run_command(f"gcloud config get-value project", "Verificando proyecto")
        if not success or output.strip() != self.project_id:
            print(f"❌ Proyecto configurado incorrectamente")
            print(f"   Actual: {output.strip()}")
            print(f"   Esperado: {self.project_id}")
            print(f"   Ejecuta: gcloud config set project {self.project_id}")
            return False
        
        print(f"   ✅ Proyecto configurado: {self.project_id}")
        
        # Habilitar APIs necesarias
        apis = [
            "cloudbuild.googleapis.com",
            "run.googleapis.com",
            "containerregistry.googleapis.com"
        ]
        
        for api in apis:
            success, output = self.run_command(
                f"gcloud services enable {api}",
                f"Habilitando API {api}"
            )
            if not success:
                print(f"⚠️  No se pudo habilitar {api}")
        
        return True
    
    def build_and_deploy(self) -> bool:
        """Construir y desplegar la aplicación en Cloud Run."""
        
        print("🚀 Iniciando build y deployment...")
        
        # Navegar al directorio del proyecto
        project_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        os.chdir(project_dir)
        
        # Ejecutar Cloud Build
        build_command = f"gcloud builds submit --config deployment/cloud/cloudbuild.yaml --project {self.project_id}"
        success, output = self.run_command(build_command, "Ejecutando Cloud Build")
        
        if not success:
            return False
        
        # Obtener URL del servicio desplegado
        get_url_command = f"gcloud run services describe {self.service_name} --region {self.region} --format='value(status.url)' --project {self.project_id}"
        success, output = self.run_command(get_url_command, "Obteniendo URL del servicio")
        
        if not success:
            return False
        
        self.service_url = output.strip()
        print(f"   ✅ Servicio desplegado en: {self.service_url}")
        
        return True
    
    def wait_for_service_ready(self, max_wait_minutes: int = 5) -> bool:
        """Esperar a que el servicio esté listo."""
        
        print(f"⏳ Esperando que el servicio esté listo (máximo {max_wait_minutes} minutos)...")
        
        start_time = time.time()
        max_wait_seconds = max_wait_minutes * 60
        
        while time.time() - start_time < max_wait_seconds:
            # Probar endpoint de health
            test_command = f"curl -s -o /dev/null -w '%{{http_code}}' {self.service_url}/health"
            success, output = self.run_command(test_command, "Probando endpoint health")
            
            if success and output.strip() == "200":
                print("   ✅ Servicio está listo y respondiendo")
                return True
            
            print(f"   ⏳ Esperando... ({int(time.time() - start_time)}s)")
            time.sleep(10)
        
        print("   ⏰ Timeout esperando que el servicio esté listo")
        return False
    
    def run_api_tests(self) -> bool:
        """Ejecutar tests de la API."""
        
        print("🧪 Ejecutando tests de la API...")
        
        # Ejecutar script de test
        test_script = os.path.join(os.path.dirname(__file__), "test_api_gcp.py")
        test_command = f"python {test_script} {self.service_url}"
        
        success, output = self.run_command(test_command, "Ejecutando tests de API")
        
        if success:
            print("   ✅ Tests completados exitosamente")
            print("   📊 Resultados del test:")
            print(output)
            return True
        else:
            print("   ❌ Tests fallaron")
            print("   📊 Output del test:")
            print(output)
            return False
    
    def generate_deployment_report(self, deployment_success: bool, test_success: bool) -> str:
        """Generar reporte de deployment y testing."""
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = {
            "deployment_report": {
                "timestamp": timestamp,
                "project_id": self.project_id,
                "service_name": self.service_name,
                "region": self.region,
                "service_url": getattr(self, 'service_url', 'N/A'),
                "deployment_success": deployment_success,
                "test_success": test_success,
                "overall_status": "SUCCESS" if (deployment_success and test_success) else "FAILED"
            }
        }
        
        # Guardar reporte
        report_file = f"deployment_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path = os.path.join("data", "predictions", report_file)
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n📋 REPORTE DE DEPLOYMENT")
        print("="*50)
        print(f"   Timestamp: {timestamp}")
        print(f"   Proyecto: {self.project_id}")
        print(f"   Servicio: {self.service_name}")
        print(f"   Región: {self.region}")
        print(f"   URL: {getattr(self, 'service_url', 'N/A')}")
        print(f"   Deployment: {'✅' if deployment_success else '❌'}")
        print(f"   Tests: {'✅' if test_success else '❌'}")
        print(f"   Estado General: {'✅ SUCCESS' if (deployment_success and test_success) else '❌ FAILED'}")
        print(f"   Reporte guardado en: {report_path}")
        
        return report_path

def main():
    """Función principal."""
    
    if len(sys.argv) < 2:
        print("❌ Error: Debes proporcionar el Project ID de GCP")
        print("   Uso: python deploy_and_test_gcp.py <PROJECT_ID>")
        print("   Ejemplo: python deploy_and_test_gcp.py mi-proyecto-gcp")
        sys.exit(1)
    
    project_id = sys.argv[1]
    
    print("🚀 DEPLOYMENT Y TESTING DE API EN GCP")
    print("="*50)
    print(f"   Proyecto: {project_id}")
    print(f"   Servicio: steel-rebar-predictor")
    print(f"   Región: us-central1")
    print("-" * 50)
    
    # Crear instancia del deployment tester
    tester = GCPDeploymentTester(project_id)
    
    try:
        # 1. Verificar configuración de GCP
        if not tester.check_gcp_setup():
            print("\n❌ Configuración de GCP incorrecta")
            sys.exit(1)
        
        # 2. Build y deployment
        deployment_success = tester.build_and_deploy()
        
        if not deployment_success:
            print("\n❌ Deployment falló")
            sys.exit(1)
        
        # 3. Esperar que el servicio esté listo
        if not tester.wait_for_service_ready():
            print("\n⚠️  Servicio desplegado pero no responde correctamente")
        
        # 4. Ejecutar tests
        test_success = tester.run_api_tests()
        
        # 5. Generar reporte
        tester.generate_deployment_report(deployment_success, test_success)
        
        # Determinar código de salida
        if deployment_success and test_success:
            print("\n🎉 DEPLOYMENT Y TESTING COMPLETADOS EXITOSAMENTE")
            sys.exit(0)
        else:
            print("\n⚠️  DEPLOYMENT COMPLETADO CON PROBLEMAS")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️  Proceso interrumpido por el usuario")
        sys.exit(3)
    except Exception as e:
        print(f"\n💥 Error inesperado: {e}")
        sys.exit(4)

if __name__ == "__main__":
    main()
