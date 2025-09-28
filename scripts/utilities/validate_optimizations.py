#!/usr/bin/env python3
"""
Script de validación de optimizaciones implementadas.
Verifica que todas las optimizaciones funcionen correctamente.
"""

import sys
import os
import time
import subprocess
from datetime import datetime

class OptimizationValidator:
    """Validador de optimizaciones implementadas."""
    
    def __init__(self):
        self.results = {}
        self.start_time = time.time()
    
    def validate_training_profiles(self):
        """Validar que los perfiles de entrenamiento funcionen."""
        
        print("🧪 VALIDANDO PERFILES DE ENTRENAMIENTO")
        print("=" * 50)
        
        try:
            # Importar el entrenador optimizado
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'model_training'))
            from optimized_training import OptimizedSteelRebarTrainer
            
            trainer = OptimizedSteelRebarTrainer()
            
            # Crear datos de prueba pequeños
            data = trainer.create_optimized_training_data()
            enhanced_data = trainer.create_essential_features(data)
            
            # Probar perfil ultra_fast
            print("\n⚡ Probando perfil ultra_fast...")
            start_time = time.time()
            
            result = trainer.train_with_profile(enhanced_data, 'ultra_fast')
            
            ultra_fast_time = time.time() - start_time
            
            print(f"   ✅ ultra_fast: {result['total_time']:.2f}s")
            print(f"   📊 Confianza: {result['model_confidence']:.3f}")
            
            # Probar perfil balanced
            print("\n⚖️ Probando perfil balanced...")
            start_time = time.time()
            
            result = trainer.train_with_profile(enhanced_data, 'balanced')
            
            balanced_time = time.time() - start_time
            
            print(f"   ✅ balanced: {result['total_time']:.2f}s")
            print(f"   📊 Confianza: {result['model_confidence']:.3f}")
            
            self.results['training_profiles'] = {
                'ultra_fast_time': ultra_fast_time,
                'balanced_time': balanced_time,
                'ultra_fast_confidence': result['model_confidence'],
                'balanced_confidence': result['model_confidence'],
                'status': 'SUCCESS'
            }
            
            print(f"\n✅ Perfiles de entrenamiento validados exitosamente")
            
        except Exception as e:
            print(f"❌ Error validando perfiles: {e}")
            self.results['training_profiles'] = {
                'status': 'FAILED',
                'error': str(e)
            }
    
    def validate_cost_optimization(self):
        """Validar que las optimizaciones de costo funcionen."""
        
        print("\n💰 VALIDANDO OPTIMIZACIONES DE COSTO")
        print("=" * 50)
        
        try:
            # Importar el analizador de costos
            sys.path.append(os.path.join(os.path.dirname(__file__)))
            from cost_optimization_analyzer import CostOptimizationAnalyzer
            
            analyzer = CostOptimizationAnalyzer()
            
            # Analizar costos actuales
            current_costs = analyzer.analyze_current_costs()
            
            # Generar recomendaciones
            recommendations = analyzer.generate_optimization_recommendations()
            
            # Crear plan de optimización
            plan = analyzer.create_optimization_plan()
            
            self.results['cost_optimization'] = {
                'current_monthly_cost': current_costs['total_monthly'],
                'budget_limit': current_costs['budget_limit'],
                'budget_utilization': current_costs['budget_utilization'],
                'recommendations_count': len(recommendations),
                'optimization_phases': len(plan),
                'status': 'SUCCESS'
            }
            
            print(f"   ✅ Costo actual: ${current_costs['total_monthly']:.2f}/mes")
            print(f"   📊 Presupuesto: ${current_costs['budget_limit']:.2f}/mes")
            print(f"   ⚠️ Utilización: {current_costs['budget_utilization']:.1f}%")
            print(f"   📋 Recomendaciones: {len(recommendations)}")
            print(f"   📅 Fases de optimización: {len(plan)}")
            
        except Exception as e:
            print(f"❌ Error validando optimizaciones de costo: {e}")
            self.results['cost_optimization'] = {
                'status': 'FAILED',
                'error': str(e)
            }
    
    def validate_performance_benchmark(self):
        """Validar que los benchmarks de rendimiento funcionen."""
        
        print("\n🏁 VALIDANDO BENCHMARKS DE RENDIMIENTO")
        print("=" * 50)
        
        try:
            # Importar el benchmark de rendimiento
            sys.path.append(os.path.join(os.path.dirname(__file__)))
            from performance_benchmark import PerformanceBenchmark
            
            benchmark = PerformanceBenchmark()
            
            # Ejecutar benchmark de entrenamiento
            training_results = benchmark.benchmark_training_times()
            
            # Ejecutar benchmark de predicción
            prediction_results = benchmark.benchmark_prediction_times()
            
            # Ejecutar benchmark de memoria
            memory_results = benchmark.benchmark_memory_usage()
            
            self.results['performance_benchmark'] = {
                'training_profiles_tested': len([r for r in training_results.values() if r is not None]),
                'prediction_sizes_tested': len(prediction_results),
                'memory_operations_tested': len(memory_results),
                'status': 'SUCCESS'
            }
            
            print(f"   ✅ Perfiles de entrenamiento probados: {len([r for r in training_results.values() if r is not None])}")
            print(f"   ✅ Tamaños de predicción probados: {len(prediction_results)}")
            print(f"   ✅ Operaciones de memoria probadas: {len(memory_results)}")
            
        except Exception as e:
            print(f"❌ Error validando benchmarks: {e}")
            self.results['performance_benchmark'] = {
                'status': 'FAILED',
                'error': str(e)
            }
    
    def validate_model_configuration(self):
        """Validar que la configuración del modelo esté optimizada."""
        
        print("\n🤖 VALIDANDO CONFIGURACIÓN DEL MODELO")
        print("=" * 50)
        
        try:
            # Leer configuración del modelo principal
            model_file = os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'app', 'models', 'ml_model.py')
            
            with open(model_file, 'r') as f:
                content = f.read()
            
            # Verificar que use perfil balanced
            if 'n_estimators=150' in content and 'max_depth=12' in content:
                print("   ✅ Modelo configurado con perfil balanced")
                model_optimized = True
            else:
                print("   ❌ Modelo no configurado con perfil balanced")
                model_optimized = False
            
            # Verificar que tenga optimizaciones
            optimizations = [
                'min_samples_split=3',
                'min_samples_leaf=1',
                'max_features=\'sqrt\'',
                'bootstrap=True',
                'oob_score=True'
            ]
            
            optimizations_found = sum(1 for opt in optimizations if opt in content)
            
            print(f"   📊 Optimizaciones encontradas: {optimizations_found}/{len(optimizations)}")
            
            self.results['model_configuration'] = {
                'profile_balanced': model_optimized,
                'optimizations_found': optimizations_found,
                'total_optimizations': len(optimizations),
                'status': 'SUCCESS' if model_optimized else 'PARTIAL'
            }
            
        except Exception as e:
            print(f"❌ Error validando configuración del modelo: {e}")
            self.results['model_configuration'] = {
                'status': 'FAILED',
                'error': str(e)
            }
    
    def generate_validation_report(self):
        """Generar reporte de validación."""
        
        print("\n📋 GENERANDO REPORTE DE VALIDACIÓN")
        print("=" * 50)
        
        total_time = time.time() - self.start_time
        
        # Contar resultados exitosos
        successful_validations = sum(1 for result in self.results.values() if result.get('status') == 'SUCCESS')
        total_validations = len(self.results)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_validation_time': total_time,
            'successful_validations': successful_validations,
            'total_validations': total_validations,
            'success_rate': (successful_validations / total_validations) * 100 if total_validations > 0 else 0,
            'validation_results': self.results
        }
        
        # Guardar reporte
        report_filename = f'optimization_validation_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        report_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'predictions', report_filename)
        
        import json
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Reporte guardado: {report_filename}")
        
        # Mostrar resumen
        print(f"\n🎯 RESUMEN DE VALIDACIÓN:")
        print(f"   ⏱️ Tiempo total: {total_time:.2f}s")
        print(f"   ✅ Validaciones exitosas: {successful_validations}/{total_validations}")
        print(f"   📊 Tasa de éxito: {report['success_rate']:.1f}%")
        
        if report['success_rate'] >= 75:
            print(f"\n🎉 ¡VALIDACIÓN EXITOSA!")
            print(f"   Las optimizaciones están funcionando correctamente.")
        elif report['success_rate'] >= 50:
            print(f"\n⚠️ VALIDACIÓN PARCIAL")
            print(f"   Algunas optimizaciones necesitan revisión.")
        else:
            print(f"\n❌ VALIDACIÓN FALLIDA")
            print(f"   Las optimizaciones necesitan corrección.")
        
        return report

def main():
    """Función principal para validar optimizaciones."""
    
    print("🧪 VALIDADOR DE OPTIMIZACIONES - STEEL REBAR PREDICTOR")
    print("=" * 70)
    print("Verificando que todas las optimizaciones funcionen correctamente")
    print("=" * 70)
    
    validator = OptimizationValidator()
    
    # Ejecutar validaciones
    validator.validate_training_profiles()
    validator.validate_cost_optimization()
    validator.validate_performance_benchmark()
    validator.validate_model_configuration()
    
    # Generar reporte
    report = validator.generate_validation_report()
    
    print(f"\n✅ VALIDACIÓN COMPLETADA")
    print(f"   📊 {report['successful_validations']}/{report['total_validations']} validaciones exitosas")
    print(f"   📋 Reporte generado con detalles completos")

if __name__ == "__main__":
    main()
