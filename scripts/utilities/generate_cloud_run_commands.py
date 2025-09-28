#!/usr/bin/env python3
"""
Script para generar comandos de optimización de Cloud Run.
Genera los comandos que deben ejecutarse manualmente en GCP Console o con gcloud CLI.
"""

import json
from datetime import datetime

class CloudRunCommandGenerator:
    """Generador de comandos para optimizar Cloud Run."""
    
    def __init__(self, project_id="steel-rebar-predictor-deacero", region="us-central1"):
        self.project_id = project_id
        self.region = region
        self.service_name = "steel-rebar-predictor"
    
    def generate_optimization_commands(self):
        """Generar comandos de optimización."""
        
        print("🚀 GENERADOR DE COMANDOS DE OPTIMIZACIÓN - CLOUD RUN")
        print("=" * 70)
        print(f"Proyecto: {self.project_id}")
        print(f"Región: {self.region}")
        print(f"Servicio: {self.service_name}")
        print("=" * 70)
        
        commands = [
            {
                'name': 'Reducir CPU a 0.5 vCPU',
                'command': f'gcloud run services update {self.service_name} --region={self.region} --cpu=0.5 --project={self.project_id}',
                'savings': '$8.64/mes',
                'description': 'Reduce el costo de CPU de $17.28 a $8.64/mes'
            },
            {
                'name': 'Reducir memoria a 512Mi',
                'command': f'gcloud run services update {self.service_name} --region={self.region} --memory=512Mi --project={self.project_id}',
                'savings': '$0.90/mes',
                'description': 'Reduce el costo de memoria de $1.80 a $0.90/mes'
            },
            {
                'name': 'Configurar timeout a 30s',
                'command': f'gcloud run services update {self.service_name} --region={self.region} --timeout=30s --project={self.project_id}',
                'savings': '$0.01/mes',
                'description': 'Optimiza el timeout para reducir costos de procesamiento'
            },
            {
                'name': 'Limitar instancias máximas a 5',
                'command': f'gcloud run services update {self.service_name} --region={self.region} --max-instances=5 --project={self.project_id}',
                'savings': 'Preventivo',
                'description': 'Previene escalado excesivo y costos inesperados'
            },
            {
                'name': 'Configurar concurrencia a 50',
                'command': f'gcloud run services update {self.service_name} --region={self.region} --concurrency=50 --project={self.project_id}',
                'savings': 'Eficiencia',
                'description': 'Optimiza el uso de recursos por instancia'
            }
        ]
        
        print(f"\n📋 COMANDOS DE OPTIMIZACIÓN:")
        print("=" * 70)
        
        for i, cmd in enumerate(commands, 1):
            print(f"\n{i}. 🔧 {cmd['name']}")
            print(f"   💰 Ahorro: {cmd['savings']}")
            print(f"   📝 Descripción: {cmd['description']}")
            print(f"   💻 Comando:")
            print(f"      {cmd['command']}")
        
        # Comando combinado
        print(f"\n🚀 COMANDO COMBINADO (ejecutar todo de una vez):")
        print("=" * 70)
        
        combined_command = f"""gcloud run services update {self.service_name} \\
    --region={self.region} \\
    --cpu=0.5 \\
    --memory=512Mi \\
    --timeout=30s \\
    --max-instances=5 \\
    --concurrency=50 \\
    --project={self.project_id}"""
        
        print(combined_command)
        
        return commands
    
    def generate_verification_commands(self):
        """Generar comandos de verificación."""
        
        print(f"\n🔍 COMANDOS DE VERIFICACIÓN:")
        print("=" * 70)
        
        verification_commands = [
            {
                'name': 'Verificar configuración actual',
                'command': f'gcloud run services describe {self.service_name} --region={self.region} --project={self.project_id}',
                'description': 'Muestra la configuración actual del servicio'
            },
            {
                'name': 'Verificar recursos específicos',
                'command': f'gcloud run services describe {self.service_name} --region={self.region} --project={self.project_id} --format="value(spec.template.spec.containers[0].resources.limits.cpu,spec.template.spec.containers[0].resources.limits.memory)"',
                'description': 'Muestra solo CPU y memoria'
            },
            {
                'name': 'Verificar escalado',
                'command': f'gcloud run services describe {self.service_name} --region={self.region} --project={self.project_id} --format="value(spec.template.metadata.annotations.autoscaling.knative.dev/maxScale)"',
                'description': 'Muestra configuración de escalado'
            }
        ]
        
        for i, cmd in enumerate(verification_commands, 1):
            print(f"\n{i}. 🔍 {cmd['name']}")
            print(f"   📝 Descripción: {cmd['description']}")
            print(f"   💻 Comando:")
            print(f"      {cmd['command']}")
        
        return verification_commands
    
    def generate_cost_analysis(self):
        """Generar análisis de costos."""
        
        print(f"\n💰 ANÁLISIS DE COSTOS:")
        print("=" * 70)
        
        # Costos antes de optimización
        before_costs = {
            'cpu': 1.0 * 24 * 30 * 0.024,  # 1 vCPU * 24h * 30d * $0.024/vCPU-h
            'memory': 1.0 * 24 * 30 * 0.0025,  # 1 GiB * 24h * 30d * $0.0025/GiB-h
            'requests': 100 * 30 / 1000000 * 0.40  # 100 req/d * 30d / 1M * $0.40/1M
        }
        before_total = sum(before_costs.values())
        
        # Costos después de optimización
        after_costs = {
            'cpu': 0.5 * 24 * 30 * 0.024,  # 0.5 vCPU * 24h * 30d * $0.024/vCPU-h
            'memory': 0.5 * 24 * 30 * 0.0025,  # 0.5 GiB * 24h * 30d * $0.0025/GiB-h
            'requests': 100 * 30 / 1000000 * 0.40  # Mismo número de requests
        }
        after_total = sum(after_costs.values())
        
        savings = before_total - after_total
        savings_percent = (savings / before_total) * 100
        
        print(f"📊 Comparación de costos mensuales:")
        print(f"   🖥️ CPU:")
        print(f"      Antes: ${before_costs['cpu']:.2f}")
        print(f"      Después: ${after_costs['cpu']:.2f}")
        print(f"      Ahorro: ${before_costs['cpu'] - after_costs['cpu']:.2f}")
        
        print(f"   💾 Memoria:")
        print(f"      Antes: ${before_costs['memory']:.2f}")
        print(f"      Después: ${after_costs['memory']:.2f}")
        print(f"      Ahorro: ${before_costs['memory'] - after_costs['memory']:.2f}")
        
        print(f"   📨 Requests:")
        print(f"      Antes: ${before_costs['requests']:.2f}")
        print(f"      Después: ${after_costs['requests']:.2f}")
        print(f"      Ahorro: ${before_costs['requests'] - after_costs['requests']:.2f}")
        
        print(f"\n💰 RESUMEN:")
        print(f"   💵 Costo antes: ${before_total:.2f}/mes")
        print(f"   💵 Costo después: ${after_total:.2f}/mes")
        print(f"   💰 Ahorro total: ${savings:.2f}/mes ({savings_percent:.1f}%)")
        print(f"   📊 Presupuesto objetivo: $5.00/mes")
        print(f"   ✅ Cumplimiento: {'SÍ' if after_total <= 5.0 else 'NO'}")
        
        return {
            'before_total': before_total,
            'after_total': after_total,
            'savings': savings,
            'savings_percent': savings_percent,
            'budget_compliance': after_total <= 5.0
        }
    
    def generate_instructions(self):
        """Generar instrucciones paso a paso."""
        
        print(f"\n📋 INSTRUCCIONES PASO A PASO:")
        print("=" * 70)
        
        instructions = [
            {
                'step': 1,
                'title': 'Preparar entorno',
                'description': 'Asegúrate de tener gcloud CLI instalado y configurado',
                'commands': [
                    'gcloud auth login',
                    f'gcloud config set project {self.project_id}'
                ]
            },
            {
                'step': 2,
                'title': 'Verificar estado actual',
                'description': 'Revisar la configuración actual del servicio',
                'commands': [
                    f'gcloud run services describe {self.service_name} --region={self.region} --project={self.project_id}'
                ]
            },
            {
                'step': 3,
                'title': 'Aplicar optimizaciones',
                'description': 'Ejecutar el comando combinado de optimización',
                'commands': [
                    f'gcloud run services update {self.service_name} --region={self.region} --cpu=0.5 --memory=512Mi --timeout=30s --max-instances=5 --concurrency=50 --project={self.project_id}'
                ]
            },
            {
                'step': 4,
                'title': 'Verificar cambios',
                'description': 'Confirmar que las optimizaciones se aplicaron correctamente',
                'commands': [
                    f'gcloud run services describe {self.service_name} --region={self.region} --project={self.project_id} --format="value(spec.template.spec.containers[0].resources.limits.cpu,spec.template.spec.containers[0].resources.limits.memory)"'
                ]
            },
            {
                'step': 5,
                'title': 'Probar servicio',
                'description': 'Verificar que el servicio funciona correctamente',
                'commands': [
                    f'curl https://{self.service_name}-{self.project_id}.{self.region}.run.app/health'
                ]
            }
        ]
        
        for instruction in instructions:
            print(f"\n{instruction['step']}. 📝 {instruction['title']}")
            print(f"   📋 Descripción: {instruction['description']}")
            print(f"   💻 Comandos:")
            for cmd in instruction['commands']:
                print(f"      {cmd}")
        
        return instructions
    
    def save_commands_to_file(self, commands, verification_commands, cost_analysis, instructions):
        """Guardar comandos en archivo."""
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'project_id': self.project_id,
            'region': self.region,
            'service_name': self.service_name,
            'optimization_commands': commands,
            'verification_commands': verification_commands,
            'cost_analysis': cost_analysis,
            'instructions': instructions
        }
        
        # Guardar reporte
        report_filename = f'cloud_run_optimization_commands_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        report_path = f'../../data/predictions/{report_filename}'
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n💾 COMANDOS GUARDADOS:")
        print(f"   📁 Archivo: {report_filename}")
        print(f"   📍 Ubicación: {report_path}")
        
        return report_filename

def main():
    """Función principal para generar comandos de optimización."""
    
    generator = CloudRunCommandGenerator()
    
    # Generar comandos de optimización
    commands = generator.generate_optimization_commands()
    
    # Generar comandos de verificación
    verification_commands = generator.generate_verification_commands()
    
    # Generar análisis de costos
    cost_analysis = generator.generate_cost_analysis()
    
    # Generar instrucciones
    instructions = generator.generate_instructions()
    
    # Guardar en archivo
    report_filename = generator.save_commands_to_file(commands, verification_commands, cost_analysis, instructions)
    
    print(f"\n✅ COMANDOS GENERADOS EXITOSAMENTE")
    print(f"   📋 {len(commands)} comandos de optimización")
    print(f"   🔍 {len(verification_commands)} comandos de verificación")
    print(f"   📊 Análisis de costos completo")
    print(f"   📝 Instrucciones paso a paso")
    print(f"   💾 Archivo guardado: {report_filename}")
    
    print(f"\n🎯 PRÓXIMOS PASOS:")
    print(f"   1. Ejecutar comandos en GCP Console o con gcloud CLI")
    print(f"   2. Verificar que las optimizaciones se aplicaron")
    print(f"   3. Probar el servicio después de los cambios")
    print(f"   4. Monitorear costos mensualmente")

if __name__ == "__main__":
    main()
