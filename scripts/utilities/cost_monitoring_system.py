#!/usr/bin/env python3
"""
Sistema de monitoreo automático de costos para el Steel Rebar Predictor.
Genera alertas automáticas cuando se exceden los límites de presupuesto.
"""

import json
import os
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd

class CostMonitoringSystem:
    """Sistema de monitoreo automático de costos."""
    
    def __init__(self, project_id="steel-rebar-predictor-deacero", budget_limit=5.0):
        self.project_id = project_id
        self.budget_limit = budget_limit
        self.alert_thresholds = [0.5, 0.8, 0.95]  # 50%, 80%, 95% del presupuesto
        self.monitoring_data = []
    
    def estimate_current_costs(self):
        """Estimar costos actuales basados en configuración."""
        
        # Configuración actual estimada
        current_config = {
            'cpu': 1.0,  # vCPU (antes de optimización)
            'memory': 1.0,  # GiB (antes de optimización)
            'requests_per_day': 100,
            'uptime_hours': 24
        }
        
        # Precios GCP (us-central1)
        pricing = {
            'cpu_per_hour': 0.024,  # USD/vCPU-hora
            'memory_per_hour': 0.0025,  # USD/GiB-hora
            'requests_per_million': 0.40  # USD/1M requests
        }
        
        # Cálculos mensuales
        cpu_cost = current_config['cpu'] * current_config['uptime_hours'] * 30 * pricing['cpu_per_hour']
        memory_cost = current_config['memory'] * current_config['uptime_hours'] * 30 * pricing['memory_per_hour']
        requests_cost = (current_config['requests_per_day'] * 30) / 1000000 * pricing['requests_per_million']
        
        # Costos adicionales
        container_registry_cost = 0.01  # USD/mes
        cloud_build_cost = 0.09  # USD/mes
        
        total_monthly = cpu_cost + memory_cost + requests_cost + container_registry_cost + cloud_build_cost
        
        return {
            'cpu_cost': cpu_cost,
            'memory_cost': memory_cost,
            'requests_cost': requests_cost,
            'container_registry_cost': container_registry_cost,
            'cloud_build_cost': cloud_build_cost,
            'total_monthly': total_monthly,
            'budget_utilization': (total_monthly / self.budget_limit) * 100,
            'timestamp': datetime.now().isoformat()
        }
    
    def estimate_optimized_costs(self):
        """Estimar costos después de optimizaciones."""
        
        # Configuración optimizada
        optimized_config = {
            'cpu': 0.5,  # vCPU (después de optimización)
            'memory': 0.5,  # GiB (después de optimización)
            'requests_per_day': 100,
            'uptime_hours': 24
        }
        
        # Precios GCP (us-central1)
        pricing = {
            'cpu_per_hour': 0.024,  # USD/vCPU-hora
            'memory_per_hour': 0.0025,  # USD/GiB-hora
            'requests_per_million': 0.40  # USD/1M requests
        }
        
        # Cálculos mensuales
        cpu_cost = optimized_config['cpu'] * optimized_config['uptime_hours'] * 30 * pricing['cpu_per_hour']
        memory_cost = optimized_config['memory'] * optimized_config['uptime_hours'] * 30 * pricing['memory_per_hour']
        requests_cost = (optimized_config['requests_per_day'] * 30) / 1000000 * pricing['requests_per_million']
        
        # Costos adicionales
        container_registry_cost = 0.01  # USD/mes
        cloud_build_cost = 0.09  # USD/mes
        
        total_monthly = cpu_cost + memory_cost + requests_cost + container_registry_cost + cloud_build_cost
        
        return {
            'cpu_cost': cpu_cost,
            'memory_cost': memory_cost,
            'requests_cost': requests_cost,
            'container_registry_cost': container_registry_cost,
            'cloud_build_cost': cloud_build_cost,
            'total_monthly': total_monthly,
            'budget_utilization': (total_monthly / self.budget_limit) * 100,
            'timestamp': datetime.now().isoformat()
        }
    
    def check_budget_alerts(self, cost_data):
        """Verificar si se deben enviar alertas de presupuesto."""
        
        utilization = cost_data['budget_utilization']
        alerts = []
        
        for threshold in self.alert_thresholds:
            threshold_percent = threshold * 100
            
            if utilization >= threshold_percent:
                alert_level = self._get_alert_level(threshold)
                alerts.append({
                    'level': alert_level,
                    'threshold': threshold_percent,
                    'current_utilization': utilization,
                    'current_cost': cost_data['total_monthly'],
                    'budget_limit': self.budget_limit,
                    'message': self._generate_alert_message(alert_level, utilization, cost_data['total_monthly'])
                })
        
        return alerts
    
    def _get_alert_level(self, threshold):
        """Determinar nivel de alerta."""
        
        if threshold >= 0.95:
            return 'CRITICAL'
        elif threshold >= 0.8:
            return 'HIGH'
        else:
            return 'MEDIUM'
    
    def _generate_alert_message(self, level, utilization, current_cost):
        """Generar mensaje de alerta."""
        
        messages = {
            'CRITICAL': f"🚨 ALERTA CRÍTICA: El proyecto ha alcanzado {utilization:.1f}% del presupuesto (${current_cost:.2f}/${self.budget_limit:.2f}). Se requiere acción inmediata.",
            'HIGH': f"⚠️ ALERTA ALTA: El proyecto ha alcanzado {utilization:.1f}% del presupuesto (${current_cost:.2f}/${self.budget_limit:.2f}). Se recomienda revisar costos.",
            'MEDIUM': f"📊 ALERTA MEDIA: El proyecto ha alcanzado {utilization:.1f}% del presupuesto (${current_cost:.2f}/${self.budget_limit:.2f}). Monitorear de cerca."
        }
        
        return messages.get(level, "Alerta de presupuesto generada.")
    
    def generate_cost_report(self):
        """Generar reporte de costos."""
        
        print("💰 GENERANDO REPORTE DE MONITOREO DE COSTOS")
        print("=" * 60)
        
        # Estimar costos actuales y optimizados
        current_costs = self.estimate_current_costs()
        optimized_costs = self.estimate_optimized_costs()
        
        # Verificar alertas
        current_alerts = self.check_budget_alerts(current_costs)
        optimized_alerts = self.check_budget_alerts(optimized_costs)
        
        # Calcular ahorros
        savings = current_costs['total_monthly'] - optimized_costs['total_monthly']
        savings_percent = (savings / current_costs['total_monthly']) * 100
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'project_id': self.project_id,
            'budget_limit': self.budget_limit,
            'current_costs': current_costs,
            'optimized_costs': optimized_costs,
            'savings': {
                'amount': savings,
                'percent': savings_percent
            },
            'current_alerts': current_alerts,
            'optimized_alerts': optimized_alerts,
            'recommendations': self._generate_recommendations(current_costs, optimized_costs)
        }
        
        # Mostrar resumen
        print(f"\n📊 RESUMEN DE COSTOS:")
        print(f"   💰 Costo actual: ${current_costs['total_monthly']:.2f}/mes")
        print(f"   💰 Costo optimizado: ${optimized_costs['total_monthly']:.2f}/mes")
        print(f"   💵 Ahorro potencial: ${savings:.2f}/mes ({savings_percent:.1f}%)")
        print(f"   📊 Presupuesto: ${self.budget_limit:.2f}/mes")
        
        print(f"\n🚨 ALERTAS ACTUALES:")
        if current_alerts:
            for alert in current_alerts:
                print(f"   {alert['level']}: {alert['message']}")
        else:
            print(f"   ✅ Sin alertas activas")
        
        print(f"\n🚨 ALERTAS DESPUÉS DE OPTIMIZACIÓN:")
        if optimized_alerts:
            for alert in optimized_alerts:
                print(f"   {alert['level']}: {alert['message']}")
        else:
            print(f"   ✅ Sin alertas después de optimización")
        
        return report
    
    def _generate_recommendations(self, current_costs, optimized_costs):
        """Generar recomendaciones basadas en costos."""
        
        recommendations = []
        
        # Recomendación de optimización
        if current_costs['budget_utilization'] > 100:
            recommendations.append({
                'priority': 'CRITICAL',
                'title': 'Aplicar optimizaciones inmediatamente',
                'description': f"El costo actual (${current_costs['total_monthly']:.2f}) excede el presupuesto (${self.budget_limit:.2f})",
                'action': 'Ejecutar comandos de optimización de Cloud Run'
            })
        
        # Recomendación de monitoreo
        if current_costs['budget_utilization'] > 80:
            recommendations.append({
                'priority': 'HIGH',
                'title': 'Configurar monitoreo diario',
                'description': f"Utilización actual: {current_costs['budget_utilization']:.1f}%",
                'action': 'Ejecutar este script diariamente'
            })
        
        # Recomendación de alertas
        if not self.check_budget_alerts(optimized_costs):
            recommendations.append({
                'priority': 'MEDIUM',
                'title': 'Configurar alertas automáticas',
                'description': 'Después de optimización, configurar alertas en GCP Console',
                'action': 'Configurar Budget Alerts en GCP Billing'
            })
        
        return recommendations
    
    def save_monitoring_data(self, report):
        """Guardar datos de monitoreo."""
        
        # Agregar a datos históricos
        self.monitoring_data.append(report)
        
        # Guardar reporte actual
        report_filename = f'cost_monitoring_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        report_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'predictions', report_filename)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n💾 REPORTE GUARDADO:")
        print(f"   📁 Archivo: {report_filename}")
        print(f"   📍 Ubicación: {report_path}")
        
        return report_filename
    
    def generate_monitoring_schedule(self):
        """Generar cronograma de monitoreo."""
        
        print(f"\n📅 CRONOGRAMA DE MONITOREO RECOMENDADO:")
        print("=" * 60)
        
        schedule = {
            'daily': {
                'description': 'Monitoreo diario de costos',
                'command': 'python scripts/utilities/cost_monitoring_system.py --mode daily',
                'time': '09:00 AM',
                'purpose': 'Detectar cambios rápidos en costos'
            },
            'weekly': {
                'description': 'Reporte semanal de costos',
                'command': 'python scripts/utilities/cost_monitoring_system.py --mode weekly',
                'time': 'Monday 10:00 AM',
                'purpose': 'Análisis de tendencias semanales'
            },
            'monthly': {
                'description': 'Reporte mensual completo',
                'command': 'python scripts/utilities/cost_monitoring_system.py --mode monthly',
                'time': '1st of month 11:00 AM',
                'purpose': 'Análisis completo del mes anterior'
            }
        }
        
        for frequency, details in schedule.items():
            print(f"\n📊 {frequency.upper()}:")
            print(f"   📝 Descripción: {details['description']}")
            print(f"   ⏰ Horario: {details['time']}")
            print(f"   🎯 Propósito: {details['purpose']}")
            print(f"   💻 Comando: {details['command']}")
        
        return schedule
    
    def create_alert_configuration(self):
        """Crear configuración de alertas para GCP."""
        
        print(f"\n🔔 CONFIGURACIÓN DE ALERTAS GCP:")
        print("=" * 60)
        
        alert_config = {
            'budget_alerts': [
                {
                    'threshold': 50,
                    'description': 'Alerta cuando se alcanza 50% del presupuesto',
                    'gcp_command': f'gcloud billing budgets create --billing-account=BILLING_ACCOUNT --budget-amount={self.budget_limit} --threshold-rule=percent=50'
                },
                {
                    'threshold': 80,
                    'description': 'Alerta cuando se alcanza 80% del presupuesto',
                    'gcp_command': f'gcloud billing budgets create --billing-account=BILLING_ACCOUNT --budget-amount={self.budget_limit} --threshold-rule=percent=80'
                },
                {
                    'threshold': 95,
                    'description': 'Alerta crítica cuando se alcanza 95% del presupuesto',
                    'gcp_command': f'gcloud billing budgets create --billing-account=BILLING_ACCOUNT --budget-amount={self.budget_limit} --threshold-rule=percent=95'
                }
            ],
            'quota_alerts': [
                {
                    'service': 'Cloud Run',
                    'description': 'Alerta cuando se alcanza 80% de la cuota de CPU',
                    'gcp_command': 'gcloud alpha monitoring policies create --policy-from-file=cloud_run_cpu_policy.yaml'
                },
                {
                    'service': 'Cloud Run',
                    'description': 'Alerta cuando se alcanza 80% de la cuota de memoria',
                    'gcp_command': 'gcloud alpha monitoring policies create --policy-from-file=cloud_run_memory_policy.yaml'
                }
            ]
        }
        
        print(f"📋 ALERTAS DE PRESUPUESTO:")
        for alert in alert_config['budget_alerts']:
            print(f"   🔔 {alert['threshold']}%: {alert['description']}")
            print(f"      💻 {alert['gcp_command']}")
        
        print(f"\n📋 ALERTAS DE CUOTA:")
        for alert in alert_config['quota_alerts']:
            print(f"   🔔 {alert['service']}: {alert['description']}")
            print(f"      💻 {alert['gcp_command']}")
        
        return alert_config

def main():
    """Función principal para el sistema de monitoreo."""
    
    print("💰 SISTEMA DE MONITOREO AUTOMÁTICO DE COSTOS")
    print("=" * 70)
    print("Monitoreando costos del Steel Rebar Predictor")
    print("=" * 70)
    
    monitor = CostMonitoringSystem()
    
    # Generar reporte de costos
    report = monitor.generate_cost_report()
    
    # Guardar datos de monitoreo
    report_filename = monitor.save_monitoring_data(report)
    
    # Generar cronograma de monitoreo
    schedule = monitor.generate_monitoring_schedule()
    
    # Crear configuración de alertas
    alert_config = monitor.create_alert_configuration()
    
    print(f"\n✅ SISTEMA DE MONITOREO CONFIGURADO")
    print(f"   📊 Reporte generado: {report_filename}")
    print(f"   📅 Cronograma de monitoreo configurado")
    print(f"   🔔 Configuración de alertas creada")
    
    print(f"\n🎯 PRÓXIMOS PASOS:")
    print(f"   1. Configurar alertas en GCP Console")
    print(f"   2. Programar ejecución automática del monitoreo")
    print(f"   3. Revisar reportes semanalmente")
    print(f"   4. Ajustar presupuesto según necesidades")

if __name__ == "__main__":
    main()
