#!/usr/bin/env python3
"""
Análisis detallado de optimización de costos para el Steel Rebar Predictor.
Evalúa el cumplimiento del presupuesto de $5 USD/mes y propone optimizaciones.
"""

import json
import subprocess
import sys
import os
from datetime import datetime, timedelta
import pandas as pd

class CostOptimizationAnalyzer:
    """Analizador de optimización de costos para GCP."""
    
    def __init__(self, project_id="steel-rebar-predictor-deacero"):
        self.project_id = project_id
        self.budget_limit = 5.0  # USD/mes
        self.current_costs = {}
        self.optimization_recommendations = []
    
    def analyze_current_costs(self):
        """Analizar costos actuales del proyecto."""
        
        print("💰 ANÁLISIS DE COSTOS ACTUALES")
        print("=" * 60)
        
        # Cloud Run costs
        cloud_run_costs = self._analyze_cloud_run_costs()
        
        # Container Registry costs
        container_registry_costs = self._analyze_container_registry_costs()
        
        # Cloud Build costs
        cloud_build_costs = self._analyze_cloud_build_costs()
        
        # Memorystore costs (si está habilitado)
        memorystore_costs = self._analyze_memorystore_costs()
        
        # Total estimado
        total_monthly_cost = (
            cloud_run_costs['monthly'] +
            container_registry_costs['monthly'] +
            cloud_build_costs['monthly'] +
            memorystore_costs['monthly']
        )
        
        self.current_costs = {
            'cloud_run': cloud_run_costs,
            'container_registry': container_registry_costs,
            'cloud_build': cloud_build_costs,
            'memorystore': memorystore_costs,
            'total_monthly': total_monthly_cost,
            'budget_limit': self.budget_limit,
            'budget_utilization': (total_monthly_cost / self.budget_limit) * 100
        }
        
        print(f"\n📊 RESUMEN DE COSTOS:")
        print(f"   🚀 Cloud Run: ${cloud_run_costs['monthly']:.2f}/mes")
        print(f"   📦 Container Registry: ${container_registry_costs['monthly']:.2f}/mes")
        print(f"   🏗️ Cloud Build: ${cloud_build_costs['monthly']:.2f}/mes")
        print(f"   💾 Memorystore: ${memorystore_costs['monthly']:.2f}/mes")
        print(f"   💰 TOTAL: ${total_monthly_cost:.2f}/mes")
        print(f"   📊 Presupuesto: ${self.budget_limit:.2f}/mes")
        print(f"   ⚠️ Utilización: {self.current_costs['budget_utilization']:.1f}%")
        
        return self.current_costs
    
    def _analyze_cloud_run_costs(self):
        """Analizar costos de Cloud Run."""
        
        print("\n🚀 Analizando costos de Cloud Run...")
        
        # Configuración actual (estimada)
        current_config = {
            'cpu': 1.0,  # vCPU
            'memory': 1.0,  # GiB
            'requests_per_day': 100,  # Estimado
            'avg_response_time': 2.0,  # segundos
            'uptime_hours': 24  # horas/día
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
        
        total_monthly = cpu_cost + memory_cost + requests_cost
        
        return {
            'config': current_config,
            'pricing': pricing,
            'cpu_cost': cpu_cost,
            'memory_cost': memory_cost,
            'requests_cost': requests_cost,
            'monthly': total_monthly,
            'breakdown': {
                'cpu': f"{cpu_cost:.2f}",
                'memory': f"{memory_cost:.2f}",
                'requests': f"{requests_cost:.2f}"
            }
        }
    
    def _analyze_container_registry_costs(self):
        """Analizar costos de Container Registry."""
        
        print("📦 Analizando costos de Container Registry...")
        
        # Estimaciones basadas en uso típico
        estimated_storage_gb = 0.5  # GB
        pricing_per_gb_month = 0.026  # USD/GB/mes
        
        monthly_cost = estimated_storage_gb * pricing_per_gb_month
        
        return {
            'storage_gb': estimated_storage_gb,
            'pricing_per_gb': pricing_per_gb_month,
            'monthly': monthly_cost
        }
    
    def _analyze_cloud_build_costs(self):
        """Analizar costos de Cloud Build."""
        
        print("🏗️ Analizando costos de Cloud Build...")
        
        # Estimaciones basadas en uso típico
        builds_per_month = 10
        avg_build_time_minutes = 3
        pricing_per_minute = 0.003  # USD/minuto
        
        monthly_cost = builds_per_month * avg_build_time_minutes * pricing_per_minute
        
        return {
            'builds_per_month': builds_per_month,
            'avg_build_time': avg_build_time_minutes,
            'pricing_per_minute': pricing_per_minute,
            'monthly': monthly_cost
        }
    
    def _analyze_memorystore_costs(self):
        """Analizar costos de Memorystore (Redis)."""
        
        print("💾 Analizando costos de Memorystore...")
        
        # Si no está habilitado, costo es 0
        # Si está habilitado, estimar costo
        enabled = False  # Cambiar a True si se habilita Redis
        
        if not enabled:
            return {
                'enabled': False,
                'monthly': 0.0,
                'note': 'Memorystore no habilitado'
            }
        
        # Estimaciones si estuviera habilitado
        memory_gb = 1.0
        pricing_per_gb_hour = 0.054  # USD/GiB-hora
        
        monthly_cost = memory_gb * 24 * 30 * pricing_per_gb_hour
        
        return {
            'enabled': True,
            'memory_gb': memory_gb,
            'pricing_per_gb_hour': pricing_per_gb_hour,
            'monthly': monthly_cost
        }
    
    def generate_optimization_recommendations(self):
        """Generar recomendaciones de optimización."""
        
        print("\n🔧 GENERANDO RECOMENDACIONES DE OPTIMIZACIÓN")
        print("=" * 60)
        
        recommendations = []
        
        # Análisis de Cloud Run
        if self.current_costs['cloud_run']['monthly'] > 2.0:
            recommendations.append({
                'priority': 'HIGH',
                'service': 'Cloud Run',
                'current_cost': self.current_costs['cloud_run']['monthly'],
                'optimization': 'Reducir CPU y memoria',
                'potential_savings': self._calculate_cloud_run_savings(),
                'implementation': 'Cambiar a 0.5 CPU y 512Mi memoria',
                'risk': 'LOW',
                'impact': 'Reducción de ~50% en costos de Cloud Run'
            })
        
        # Análisis de Container Registry
        if self.current_costs['container_registry']['monthly'] > 0.05:
            recommendations.append({
                'priority': 'MEDIUM',
                'service': 'Container Registry',
                'current_cost': self.current_costs['container_registry']['monthly'],
                'optimization': 'Limpiar imágenes antiguas',
                'potential_savings': 0.01,
                'implementation': 'Script de limpieza automática',
                'risk': 'LOW',
                'impact': 'Reducción mínima pero constante'
            })
        
        # Análisis de Cloud Build
        if self.current_costs['cloud_build']['monthly'] > 0.1:
            recommendations.append({
                'priority': 'MEDIUM',
                'service': 'Cloud Build',
                'current_cost': self.current_costs['cloud_build']['monthly'],
                'optimization': 'Optimizar Dockerfile',
                'potential_savings': 0.02,
                'implementation': 'Multi-stage build y cache layers',
                'risk': 'LOW',
                'impact': 'Builds más rápidos y baratos'
            })
        
        # Análisis de presupuesto general
        if self.current_costs['budget_utilization'] > 100:
            recommendations.append({
                'priority': 'CRITICAL',
                'service': 'General',
                'current_cost': self.current_costs['total_monthly'],
                'optimization': 'Aplicar todas las optimizaciones',
                'potential_savings': self._calculate_total_savings(),
                'implementation': 'Implementar todas las recomendaciones',
                'risk': 'MEDIUM',
                'impact': 'Cumplir presupuesto de $5/mes'
            })
        
        self.optimization_recommendations = recommendations
        
        # Mostrar recomendaciones
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. 🎯 {rec['service']} - {rec['priority']} PRIORITY")
            print(f"   💰 Costo actual: ${rec['current_cost']:.2f}/mes")
            print(f"   🔧 Optimización: {rec['optimization']}")
            print(f"   💵 Ahorro potencial: ${rec['potential_savings']:.2f}/mes")
            print(f"   ⚠️ Riesgo: {rec['risk']}")
            print(f"   📈 Impacto: {rec['impact']}")
        
        return recommendations
    
    def _calculate_cloud_run_savings(self):
        """Calcular ahorros potenciales en Cloud Run."""
        
        current_cost = self.current_costs['cloud_run']['monthly']
        
        # Configuración optimizada
        optimized_config = {
            'cpu': 0.5,  # vCPU
            'memory': 0.5,  # GiB (512Mi)
            'requests_per_day': 100,
            'uptime_hours': 24
        }
        
        pricing = self.current_costs['cloud_run']['pricing']
        
        # Cálculos con configuración optimizada
        cpu_cost = optimized_config['cpu'] * optimized_config['uptime_hours'] * 30 * pricing['cpu_per_hour']
        memory_cost = optimized_config['memory'] * optimized_config['uptime_hours'] * 30 * pricing['memory_per_hour']
        requests_cost = (optimized_config['requests_per_day'] * 30) / 1000000 * pricing['requests_per_million']
        
        optimized_total = cpu_cost + memory_cost + requests_cost
        
        return current_cost - optimized_total
    
    def _calculate_total_savings(self):
        """Calcular ahorros totales potenciales."""
        
        total_savings = 0
        
        for rec in self.optimization_recommendations:
            if rec['service'] != 'General':  # Evitar duplicar el total
                total_savings += rec['potential_savings']
        
        return total_savings
    
    def create_optimization_plan(self):
        """Crear plan de optimización paso a paso."""
        
        print("\n📋 PLAN DE OPTIMIZACIÓN PASO A PASO")
        print("=" * 60)
        
        plan = {
            'phase_1': {
                'title': 'Optimizaciones Inmediatas (Sin Riesgo)',
                'duration': '1 día',
                'actions': [
                    {
                        'action': 'Reducir CPU de Cloud Run a 0.5',
                        'command': 'gcloud run services update steel-rebar-predictor --region=us-central1 --cpu=0.5',
                        'savings': self._calculate_cloud_run_savings() * 0.6
                    },
                    {
                        'action': 'Reducir memoria a 512Mi',
                        'command': 'gcloud run services update steel-rebar-predictor --region=us-central1 --memory=512Mi',
                        'savings': self._calculate_cloud_run_savings() * 0.4
                    },
                    {
                        'action': 'Configurar timeout más corto',
                        'command': 'gcloud run services update steel-rebar-predictor --region=us-central1 --timeout=30s',
                        'savings': 0.01
                    }
                ]
            },
            'phase_2': {
                'title': 'Optimizaciones de Desarrollo (Bajo Riesgo)',
                'duration': '1 semana',
                'actions': [
                    {
                        'action': 'Optimizar Dockerfile con multi-stage build',
                        'command': 'Implementar en Dockerfile',
                        'savings': 0.02
                    },
                    {
                        'action': 'Implementar limpieza automática de imágenes',
                        'command': 'Script de limpieza en CI/CD',
                        'savings': 0.01
                    },
                    {
                        'action': 'Configurar presupuesto con alertas',
                        'command': 'gcloud billing budgets create',
                        'savings': 0.0  # Preventivo
                    }
                ]
            },
            'phase_3': {
                'title': 'Optimizaciones Avanzadas (Medio Riesgo)',
                'duration': '2 semanas',
                'actions': [
                    {
                        'action': 'Implementar cache inteligente',
                        'command': 'Optimizar lógica de cache',
                        'savings': 0.05
                    },
                    {
                        'action': 'Optimizar modelo ML para menor uso de memoria',
                        'command': 'Usar perfil "fast" en producción',
                        'savings': 0.03
                    },
                    {
                        'action': 'Configurar auto-scaling más agresivo',
                        'command': 'Ajustar min-instances y concurrency',
                        'savings': 0.02
                    }
                ]
            }
        }
        
        # Mostrar plan
        for phase_name, phase in plan.items():
            print(f"\n{phase_name.upper()}: {phase['title']}")
            print(f"   ⏱️ Duración: {phase['duration']}")
            print(f"   💰 Ahorro estimado: ${sum(action['savings'] for action in phase['actions']):.2f}/mes")
            
            for i, action in enumerate(phase['actions'], 1):
                print(f"   {i}. {action['action']}")
                print(f"      💵 Ahorro: ${action['savings']:.2f}/mes")
        
        return plan
    
    def generate_cost_report(self):
        """Generar reporte completo de costos."""
        
        print("\n📊 GENERANDO REPORTE DE COSTOS")
        print("=" * 60)
        
        # Ejecutar análisis
        self.analyze_current_costs()
        self.generate_optimization_recommendations()
        plan = self.create_optimization_plan()
        
        # Crear reporte
        report = {
            'timestamp': datetime.now().isoformat(),
            'project_id': self.project_id,
            'budget_limit': self.budget_limit,
            'current_costs': self.current_costs,
            'optimization_recommendations': self.optimization_recommendations,
            'optimization_plan': plan,
            'summary': {
                'current_monthly_cost': self.current_costs['total_monthly'],
                'budget_utilization_percent': self.current_costs['budget_utilization'],
                'potential_monthly_savings': self._calculate_total_savings(),
                'optimized_monthly_cost': self.current_costs['total_monthly'] - self._calculate_total_savings(),
                'budget_compliance': (self.current_costs['total_monthly'] - self._calculate_total_savings()) <= self.budget_limit
            }
        }
        
        # Guardar reporte
        report_filename = f'cost_optimization_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        report_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'predictions', report_filename)
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Reporte guardado: {report_filename}")
        
        # Mostrar resumen final
        print(f"\n🎯 RESUMEN FINAL:")
        print(f"   💰 Costo actual: ${self.current_costs['total_monthly']:.2f}/mes")
        print(f"   📊 Presupuesto: ${self.budget_limit:.2f}/mes")
        print(f"   ⚠️ Utilización: {self.current_costs['budget_utilization']:.1f}%")
        print(f"   💵 Ahorro potencial: ${self._calculate_total_savings():.2f}/mes")
        print(f"   🎯 Costo optimizado: ${self.current_costs['total_monthly'] - self._calculate_total_savings():.2f}/mes")
        
        compliance = "✅ CUMPLE" if report['summary']['budget_compliance'] else "❌ EXCEDE"
        print(f"   📋 Presupuesto: {compliance}")
        
        return report

def main():
    """Función principal para análisis de costos."""
    
    print("💰 ANÁLISIS DE OPTIMIZACIÓN DE COSTOS - STEEL REBAR PREDICTOR")
    print("=" * 70)
    print("Evaluando cumplimiento del presupuesto de $5 USD/mes")
    print("=" * 70)
    
    analyzer = CostOptimizationAnalyzer()
    report = analyzer.generate_cost_report()
    
    print(f"\n✅ ANÁLISIS COMPLETADO")
    print(f"   📊 {len(analyzer.optimization_recommendations)} recomendaciones generadas")
    print(f"   📋 Plan de optimización en 3 fases")
    print(f"   🎯 Objetivo: Cumplir presupuesto de $5 USD/mes")

if __name__ == "__main__":
    main()
