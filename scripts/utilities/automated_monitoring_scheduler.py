#!/usr/bin/env python3
"""
Sistema de monitoreo automático programado para el Steel Rebar Predictor.
Configura monitoreo semanal, mensual y alertas automáticas.
"""

import json
import os
import time
from datetime import datetime, timedelta
import subprocess
import sys

class AutomatedMonitoringScheduler:
    """Programador de monitoreo automático."""
    
    def __init__(self, project_id="steel-rebar-predictor-deacero"):
        self.project_id = project_id
        self.monitoring_logs = []
        self.scheduled_jobs = []
    
    def create_monitoring_schedule(self):
        """Crear cronograma de monitoreo."""
        
        print("📅 CONFIGURANDO MONITOREO AUTOMÁTICO")
        print("=" * 70)
        print(f"Proyecto: {self.project_id}")
        print("=" * 70)
        
        # Configurar trabajos programados
        schedule_config = {
            'daily_monitoring': {
                'title': 'Monitoreo Diario',
                'description': 'Verificación diaria de costos y rendimiento',
                'schedule': '09:00',
                'command': 'python scripts/utilities/cost_monitoring_system.py --mode daily',
                'enabled': True,
                'priority': 'HIGH'
            },
            'weekly_report': {
                'title': 'Reporte Semanal',
                'description': 'Análisis semanal completo de costos y rendimiento',
                'schedule': 'monday 10:00',
                'command': 'python scripts/utilities/cost_monitoring_system.py --mode weekly',
                'enabled': True,
                'priority': 'HIGH'
            },
            'monthly_analysis': {
                'title': 'Análisis Mensual',
                'description': 'Análisis mensual completo y recomendaciones',
                'schedule': '1 11:00',
                'command': 'python scripts/utilities/cost_monitoring_system.py --mode monthly',
                'enabled': True,
                'priority': 'MEDIUM'
            },
            'performance_check': {
                'title': 'Verificación de Rendimiento',
                'description': 'Verificación semanal del rendimiento de la API',
                'schedule': 'wednesday 14:00',
                'command': 'python scripts/utilities/performance_benchmark.py',
                'enabled': True,
                'priority': 'MEDIUM'
            },
            'budget_alert_check': {
                'title': 'Verificación de Alertas de Presupuesto',
                'description': 'Verificación diaria de alertas de presupuesto',
                'schedule': '08:00',
                'command': 'python scripts/utilities/budget_alerts_configurator.py --check',
                'enabled': True,
                'priority': 'HIGH'
            }
        }
        
        return schedule_config
    
    def create_cron_configuration(self):
        """Crear configuración de cron para Linux/Unix."""
        
        print("\n⏰ CONFIGURACIÓN DE CRON")
        print("=" * 70)
        
        cron_config = {
            'daily_monitoring': {
                'cron': '0 9 * * *',
                'description': 'Monitoreo diario a las 9:00 AM',
                'command': f'cd /path/to/steel-rebar-predictor && python scripts/utilities/cost_monitoring_system.py --mode daily >> logs/monitoring.log 2>&1'
            },
            'weekly_report': {
                'cron': '0 10 * * 1',
                'description': 'Reporte semanal los lunes a las 10:00 AM',
                'command': f'cd /path/to/steel-rebar-predictor && python scripts/utilities/cost_monitoring_system.py --mode weekly >> logs/monitoring.log 2>&1'
            },
            'monthly_analysis': {
                'cron': '0 11 1 * *',
                'description': 'Análisis mensual el día 1 a las 11:00 AM',
                'command': f'cd /path/to/steel-rebar-predictor && python scripts/utilities/cost_monitoring_system.py --mode monthly >> logs/monitoring.log 2>&1'
            },
            'performance_check': {
                'cron': '0 14 * * 3',
                'description': 'Verificación de rendimiento los miércoles a las 2:00 PM',
                'command': f'cd /path/to/steel-rebar-predictor && python scripts/utilities/performance_benchmark.py >> logs/performance.log 2>&1'
            },
            'budget_alert_check': {
                'cron': '0 8 * * *',
                'description': 'Verificación de alertas de presupuesto a las 8:00 AM',
                'command': f'cd /path/to/steel-rebar-predictor && python scripts/utilities/budget_alerts_configurator.py --check >> logs/budget.log 2>&1'
            }
        }
        
        return cron_config
    
    def create_windows_task_configuration(self):
        """Crear configuración de tareas programadas para Windows."""
        
        print("\n🪟 CONFIGURACIÓN DE TAREAS PROGRAMADAS (WINDOWS)")
        print("=" * 70)
        
        windows_tasks = {
            'daily_monitoring': {
                'task_name': 'SteelRebarPredictor_DailyMonitoring',
                'description': 'Monitoreo diario de costos y rendimiento',
                'schedule': 'Daily at 9:00 AM',
                'command': f'python scripts/utilities/cost_monitoring_system.py --mode daily',
                'working_directory': 'C:\\path\\to\\steel-rebar-predictor'
            },
            'weekly_report': {
                'task_name': 'SteelRebarPredictor_WeeklyReport',
                'description': 'Reporte semanal completo',
                'schedule': 'Weekly on Monday at 10:00 AM',
                'command': f'python scripts/utilities/cost_monitoring_system.py --mode weekly',
                'working_directory': 'C:\\path\\to\\steel-rebar-predictor'
            },
            'monthly_analysis': {
                'task_name': 'SteelRebarPredictor_MonthlyAnalysis',
                'description': 'Análisis mensual completo',
                'schedule': 'Monthly on day 1 at 11:00 AM',
                'command': f'python scripts/utilities/cost_monitoring_system.py --mode monthly',
                'working_directory': 'C:\\path\\to\\steel-rebar-predictor'
            }
        }
        
        return windows_tasks
    
    def create_monitoring_scripts(self):
        """Crear scripts de monitoreo."""
        
        print("\n📜 CREANDO SCRIPTS DE MONITOREO")
        print("=" * 70)
        
        scripts = {
            'start_monitoring': {
                'title': 'Script de Inicio de Monitoreo',
                'content': f'''#!/bin/bash
# Script para iniciar el sistema de monitoreo automático
# Proyecto: {self.project_id}

echo "🚀 Iniciando sistema de monitoreo automático..."

# Crear directorio de logs si no existe
mkdir -p logs

# Verificar que Python esté disponible
python3 --version || python --version

# Verificar que los scripts existan
if [ ! -f "scripts/utilities/cost_monitoring_system.py" ]; then
    echo "❌ Error: Script de monitoreo de costos no encontrado"
    exit 1
fi

if [ ! -f "scripts/utilities/performance_benchmark.py" ]; then
    echo "❌ Error: Script de benchmark de rendimiento no encontrado"
    exit 1
fi

echo "✅ Verificaciones completadas"
echo "📅 Sistema de monitoreo iniciado"
echo "📊 Logs se guardarán en: logs/monitoring.log"

# Ejecutar monitoreo inicial
python3 scripts/utilities/cost_monitoring_system.py --mode daily

echo "🎯 Monitoreo inicial completado"
''',
                'file_name': 'start_monitoring.sh'
            },
            'stop_monitoring': {
                'title': 'Script de Parada de Monitoreo',
                'content': f'''#!/bin/bash
# Script para detener el sistema de monitoreo automático
# Proyecto: {self.project_id}

echo "⏹️ Deteniendo sistema de monitoreo automático..."

# Matar procesos de monitoreo
pkill -f "cost_monitoring_system.py"
pkill -f "performance_benchmark.py"

# Limpiar trabajos de cron (opcional)
# crontab -r

echo "✅ Sistema de monitoreo detenido"
echo "📊 Logs disponibles en: logs/"
''',
                'file_name': 'stop_monitoring.sh'
            },
            'monitoring_status': {
                'title': 'Script de Estado del Monitoreo',
                'content': f'''#!/bin/bash
# Script para verificar el estado del monitoreo
# Proyecto: {self.project_id}

echo "📊 Estado del Sistema de Monitoreo"
echo "=================================="

# Verificar procesos activos
echo "🔍 Procesos activos:"
ps aux | grep -E "(cost_monitoring|performance_benchmark)" | grep -v grep

# Verificar trabajos de cron
echo "⏰ Trabajos programados:"
crontab -l 2>/dev/null | grep -E "(monitoring|benchmark)" || echo "No hay trabajos programados"

# Verificar logs recientes
echo "📄 Logs recientes:"
if [ -d "logs" ]; then
    ls -la logs/ | tail -5
else
    echo "Directorio de logs no encontrado"
fi

# Verificar archivos de configuración
echo "⚙️ Archivos de configuración:"
ls -la scripts/utilities/*monitoring*.py 2>/dev/null || echo "Scripts de monitoreo no encontrados"

echo "✅ Verificación completada"
''',
                'file_name': 'monitoring_status.sh'
            }
        }
        
        return scripts
    
    def create_cloud_scheduler_configuration(self):
        """Crear configuración para Google Cloud Scheduler."""
        
        print("\n☁️ CONFIGURACIÓN DE GOOGLE CLOUD SCHEDULER")
        print("=" * 70)
        
        cloud_scheduler_jobs = {
            'daily_monitoring': {
                'job_name': 'steel-rebar-daily-monitoring',
                'description': 'Monitoreo diario de costos y rendimiento',
                'schedule': '0 9 * * *',
                'timezone': 'America/Mexico_City',
                'target_type': 'HTTP',
                'target_url': f'https://{self.project_id}.run.app/monitoring/daily',
                'method': 'POST',
                'headers': {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer $(gcloud auth print-access-token)'
                }
            },
            'weekly_report': {
                'job_name': 'steel-rebar-weekly-report',
                'description': 'Reporte semanal completo',
                'schedule': '0 10 * * 1',
                'timezone': 'America/Mexico_City',
                'target_type': 'HTTP',
                'target_url': f'https://{self.project_id}.run.app/monitoring/weekly',
                'method': 'POST',
                'headers': {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer $(gcloud auth print-access-token)'
                }
            },
            'monthly_analysis': {
                'job_name': 'steel-rebar-monthly-analysis',
                'description': 'Análisis mensual completo',
                'schedule': '0 11 1 * *',
                'timezone': 'America/Mexico_City',
                'target_type': 'HTTP',
                'target_url': f'https://{self.project_id}.run.app/monitoring/monthly',
                'method': 'POST',
                'headers': {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer $(gcloud auth print-access-token)'
                }
            }
        }
        
        return cloud_scheduler_jobs
    
    def create_monitoring_endpoints(self):
        """Crear endpoints de monitoreo para la API."""
        
        print("\n🌐 CREANDO ENDPOINTS DE MONITOREO")
        print("=" * 70)
        
        endpoints = {
            'daily_monitoring': {
                'endpoint': '/monitoring/daily',
                'method': 'POST',
                'description': 'Ejecutar monitoreo diario',
                'code': '''
@app.post("/monitoring/daily")
async def daily_monitoring():
    """Ejecutar monitoreo diario."""
    try:
        # Importar sistema de monitoreo
        from scripts.utilities.cost_monitoring_system import CostMonitoringSystem
        
        monitor = CostMonitoringSystem()
        report = monitor.generate_cost_report()
        
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "report": report
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
'''
            },
            'weekly_report': {
                'endpoint': '/monitoring/weekly',
                'method': 'POST',
                'description': 'Generar reporte semanal',
                'code': '''
@app.post("/monitoring/weekly")
async def weekly_report():
    """Generar reporte semanal."""
    try:
        # Importar sistema de monitoreo
        from scripts.utilities.cost_monitoring_system import CostMonitoringSystem
        
        monitor = CostMonitoringSystem()
        report = monitor.generate_cost_report()
        
        # Agregar análisis semanal
        weekly_analysis = {
            "trend_analysis": "Análisis de tendencias semanales",
            "cost_prediction": "Predicción de costos para la próxima semana",
            "recommendations": "Recomendaciones basadas en datos semanales"
        }
        
        report["weekly_analysis"] = weekly_analysis
        
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "report": report
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
'''
            }
        }
        
        return endpoints
    
    def save_monitoring_configuration(self, schedule_config, cron_config, windows_tasks, scripts, cloud_scheduler, endpoints):
        """Guardar configuración completa de monitoreo."""
        
        monitoring_package = {
            'timestamp': datetime.now().isoformat(),
            'project_id': self.project_id,
            'schedule_configuration': schedule_config,
            'cron_configuration': cron_config,
            'windows_tasks': windows_tasks,
            'monitoring_scripts': scripts,
            'cloud_scheduler_jobs': cloud_scheduler,
            'monitoring_endpoints': endpoints,
            'setup_instructions': {
                'linux_unix': 'Usar configuración de cron',
                'windows': 'Usar tareas programadas',
                'cloud': 'Usar Google Cloud Scheduler',
                'manual': 'Usar scripts de monitoreo'
            },
            'estimated_setup_time': '30 minutos'
        }
        
        # Guardar configuración
        config_filename = f'automated_monitoring_configuration_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'predictions', config_filename)
        
        with open(config_path, 'w') as f:
            json.dump(monitoring_package, f, indent=2)
        
        # Guardar scripts
        scripts_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'predictions')
        
        for script_name, script_data in scripts.items():
            script_file = os.path.join(scripts_dir, script_data['file_name'])
            with open(script_file, 'w', encoding='utf-8') as f:
                f.write(script_data['content'])
            # Hacer ejecutable
            os.chmod(script_file, 0o755)
        
        print(f"\n💾 CONFIGURACIÓN DE MONITOREO GUARDADA:")
        print(f"   📁 Archivo principal: {config_filename}")
        print(f"   📜 Scripts: {len(scripts)} scripts ejecutables")
        print(f"   ⏱️ Tiempo estimado: {monitoring_package['estimated_setup_time']}")
        
        return config_filename
    
    def display_setup_summary(self):
        """Mostrar resumen de configuración."""
        
        print(f"\n🎯 RESUMEN DE CONFIGURACIÓN DE MONITOREO:")
        print("=" * 70)
        
        print(f"📅 CRONOGRAMA DE MONITOREO:")
        print(f"   🌅 Diario (9:00 AM): Verificación de costos y rendimiento")
        print(f"   📊 Semanal (Lunes 10:00 AM): Reporte semanal completo")
        print(f"   📈 Mensual (Día 1, 11:00 AM): Análisis mensual completo")
        print(f"   ⚡ Rendimiento (Miércoles 2:00 PM): Verificación de API")
        print(f"   💰 Presupuesto (8:00 AM): Verificación de alertas")
        
        print(f"\n🛠️ OPCIONES DE IMPLEMENTACIÓN:")
        print(f"   🐧 Linux/Unix: Configuración de cron")
        print(f"   🪟 Windows: Tareas programadas")
        print(f"   ☁️ Google Cloud: Cloud Scheduler")
        print(f"   🔧 Manual: Scripts de monitoreo")
        
        print(f"\n📋 ARCHIVOS GENERADOS:")
        print(f"   📜 start_monitoring.sh - Iniciar monitoreo")
        print(f"   📜 stop_monitoring.sh - Detener monitoreo")
        print(f"   📜 monitoring_status.sh - Verificar estado")
        print(f"   📄 Configuración de cron")
        print(f"   📄 Configuración de tareas de Windows")
        print(f"   📄 Configuración de Cloud Scheduler")

def main():
    """Función principal para configurar monitoreo automático."""
    
    print("📅 CONFIGURADOR DE MONITOREO AUTOMÁTICO")
    print("=" * 70)
    print("Configurando monitoreo programado para Steel Rebar Predictor")
    print("=" * 70)
    
    scheduler = AutomatedMonitoringScheduler()
    
    # Generar configuraciones
    schedule_config = scheduler.create_monitoring_schedule()
    cron_config = scheduler.create_cron_configuration()
    windows_tasks = scheduler.create_windows_task_configuration()
    scripts = scheduler.create_monitoring_scripts()
    cloud_scheduler = scheduler.create_cloud_scheduler_configuration()
    endpoints = scheduler.create_monitoring_endpoints()
    
    # Guardar configuración
    config_filename = scheduler.save_monitoring_configuration(schedule_config, cron_config, windows_tasks, scripts, cloud_scheduler, endpoints)
    
    # Mostrar resumen
    scheduler.display_setup_summary()
    
    print(f"\n✅ CONFIGURACIÓN DE MONITOREO COMPLETADA")
    print(f"   📦 Archivo: {config_filename}")
    print(f"   📅 Cronograma: Diario, semanal, mensual")
    print(f"   📜 Scripts: {len(scripts)} scripts")
    print(f"   🌐 Endpoints: {len(endpoints)} endpoints")

if __name__ == "__main__":
    main()
