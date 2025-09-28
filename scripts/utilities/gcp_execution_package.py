#!/usr/bin/env python3
"""
Script para generar comandos específicos de GCP y guías de ejecución.
Facilita la implementación de optimizaciones en GCP Console.
"""

import json
import os
from datetime import datetime

class GCPCommandExecutor:
    """Ejecutor de comandos de GCP con guías detalladas."""
    
    def __init__(self, project_id="steel-rebar-predictor-deacero", region="us-central1"):
        self.project_id = project_id
        self.region = region
        self.service_name = "steel-rebar-predictor"
    
    def generate_cloud_run_commands(self):
        """Generar comandos específicos de Cloud Run."""
        
        print("🚀 GENERANDO COMANDOS DE CLOUD RUN PARA GCP")
        print("=" * 70)
        print(f"Proyecto: {self.project_id}")
        print(f"Región: {self.region}")
        print(f"Servicio: {self.service_name}")
        print("=" * 70)
        
        commands = {
            'preparation': {
                'title': 'Preparación del Entorno',
                'commands': [
                    {
                        'description': 'Autenticarse en GCP',
                        'command': 'gcloud auth login',
                        'explanation': 'Inicia sesión en tu cuenta de Google Cloud'
                    },
                    {
                        'description': 'Configurar proyecto',
                        'command': f'gcloud config set project {self.project_id}',
                        'explanation': 'Establece el proyecto activo'
                    },
                    {
                        'description': 'Verificar configuración',
                        'command': 'gcloud config list',
                        'explanation': 'Confirma que el proyecto está configurado correctamente'
                    }
                ]
            },
            'verification': {
                'title': 'Verificación del Estado Actual',
                'commands': [
                    {
                        'description': 'Verificar servicio actual',
                        'command': f'gcloud run services describe {self.service_name} --region={self.region} --project={self.project_id}',
                        'explanation': 'Muestra la configuración actual del servicio'
                    },
                    {
                        'description': 'Verificar recursos específicos',
                        'command': f'gcloud run services describe {self.service_name} --region={self.region} --project={self.project_id} --format="value(spec.template.spec.containers[0].resources.limits.cpu,spec.template.spec.containers[0].resources.limits.memory)"',
                        'explanation': 'Muestra solo CPU y memoria actuales'
                    }
                ]
            },
            'optimization': {
                'title': 'Aplicar Optimizaciones',
                'commands': [
                    {
                        'description': 'Optimización completa (recomendado)',
                        'command': f'gcloud run services update {self.service_name} --region={self.region} --cpu=0.5 --memory=512Mi --timeout=30s --max-instances=5 --concurrency=50 --project={self.project_id}',
                        'explanation': 'Aplica todas las optimizaciones de una vez',
                        'estimated_time': '2-3 minutos',
                        'risk': 'BAJO'
                    },
                    {
                        'description': 'Optimización paso a paso - CPU',
                        'command': f'gcloud run services update {self.service_name} --region={self.region} --cpu=0.5 --project={self.project_id}',
                        'explanation': 'Reduce CPU a 0.5 vCPU',
                        'estimated_time': '1 minuto',
                        'risk': 'MUY BAJO'
                    },
                    {
                        'description': 'Optimización paso a paso - Memoria',
                        'command': f'gcloud run services update {self.service_name} --region={self.region} --memory=512Mi --project={self.project_id}',
                        'explanation': 'Reduce memoria a 512Mi',
                        'estimated_time': '1 minuto',
                        'risk': 'MUY BAJO'
                    },
                    {
                        'description': 'Optimización paso a paso - Timeout',
                        'command': f'gcloud run services update {self.service_name} --region={self.region} --timeout=30s --project={self.project_id}',
                        'explanation': 'Configura timeout a 30 segundos',
                        'estimated_time': '30 segundos',
                        'risk': 'MUY BAJO'
                    },
                    {
                        'description': 'Optimización paso a paso - Instancias',
                        'command': f'gcloud run services update {self.service_name} --region={self.region} --max-instances=5 --project={self.project_id}',
                        'explanation': 'Limita instancias máximas a 5',
                        'estimated_time': '30 segundos',
                        'risk': 'BAJO'
                    },
                    {
                        'description': 'Optimización paso a paso - Concurrencia',
                        'command': f'gcloud run services update {self.service_name} --region={self.region} --concurrency=50 --project={self.project_id}',
                        'explanation': 'Configura concurrencia a 50 requests por instancia',
                        'estimated_time': '30 segundos',
                        'risk': 'BAJO'
                    }
                ]
            },
            'verification_after': {
                'title': 'Verificación Después de Optimizaciones',
                'commands': [
                    {
                        'description': 'Verificar nueva configuración',
                        'command': f'gcloud run services describe {self.service_name} --region={self.region} --project={self.project_id} --format="value(spec.template.spec.containers[0].resources.limits.cpu,spec.template.spec.containers[0].resources.limits.memory)"',
                        'explanation': 'Confirma que las optimizaciones se aplicaron'
                    },
                    {
                        'description': 'Probar servicio',
                        'command': f'curl https://{self.service_name}-{self.project_id}.{self.region}.run.app/health',
                        'explanation': 'Verifica que el servicio funciona correctamente'
                    },
                    {
                        'description': 'Probar endpoint de información',
                        'command': f'curl https://{self.service_name}-{self.project_id}.{self.region}.run.app/',
                        'explanation': 'Verifica el endpoint principal'
                    }
                ]
            }
        }
        
        return commands
    
    def generate_budget_alerts_commands(self):
        """Generar comandos para configurar alertas de presupuesto."""
        
        print("\n💰 GENERANDO COMANDOS DE ALERTAS DE PRESUPUESTO")
        print("=" * 70)
        
        budget_commands = {
            'budget_creation': {
                'title': 'Crear Presupuesto de $5 USD/mes',
                'commands': [
                    {
                        'description': 'Crear presupuesto básico',
                        'command': f'gcloud billing budgets create --billing-account=BILLING_ACCOUNT_ID --budget-amount=5.0 --project={self.project_id}',
                        'explanation': 'Crea un presupuesto de $5 USD para el proyecto',
                        'note': 'Reemplazar BILLING_ACCOUNT_ID con tu ID de facturación'
                    },
                    {
                        'description': 'Crear presupuesto con alertas',
                        'command': f'gcloud billing budgets create --billing-account=BILLING_ACCOUNT_ID --budget-amount=5.0 --threshold-rule=percent=50 --threshold-rule=percent=80 --threshold-rule=percent=95 --project={self.project_id}',
                        'explanation': 'Crea presupuesto con alertas en 50%, 80% y 95%',
                        'note': 'Configuración recomendada para monitoreo completo'
                    }
                ]
            },
            'budget_management': {
                'title': 'Gestión de Presupuestos',
                'commands': [
                    {
                        'description': 'Listar presupuestos',
                        'command': 'gcloud billing budgets list --billing-account=BILLING_ACCOUNT_ID',
                        'explanation': 'Muestra todos los presupuestos configurados'
                    },
                    {
                        'description': 'Ver detalles de presupuesto',
                        'command': 'gcloud billing budgets describe BUDGET_ID --billing-account=BILLING_ACCOUNT_ID',
                        'explanation': 'Muestra detalles de un presupuesto específico',
                        'note': 'Reemplazar BUDGET_ID con el ID del presupuesto'
                    },
                    {
                        'description': 'Actualizar presupuesto',
                        'command': 'gcloud billing budgets update BUDGET_ID --billing-account=BILLING_ACCOUNT_ID --budget-amount=10.0',
                        'explanation': 'Actualiza el monto del presupuesto',
                        'note': 'Ejemplo: aumentar a $10 USD'
                    }
                ]
            }
        }
        
        return budget_commands
    
    def generate_monitoring_commands(self):
        """Generar comandos para configurar monitoreo."""
        
        print("\n📊 GENERANDO COMANDOS DE MONITOREO")
        print("=" * 70)
        
        monitoring_commands = {
            'cloud_monitoring': {
                'title': 'Configurar Cloud Monitoring',
                'commands': [
                    {
                        'description': 'Habilitar Cloud Monitoring API',
                        'command': 'gcloud services enable monitoring.googleapis.com',
                        'explanation': 'Habilita la API de Cloud Monitoring'
                    },
                    {
                        'description': 'Crear política de alerta para CPU',
                        'command': f'gcloud alpha monitoring policies create --policy-from-file=cpu_alert_policy.yaml --project={self.project_id}',
                        'explanation': 'Crea alerta cuando CPU exceda 80%',
                        'note': 'Requiere archivo cpu_alert_policy.yaml'
                    },
                    {
                        'description': 'Crear política de alerta para memoria',
                        'command': f'gcloud alpha monitoring policies create --policy-from-file=memory_alert_policy.yaml --project={self.project_id}',
                        'explanation': 'Crea alerta cuando memoria exceda 80%',
                        'note': 'Requiere archivo memory_alert_policy.yaml'
                    }
                ]
            },
            'logging': {
                'title': 'Configurar Logging',
                'commands': [
                    {
                        'description': 'Ver logs del servicio',
                        'command': f'gcloud run services logs read {self.service_name} --region={self.region} --project={self.project_id}',
                        'explanation': 'Muestra logs recientes del servicio'
                    },
                    {
                        'description': 'Ver logs en tiempo real',
                        'command': f'gcloud run services logs tail {self.service_name} --region={self.region} --project={self.project_id}',
                        'explanation': 'Muestra logs en tiempo real (streaming)'
                    },
                    {
                        'description': 'Filtrar logs por nivel',
                        'command': f'gcloud run services logs read {self.service_name} --region={self.region} --project={self.project_id} --filter="severity>=ERROR"',
                        'explanation': 'Muestra solo logs de error'
                    }
                ]
            }
        }
        
        return monitoring_commands
    
    def create_execution_guide(self):
        """Crear guía de ejecución paso a paso."""
        
        print("\n📋 CREANDO GUÍA DE EJECUCIÓN PASO A PASO")
        print("=" * 70)
        
        guide = {
            'phase_1': {
                'title': 'Fase 1: Preparación (5 minutos)',
                'steps': [
                    {
                        'step': 1,
                        'title': 'Verificar acceso a GCP',
                        'description': 'Asegúrate de tener acceso al proyecto y permisos de administrador',
                        'commands': ['gcloud auth login', f'gcloud config set project {self.project_id}'],
                        'verification': 'gcloud config list'
                    },
                    {
                        'step': 2,
                        'title': 'Verificar estado actual',
                        'description': 'Revisar la configuración actual del servicio',
                        'commands': [f'gcloud run services describe {self.service_name} --region={self.region} --project={self.project_id}'],
                        'verification': 'Confirmar CPU=1.0 y Memory=1Gi'
                    }
                ]
            },
            'phase_2': {
                'title': 'Fase 2: Optimización (10 minutos)',
                'steps': [
                    {
                        'step': 3,
                        'title': 'Aplicar optimizaciones',
                        'description': 'Ejecutar comando de optimización completa',
                        'commands': [f'gcloud run services update {self.service_name} --region={self.region} --cpu=0.5 --memory=512Mi --timeout=30s --max-instances=5 --concurrency=50 --project={self.project_id}'],
                        'verification': 'Esperar confirmación de actualización exitosa'
                    },
                    {
                        'step': 4,
                        'title': 'Verificar cambios',
                        'description': 'Confirmar que las optimizaciones se aplicaron',
                        'commands': [f'gcloud run services describe {self.service_name} --region={self.region} --project={self.project_id} --format="value(spec.template.spec.containers[0].resources.limits.cpu,spec.template.spec.containers[0].resources.limits.memory)"'],
                        'verification': 'Confirmar CPU=0.5 y Memory=512Mi'
                    }
                ]
            },
            'phase_3': {
                'title': 'Fase 3: Validación (5 minutos)',
                'steps': [
                    {
                        'step': 5,
                        'title': 'Probar servicio',
                        'description': 'Verificar que el servicio funciona correctamente',
                        'commands': [f'curl https://{self.service_name}-{self.project_id}.{self.region}.run.app/health'],
                        'verification': 'Respuesta HTTP 200 OK'
                    },
                    {
                        'step': 6,
                        'title': 'Probar predicción',
                        'description': 'Verificar endpoint de predicción',
                        'commands': [f'curl -H "X-API-Key: deacero_steel_predictor_2025_key" https://{self.service_name}-{self.project_id}.{self.region}.run.app/predict/steel-rebar-price'],
                        'verification': 'Respuesta con predicción válida'
                    }
                ]
            },
            'phase_4': {
                'title': 'Fase 4: Monitoreo (5 minutos)',
                'steps': [
                    {
                        'step': 7,
                        'title': 'Configurar alertas de presupuesto',
                        'description': 'Crear alertas para monitorear costos',
                        'commands': ['gcloud billing budgets create --billing-account=BILLING_ACCOUNT_ID --budget-amount=5.0 --threshold-rule=percent=50 --threshold-rule=percent=80 --threshold-rule=percent=95 --project=steel-rebar-predictor-deacero'],
                        'verification': 'Confirmar creación exitosa del presupuesto'
                    },
                    {
                        'step': 8,
                        'title': 'Configurar monitoreo',
                        'description': 'Habilitar monitoreo automático',
                        'commands': ['gcloud services enable monitoring.googleapis.com'],
                        'verification': 'API habilitada exitosamente'
                    }
                ]
            }
        }
        
        return guide
    
    def save_execution_package(self, cloud_run_commands, budget_commands, monitoring_commands, guide):
        """Guardar paquete completo de ejecución."""
        
        execution_package = {
            'timestamp': datetime.now().isoformat(),
            'project_id': self.project_id,
            'region': self.region,
            'service_name': self.service_name,
            'cloud_run_commands': cloud_run_commands,
            'budget_commands': budget_commands,
            'monitoring_commands': monitoring_commands,
            'execution_guide': guide,
            'estimated_total_time': '25 minutos',
            'risk_level': 'BAJO',
            'rollback_commands': [
                f'gcloud run services update {self.service_name} --region={self.region} --cpu=1.0 --memory=1Gi --project={self.project_id}',
                f'gcloud run services update {self.service_name} --region={self.region} --timeout=300s --project={self.project_id}',
                f'gcloud run services update {self.service_name} --region={self.region} --max-instances=10 --project={self.project_id}'
            ]
        }
        
        # Guardar paquete
        package_filename = f'gcp_execution_package_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        package_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'predictions', package_filename)
        
        with open(package_path, 'w') as f:
            json.dump(execution_package, f, indent=2)
        
        print(f"\n💾 PAQUETE DE EJECUCIÓN GUARDADO:")
        print(f"   📁 Archivo: {package_filename}")
        print(f"   📍 Ubicación: {package_path}")
        print(f"   ⏱️ Tiempo estimado: {execution_package['estimated_total_time']}")
        print(f"   ⚠️ Nivel de riesgo: {execution_package['risk_level']}")
        
        return package_filename
    
    def display_execution_summary(self):
        """Mostrar resumen de ejecución."""
        
        print(f"\n🎯 RESUMEN DE EJECUCIÓN:")
        print("=" * 70)
        
        print(f"📋 FASES DE EJECUCIÓN:")
        print(f"   1. 🔧 Preparación (5 min) - Verificar acceso y estado actual")
        print(f"   2. ⚡ Optimización (10 min) - Aplicar optimizaciones de Cloud Run")
        print(f"   3. ✅ Validación (5 min) - Probar funcionamiento del servicio")
        print(f"   4. 📊 Monitoreo (5 min) - Configurar alertas y monitoreo")
        
        print(f"\n💰 BENEFICIOS ESPERADOS:")
        print(f"   💵 Reducción de costos: $9.54/mes (50% ahorro)")
        print(f"   ⚡ Mejora de rendimiento: Tiempos de respuesta optimizados")
        print(f"   📊 Monitoreo automático: Alertas proactivas de costos")
        print(f"   🔒 Mayor control: Límites de escalado y concurrencia")
        
        print(f"\n🚨 PLAN DE ROLLBACK:")
        print(f"   🔄 Comandos de reversión incluidos en el paquete")
        print(f"   ⏱️ Tiempo de rollback: < 5 minutos")
        print(f"   📞 Soporte: Documentación completa incluida")

def main():
    """Función principal para generar paquete de ejecución."""
    
    print("🚀 GENERADOR DE PAQUETE DE EJECUCIÓN GCP")
    print("=" * 70)
    print("Creando comandos y guías para optimizar Cloud Run")
    print("=" * 70)
    
    executor = GCPCommandExecutor()
    
    # Generar comandos
    cloud_run_commands = executor.generate_cloud_run_commands()
    budget_commands = executor.generate_budget_alerts_commands()
    monitoring_commands = executor.generate_monitoring_commands()
    guide = executor.create_execution_guide()
    
    # Guardar paquete
    package_filename = executor.save_execution_package(cloud_run_commands, budget_commands, monitoring_commands, guide)
    
    # Mostrar resumen
    executor.display_execution_summary()
    
    print(f"\n✅ PAQUETE DE EJECUCIÓN GENERADO EXITOSAMENTE")
    print(f"   📦 Archivo: {package_filename}")
    print(f"   📋 Comandos: Cloud Run, Presupuesto, Monitoreo")
    print(f"   📖 Guía: Ejecución paso a paso")
    print(f"   🔄 Rollback: Plan de reversión incluido")
    
    print(f"\n🎯 PRÓXIMOS PASOS:")
    print(f"   1. Abrir GCP Console o usar gcloud CLI")
    print(f"   2. Seguir la guía de ejecución paso a paso")
    print(f"   3. Ejecutar comandos en el orden especificado")
    print(f"   4. Verificar cada paso antes de continuar")

if __name__ == "__main__":
    main()
