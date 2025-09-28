#!/usr/bin/env python3
"""
Script para configurar alertas de presupuesto en GCP Billing.
Genera comandos específicos y configuración para monitoreo de costos.
"""

import json
import os
from datetime import datetime

class BudgetAlertsConfigurator:
    """Configurador de alertas de presupuesto para GCP."""
    
    def __init__(self, project_id="steel-rebar-predictor-deacero", budget_amount=5.0):
        self.project_id = project_id
        self.budget_amount = budget_amount
        self.alert_thresholds = [0.5, 0.8, 0.95]  # 50%, 80%, 95%
    
    def generate_budget_configuration(self):
        """Generar configuración de presupuesto."""
        
        print("💰 CONFIGURANDO ALERTAS DE PRESUPUESTO GCP")
        print("=" * 70)
        print(f"Proyecto: {self.project_id}")
        print(f"Presupuesto: ${self.budget_amount} USD/mes")
        print(f"Alertas: {[f'{int(t*100)}%' for t in self.alert_thresholds]}")
        print("=" * 70)
        
        budget_config = {
            'basic_budget': {
                'title': 'Presupuesto Básico',
                'description': 'Presupuesto simple sin alertas',
                'command': f'gcloud billing budgets create --billing-account=BILLING_ACCOUNT_ID --budget-amount={self.budget_amount} --project={self.project_id}',
                'purpose': 'Crear presupuesto básico para el proyecto'
            },
            'budget_with_alerts': {
                'title': 'Presupuesto con Alertas',
                'description': 'Presupuesto con alertas en 50%, 80% y 95%',
                'command': f'gcloud billing budgets create --billing-account=BILLING_ACCOUNT_ID --budget-amount={self.budget_amount} --threshold-rule=percent=50 --threshold-rule=percent=80 --threshold-rule=percent=95 --project={self.project_id}',
                'purpose': 'Configuración recomendada con alertas completas'
            },
            'budget_with_notifications': {
                'title': 'Presupuesto con Notificaciones',
                'description': 'Presupuesto con alertas y notificaciones por email',
                'command': f'gcloud billing budgets create --billing-account=BILLING_ACCOUNT_ID --budget-amount={self.budget_amount} --threshold-rule=percent=50 --threshold-rule=percent=80 --threshold-rule=percent=95 --notification-rule=pubsub-topic=projects/{self.project_id}/topics/budget-alerts --project={self.project_id}',
                'purpose': 'Configuración avanzada con notificaciones automáticas'
            }
        }
        
        return budget_config
    
    def generate_alert_policies(self):
        """Generar políticas de alerta específicas."""
        
        print("\n🔔 GENERANDO POLÍTICAS DE ALERTA")
        print("=" * 70)
        
        alert_policies = {
            'cpu_alert': {
                'title': 'Alerta de CPU',
                'description': 'Alerta cuando CPU exceda 80%',
                'yaml_content': f'''displayName: "Cloud Run CPU High"
documentation:
  content: "CPU usage is above 80% for Steel Rebar Predictor"
  mimeType: "text/markdown"
conditions:
  - displayName: "CPU usage"
    conditionThreshold:
      filter: 'resource.type="cloud_run_revision" AND resource.labels.service_name="{self.project_id}"'
      comparison: COMPARISON_GREATER_THAN
      thresholdValue: 0.8
      duration: 300s
alertStrategy:
  autoClose: 604800s
notificationChannels: []
enabled: true''',
                'file_name': 'cpu_alert_policy.yaml'
            },
            'memory_alert': {
                'title': 'Alerta de Memoria',
                'description': 'Alerta cuando memoria exceda 80%',
                'yaml_content': f'''displayName: "Cloud Run Memory High"
documentation:
  content: "Memory usage is above 80% for Steel Rebar Predictor"
  mimeType: "text/markdown"
conditions:
  - displayName: "Memory usage"
    conditionThreshold:
      filter: 'resource.type="cloud_run_revision" AND resource.labels.service_name="{self.project_id}"'
      comparison: COMPARISON_GREATER_THAN
      thresholdValue: 0.8
      duration: 300s
alertStrategy:
  autoClose: 604800s
notificationChannels: []
enabled: true''',
                'file_name': 'memory_alert_policy.yaml'
            },
            'cost_alert': {
                'title': 'Alerta de Costo',
                'description': 'Alerta cuando costo diario exceda $0.50',
                'yaml_content': f'''displayName: "Daily Cost Alert"
documentation:
  content: "Daily cost exceeds $0.50 for Steel Rebar Predictor"
  mimeType: "text/markdown"
conditions:
  - displayName: "Daily cost"
    conditionThreshold:
      filter: 'resource.type="project" AND resource.labels.project_id="{self.project_id}"'
      comparison: COMPARISON_GREATER_THAN
      thresholdValue: 0.50
      duration: 86400s
alertStrategy:
  autoClose: 604800s
notificationChannels: []
enabled: true''',
                'file_name': 'cost_alert_policy.yaml'
            }
        }
        
        return alert_policies
    
    def generate_notification_setup(self):
        """Generar configuración de notificaciones."""
        
        print("\n📧 CONFIGURANDO NOTIFICACIONES")
        print("=" * 70)
        
        notification_config = {
            'email_notifications': {
                'title': 'Notificaciones por Email',
                'description': 'Configurar notificaciones por email',
                'commands': [
                    {
                        'description': 'Crear canal de notificación por email',
                        'command': f'gcloud alpha monitoring channels create --channel-content-from-file=email_channel.yaml --project={self.project_id}',
                        'explanation': 'Crea canal de notificación por email'
                    },
                    {
                        'description': 'Crear canal de notificación por SMS',
                        'command': f'gcloud alpha monitoring channels create --channel-content-from-file=sms_channel.yaml --project={self.project_id}',
                        'explanation': 'Crea canal de notificación por SMS'
                    }
                ]
            },
            'pubsub_notifications': {
                'title': 'Notificaciones por Pub/Sub',
                'description': 'Configurar notificaciones por Pub/Sub',
                'commands': [
                    {
                        'description': 'Crear topic de Pub/Sub',
                        'command': f'gcloud pubsub topics create budget-alerts --project={self.project_id}',
                        'explanation': 'Crea topic para alertas de presupuesto'
                    },
                    {
                        'description': 'Crear suscripción',
                        'command': f'gcloud pubsub subscriptions create budget-alerts-sub --topic=budget-alerts --project={self.project_id}',
                        'explanation': 'Crea suscripción para recibir alertas'
                    }
                ]
            }
        }
        
        return notification_config
    
    def create_setup_scripts(self):
        """Crear scripts de configuración."""
        
        print("\n📜 CREANDO SCRIPTS DE CONFIGURACIÓN")
        print("=" * 70)
        
        scripts = {
            'setup_budget': {
                'title': 'Script de Configuración de Presupuesto',
                'content': f'''#!/bin/bash
# Script para configurar presupuesto de ${self.budget_amount} USD/mes
# Proyecto: {self.project_id}

echo "💰 Configurando presupuesto de ${self.budget_amount} USD/mes..."

# Verificar que el usuario esté autenticado
gcloud auth list --filter=status:ACTIVE --format="value(account)" | head -1

# Crear presupuesto con alertas
gcloud billing budgets create \\
    --billing-account=BILLING_ACCOUNT_ID \\
    --budget-amount={self.budget_amount} \\
    --threshold-rule=percent=50 \\
    --threshold-rule=percent=80 \\
    --threshold-rule=percent=95 \\
    --project={self.project_id}

echo "✅ Presupuesto configurado exitosamente"
echo "📊 Alertas configuradas en 50%, 80% y 95%"
echo "📧 Revisar configuración de notificaciones en GCP Console"
''',
                'file_name': 'setup_budget.sh'
            },
            'setup_monitoring': {
                'title': 'Script de Configuración de Monitoreo',
                'content': f'''#!/bin/bash
# Script para configurar monitoreo del proyecto
# Proyecto: {self.project_id}

echo "📊 Configurando monitoreo..."

# Habilitar APIs necesarias
gcloud services enable monitoring.googleapis.com --project={self.project_id}
gcloud services enable logging.googleapis.com --project={self.project_id}

# Crear políticas de alerta
gcloud alpha monitoring policies create \\
    --policy-from-file=cpu_alert_policy.yaml \\
    --project={self.project_id}

gcloud alpha monitoring policies create \\
    --policy-from-file=memory_alert_policy.yaml \\
    --project={self.project_id}

gcloud alpha monitoring policies create \\
    --policy-from-file=cost_alert_policy.yaml \\
    --project={self.project_id}

echo "✅ Monitoreo configurado exitosamente"
echo "🔔 Políticas de alerta creadas"
echo "📊 Revisar configuración en Cloud Monitoring"
''',
                'file_name': 'setup_monitoring.sh'
            },
            'check_budget': {
                'title': 'Script de Verificación de Presupuesto',
                'content': f'''#!/bin/bash
# Script para verificar estado del presupuesto
# Proyecto: {self.project_id}

echo "💰 Verificando estado del presupuesto..."

# Listar presupuestos
echo "📋 Presupuestos configurados:"
gcloud billing budgets list --billing-account=BILLING_ACCOUNT_ID

# Verificar alertas activas
echo "🔔 Alertas activas:"
gcloud alpha monitoring policies list --project={self.project_id}

# Verificar costos actuales
echo "📊 Costos actuales:"
gcloud billing budgets list --billing-account=BILLING_ACCOUNT_ID --format="table(displayName,budgetFilter.projects,amount.specifiedAmount.units,thresholdRules.thresholdPercent)"

echo "✅ Verificación completada"
''',
                'file_name': 'check_budget.sh'
            }
        }
        
        return scripts
    
    def generate_setup_guide(self):
        """Generar guía de configuración paso a paso."""
        
        print("\n📖 CREANDO GUÍA DE CONFIGURACIÓN")
        print("=" * 70)
        
        guide = {
            'prerequisites': {
                'title': 'Prerrequisitos',
                'items': [
                    'Acceso de administrador al proyecto GCP',
                    'Permisos de Billing Account Administrator',
                    'gcloud CLI instalado y configurado',
                    'ID de Billing Account disponible'
                ]
            },
            'step_by_step': {
                'title': 'Configuración Paso a Paso',
                'steps': [
                    {
                        'step': 1,
                        'title': 'Obtener Billing Account ID',
                        'description': 'Identificar el ID de la cuenta de facturación',
                        'commands': [
                            'gcloud billing accounts list',
                            'gcloud billing projects describe PROJECT_ID'
                        ],
                        'verification': 'Copiar el Billing Account ID'
                    },
                    {
                        'step': 2,
                        'title': 'Crear Presupuesto',
                        'description': 'Configurar presupuesto de $5 USD/mes',
                        'commands': [
                            f'gcloud billing budgets create --billing-account=BILLING_ACCOUNT_ID --budget-amount={self.budget_amount} --threshold-rule=percent=50 --threshold-rule=percent=80 --threshold-rule=percent=95 --project={self.project_id}'
                        ],
                        'verification': 'Confirmar creación exitosa'
                    },
                    {
                        'step': 3,
                        'title': 'Configurar Notificaciones',
                        'description': 'Configurar canales de notificación',
                        'commands': [
                            'gcloud alpha monitoring channels create --channel-content-from-file=email_channel.yaml',
                            'gcloud pubsub topics create budget-alerts'
                        ],
                        'verification': 'Verificar canales creados'
                    },
                    {
                        'step': 4,
                        'title': 'Crear Políticas de Alerta',
                        'description': 'Configurar alertas de monitoreo',
                        'commands': [
                            'gcloud alpha monitoring policies create --policy-from-file=cpu_alert_policy.yaml',
                            'gcloud alpha monitoring policies create --policy-from-file=memory_alert_policy.yaml',
                            'gcloud alpha monitoring policies create --policy-from-file=cost_alert_policy.yaml'
                        ],
                        'verification': 'Confirmar políticas creadas'
                    },
                    {
                        'step': 5,
                        'title': 'Verificar Configuración',
                        'description': 'Confirmar que todo está configurado correctamente',
                        'commands': [
                            'gcloud billing budgets list --billing-account=BILLING_ACCOUNT_ID',
                            'gcloud alpha monitoring policies list'
                        ],
                        'verification': 'Revisar configuración en GCP Console'
                    }
                ]
            },
            'troubleshooting': {
                'title': 'Solución de Problemas',
                'common_issues': [
                    {
                        'issue': 'Error de permisos',
                        'solution': 'Verificar que el usuario tenga rol de Billing Account Administrator'
                    },
                    {
                        'issue': 'Billing Account no encontrado',
                        'solution': 'Verificar que el proyecto esté vinculado a una cuenta de facturación'
                    },
                    {
                        'issue': 'APIs no habilitadas',
                        'solution': 'Ejecutar: gcloud services enable monitoring.googleapis.com'
                    }
                ]
            }
        }
        
        return guide
    
    def save_budget_configuration(self, budget_config, alert_policies, notification_config, scripts, guide):
        """Guardar configuración completa de presupuesto."""
        
        configuration_package = {
            'timestamp': datetime.now().isoformat(),
            'project_id': self.project_id,
            'budget_amount': self.budget_amount,
            'alert_thresholds': self.alert_thresholds,
            'budget_configuration': budget_config,
            'alert_policies': alert_policies,
            'notification_configuration': notification_config,
            'setup_scripts': scripts,
            'setup_guide': guide,
            'estimated_setup_time': '15 minutos',
            'required_permissions': [
                'Billing Account Administrator',
                'Project Owner',
                'Monitoring Admin'
            ]
        }
        
        # Guardar configuración
        config_filename = f'budget_alerts_configuration_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'predictions', config_filename)
        
        with open(config_path, 'w') as f:
            json.dump(configuration_package, f, indent=2)
        
        # Guardar archivos YAML
        yaml_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'predictions')
        
        for policy_name, policy_data in alert_policies.items():
            yaml_file = os.path.join(yaml_dir, policy_data['file_name'])
            with open(yaml_file, 'w') as f:
                f.write(policy_data['yaml_content'])
        
        # Guardar scripts
        for script_name, script_data in scripts.items():
            script_file = os.path.join(yaml_dir, script_data['file_name'])
            with open(script_file, 'w') as f:
                f.write(script_data['content'])
            # Hacer ejecutable
            os.chmod(script_file, 0o755)
        
        print(f"\n💾 CONFIGURACIÓN DE PRESUPUESTO GUARDADA:")
        print(f"   📁 Archivo principal: {config_filename}")
        print(f"   📄 Archivos YAML: {len(alert_policies)} políticas")
        print(f"   📜 Scripts: {len(scripts)} scripts ejecutables")
        print(f"   ⏱️ Tiempo estimado: {configuration_package['estimated_setup_time']}")
        
        return config_filename
    
    def display_setup_summary(self):
        """Mostrar resumen de configuración."""
        
        print(f"\n🎯 RESUMEN DE CONFIGURACIÓN:")
        print("=" * 70)
        
        print(f"💰 CONFIGURACIÓN DE PRESUPUESTO:")
        print(f"   💵 Monto: ${self.budget_amount} USD/mes")
        print(f"   🔔 Alertas: 50%, 80%, 95%")
        print(f"   📧 Notificaciones: Email y Pub/Sub")
        print(f"   📊 Monitoreo: CPU, Memoria, Costo")
        
        print(f"\n📋 ARCHIVOS GENERADOS:")
        print(f"   📄 cpu_alert_policy.yaml - Alerta de CPU")
        print(f"   📄 memory_alert_policy.yaml - Alerta de memoria")
        print(f"   📄 cost_alert_policy.yaml - Alerta de costo")
        print(f"   📜 setup_budget.sh - Script de configuración")
        print(f"   📜 setup_monitoring.sh - Script de monitoreo")
        print(f"   📜 check_budget.sh - Script de verificación")
        
        print(f"\n🚀 PRÓXIMOS PASOS:")
        print(f"   1. Obtener Billing Account ID")
        print(f"   2. Ejecutar setup_budget.sh")
        print(f"   3. Configurar notificaciones por email")
        print(f"   4. Verificar configuración en GCP Console")

def main():
    """Función principal para configurar alertas de presupuesto."""
    
    print("💰 CONFIGURADOR DE ALERTAS DE PRESUPUESTO GCP")
    print("=" * 70)
    print("Configurando monitoreo de costos para Steel Rebar Predictor")
    print("=" * 70)
    
    configurator = BudgetAlertsConfigurator()
    
    # Generar configuración
    budget_config = configurator.generate_budget_configuration()
    alert_policies = configurator.generate_alert_policies()
    notification_config = configurator.generate_notification_setup()
    scripts = configurator.create_setup_scripts()
    guide = configurator.generate_setup_guide()
    
    # Guardar configuración
    config_filename = configurator.save_budget_configuration(budget_config, alert_policies, notification_config, scripts, guide)
    
    # Mostrar resumen
    configurator.display_setup_summary()
    
    print(f"\n✅ CONFIGURACIÓN DE PRESUPUESTO COMPLETADA")
    print(f"   📦 Archivo: {config_filename}")
    print(f"   📄 Políticas: {len(alert_policies)} alertas")
    print(f"   📜 Scripts: {len(scripts)} scripts")
    print(f"   📖 Guía: Configuración paso a paso")

if __name__ == "__main__":
    main()
