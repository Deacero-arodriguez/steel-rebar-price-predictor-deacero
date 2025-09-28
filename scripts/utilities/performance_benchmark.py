#!/usr/bin/env python3
"""
Script de benchmarks de rendimiento para el Steel Rebar Predictor.
Mide tiempos de entrenamiento, predicción y uso de recursos.
"""

import time
import psutil
import pandas as pd
import numpy as np
from datetime import datetime
import json
import subprocess
import sys
import os

class PerformanceBenchmark:
    """Benchmark de rendimiento del sistema."""
    
    def __init__(self):
        self.results = {}
        self.system_info = self.get_system_info()
    
    def get_system_info(self):
        """Obtener información del sistema."""
        
        return {
            'cpu_count': psutil.cpu_count(),
            'memory_total': psutil.virtual_memory().total / (1024**3),  # GB
            'python_version': sys.version,
            'platform': sys.platform,
            'timestamp': datetime.now().isoformat()
        }
    
    def benchmark_training_times(self):
        """Benchmark de tiempos de entrenamiento."""
        
        print("🏁 BENCHMARK DE TIEMPOS DE ENTRENAMIENTO")
        print("=" * 60)
        
        # Importar el entrenador optimizado
        sys.path.append(os.path.join(os.path.dirname(__file__)))
        from optimized_training import OptimizedSteelRebarTrainer
        
        trainer = OptimizedSteelRebarTrainer()
        
        # Crear datos de prueba
        data = trainer.create_optimized_training_data()
        enhanced_data = trainer.create_essential_features(data)
        
        training_results = {}
        
        for profile_name in trainer.training_profiles.keys():
            print(f"\n📊 Probando perfil: {profile_name}")
            
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss / (1024**2)  # MB
            
            try:
                result = trainer.train_with_profile(enhanced_data, profile_name)
                
                end_time = time.time()
                end_memory = psutil.Process().memory_info().rss / (1024**2)  # MB
                
                training_results[profile_name] = {
                    'total_time': result['total_time'],
                    'training_time': result['training_time'],
                    'eval_time': result['eval_time'],
                    'confidence': result['model_confidence'],
                    'memory_usage': end_memory - start_memory,
                    'peak_memory': end_memory,
                    'cv_mape': abs(np.mean(result['cv_scores'])),
                    'oob_score': result['model'].oob_score_,
                    'n_estimators': result['model'].n_estimators,
                    'max_depth': result['model'].max_depth
                }
                
                print(f"   ✅ Completado en {result['total_time']:.2f}s")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                training_results[profile_name] = None
        
        self.results['training'] = training_results
        return training_results
    
    def benchmark_prediction_times(self):
        """Benchmark de tiempos de predicción."""
        
        print("\n🎯 BENCHMARK DE TIEMPOS DE PREDICCIÓN")
        print("=" * 60)
        
        # Simular datos de entrada para predicción
        sample_data = np.random.rand(1, 20)  # 20 features
        
        prediction_results = {}
        
        # Probar diferentes tamaños de datos
        data_sizes = [1, 10, 100, 1000]
        
        for size in data_sizes:
            print(f"\n📊 Probando con {size} predicciones simultáneas")
            
            # Crear datos de prueba
            test_data = np.random.rand(size, 20)
            
            # Simular modelo entrenado (Random Forest simple)
            from sklearn.ensemble import RandomForestRegressor
            from sklearn.preprocessing import StandardScaler
            
            # Crear modelo de prueba
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            scaler = StandardScaler()
            
            # Datos de entrenamiento simulados
            X_train = np.random.rand(1000, 20)
            y_train = np.random.rand(1000) * 1000 + 500  # Precios simulados
            
            scaler.fit(X_train)
            X_train_scaled = scaler.transform(X_train)
            model.fit(X_train_scaled, y_train)
            
            # Benchmark de predicción
            times = []
            for _ in range(5):  # 5 iteraciones para promedio
                start_time = time.time()
                
                X_test_scaled = scaler.transform(test_data)
                predictions = model.predict(X_test_scaled)
                
                end_time = time.time()
                times.append(end_time - start_time)
            
            avg_time = np.mean(times)
            std_time = np.std(times)
            
            prediction_results[size] = {
                'avg_time': avg_time,
                'std_time': std_time,
                'predictions_per_second': size / avg_time,
                'time_per_prediction': avg_time / size
            }
            
            print(f"   ✅ {size} predicciones en {avg_time:.4f}s ± {std_time:.4f}s")
            print(f"   📈 {size/avg_time:.1f} predicciones/segundo")
        
        self.results['prediction'] = prediction_results
        return prediction_results
    
    def benchmark_api_performance(self, api_url=None):
        """Benchmark de rendimiento de la API."""
        
        print("\n🌐 BENCHMARK DE RENDIMIENTO DE API")
        print("=" * 60)
        
        if not api_url:
            print("⚠️ No se proporcionó URL de API, saltando benchmark de API")
            return None
        
        import requests
        
        api_results = {
            'endpoints': {},
            'concurrent_requests': {},
            'error_rate': 0
        }
        
        # Headers con API key
        headers = {
            'X-API-Key': 'deacero_steel_predictor_2025_key'
        }
        
        # Benchmark de endpoints individuales
        endpoints = [
            ('/', 'Service Info'),
            ('/health', 'Health Check'),
            ('/predict/steel-rebar-price', 'Prediction')
        ]
        
        for endpoint, name in endpoints:
            print(f"\n📊 Probando endpoint: {name}")
            
            times = []
            errors = 0
            
            for _ in range(10):  # 10 requests por endpoint
                try:
                    start_time = time.time()
                    
                    response = requests.get(
                        f"{api_url}{endpoint}",
                        headers=headers,
                        timeout=10
                    )
                    
                    end_time = time.time()
                    
                    if response.status_code == 200:
                        times.append(end_time - start_time)
                    else:
                        errors += 1
                        
                except Exception as e:
                    errors += 1
                    print(f"   ❌ Error: {e}")
            
            if times:
                api_results['endpoints'][endpoint] = {
                    'avg_time': np.mean(times),
                    'std_time': np.std(times),
                    'min_time': np.min(times),
                    'max_time': np.max(times),
                    'error_rate': errors / 10
                }
                
                print(f"   ✅ {name}: {np.mean(times):.3f}s ± {np.std(times):.3f}s")
                print(f"   📊 Error rate: {errors/10:.1%}")
        
        # Benchmark de requests concurrentes
        print(f"\n📊 Probando requests concurrentes...")
        
        import concurrent.futures
        import threading
        
        def make_request():
            try:
                start_time = time.time()
                response = requests.get(
                    f"{api_url}/predict/steel-rebar-price",
                    headers=headers,
                    timeout=10
                )
                end_time = time.time()
                return end_time - start_time, response.status_code == 200
            except:
                return None, False
        
        # Probar diferentes niveles de concurrencia
        concurrency_levels = [1, 5, 10, 20]
        
        for level in concurrency_levels:
            print(f"\n   🔄 Probando {level} requests concurrentes...")
            
            times = []
            successes = 0
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=level) as executor:
                futures = [executor.submit(make_request) for _ in range(level)]
                
                for future in concurrent.futures.as_completed(futures):
                    time_taken, success = future.result()
                    if time_taken is not None:
                        times.append(time_taken)
                        if success:
                            successes += 1
            
            if times:
                api_results['concurrent_requests'][level] = {
                    'avg_time': np.mean(times),
                    'std_time': np.std(times),
                    'success_rate': successes / level,
                    'throughput': level / np.mean(times)
                }
                
                print(f"   ✅ {level} concurrentes: {np.mean(times):.3f}s promedio")
                print(f"   📈 Throughput: {level/np.mean(times):.1f} req/s")
                print(f"   ✅ Success rate: {successes/level:.1%}")
        
        self.results['api'] = api_results
        return api_results
    
    def benchmark_memory_usage(self):
        """Benchmark de uso de memoria."""
        
        print("\n💾 BENCHMARK DE USO DE MEMORIA")
        print("=" * 60)
        
        memory_results = {}
        
        # Memoria inicial
        initial_memory = psutil.Process().memory_info().rss / (1024**2)  # MB
        
        # Probar diferentes operaciones
        operations = [
            ('Data Loading', self._test_data_loading),
            ('Feature Engineering', self._test_feature_engineering),
            ('Model Training', self._test_model_training),
            ('Prediction', self._test_prediction)
        ]
        
        for op_name, op_func in operations:
            print(f"\n📊 Probando: {op_name}")
            
            # Limpiar memoria antes de cada test
            import gc
            gc.collect()
            
            start_memory = psutil.Process().memory_info().rss / (1024**2)
            
            try:
                op_func()
                
                end_memory = psutil.Process().memory_info().rss / (1024**2)
                memory_used = end_memory - start_memory
                
                memory_results[op_name] = {
                    'memory_used': memory_used,
                    'peak_memory': end_memory,
                    'memory_efficiency': memory_used / (end_memory - initial_memory) if end_memory > initial_memory else 1.0
                }
                
                print(f"   ✅ Memoria usada: {memory_used:.1f} MB")
                print(f"   📊 Pico de memoria: {end_memory:.1f} MB")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                memory_results[op_name] = None
        
        self.results['memory'] = memory_results
        return memory_results
    
    def _test_data_loading(self):
        """Test de carga de datos."""
        # Simular carga de datos
        data = pd.DataFrame(np.random.rand(1000, 10))
        return data
    
    def _test_feature_engineering(self):
        """Test de ingeniería de features."""
        data = pd.DataFrame(np.random.rand(1000, 10))
        
        # Crear features
        for i in range(10):
            data[f'feature_{i}_ma_7'] = data.iloc[:, i].rolling(7).mean()
            data[f'feature_{i}_change'] = data.iloc[:, i].pct_change()
        
        return data
    
    def _test_model_training(self):
        """Test de entrenamiento de modelo."""
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.preprocessing import StandardScaler
        
        # Crear datos de prueba
        X = np.random.rand(1000, 20)
        y = np.random.rand(1000) * 1000 + 500
        
        # Entrenar modelo
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        model = RandomForestRegressor(n_estimators=50, random_state=42)
        model.fit(X_scaled, y)
        
        return model, scaler
    
    def _test_prediction(self):
        """Test de predicción."""
        model, scaler = self._test_model_training()
        
        # Hacer predicciones
        X_test = np.random.rand(100, 20)
        X_test_scaled = scaler.transform(X_test)
        predictions = model.predict(X_test_scaled)
        
        return predictions
    
    def generate_report(self):
        """Generar reporte completo de benchmarks."""
        
        print("\n📋 GENERANDO REPORTE DE BENCHMARKS")
        print("=" * 60)
        
        report = {
            'system_info': self.system_info,
            'benchmark_results': self.results,
            'recommendations': self._generate_recommendations(),
            'timestamp': datetime.now().isoformat()
        }
        
        # Guardar reporte
        report_filename = f'performance_benchmark_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(f'../../data/predictions/{report_filename}', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Reporte guardado: {report_filename}")
        
        # Mostrar resumen
        self._print_summary()
        
        return report
    
    def _generate_recommendations(self):
        """Generar recomendaciones basadas en los benchmarks."""
        
        recommendations = []
        
        if 'training' in self.results:
            training_results = self.results['training']
            
            # Encontrar el perfil más rápido con buena precisión
            valid_results = {k: v for k, v in training_results.items() if v is not None}
            
            if valid_results:
                fastest = min(valid_results.items(), key=lambda x: x[1]['total_time'])
                most_accurate = max(valid_results.items(), key=lambda x: x[1]['confidence'])
                
                recommendations.append({
                    'type': 'training_optimization',
                    'title': 'Optimización de Entrenamiento',
                    'description': f"Perfil más rápido: {fastest[0]} ({fastest[1]['total_time']:.2f}s)",
                    'details': f"Perfil más preciso: {most_accurate[0]} ({most_accurate[1]['confidence']:.3f} confianza)"
                })
        
        if 'api' in self.results and self.results['api']:
            api_results = self.results['api']
            
            if 'endpoints' in api_results:
                slowest_endpoint = max(
                    api_results['endpoints'].items(),
                    key=lambda x: x[1]['avg_time']
                )
                
                recommendations.append({
                    'type': 'api_optimization',
                    'title': 'Optimización de API',
                    'description': f"Endpoint más lento: {slowest_endpoint[0]} ({slowest_endpoint[1]['avg_time']:.3f}s)",
                    'details': "Considerar cache o optimización de queries"
                })
        
        return recommendations
    
    def _print_summary(self):
        """Imprimir resumen de benchmarks."""
        
        print(f"\n📊 RESUMEN DE BENCHMARKS")
        print("=" * 60)
        
        if 'training' in self.results:
            print(f"\n🏁 ENTRENAMIENTO:")
            training_results = self.results['training']
            valid_results = {k: v for k, v in training_results.items() if v is not None}
            
            if valid_results:
                fastest = min(valid_results.items(), key=lambda x: x[1]['total_time'])
                most_accurate = max(valid_results.items(), key=lambda x: x[1]['confidence'])
                
                print(f"   ⚡ Más rápido: {fastest[0]} ({fastest[1]['total_time']:.2f}s)")
                print(f"   🎯 Más preciso: {most_accurate[0]} ({most_accurate[1]['confidence']:.3f})")
        
        if 'prediction' in self.results:
            print(f"\n🎯 PREDICCIÓN:")
            prediction_results = self.results['prediction']
            
            if prediction_results:
                single_pred = prediction_results.get(1, {})
                if single_pred:
                    print(f"   ⚡ Predicción individual: {single_pred['time_per_prediction']:.4f}s")
                    print(f"   📈 Throughput: {single_pred['predictions_per_second']:.1f} pred/s")
        
        if 'memory' in self.results:
            print(f"\n💾 MEMORIA:")
            memory_results = self.results['memory']
            
            total_memory = sum(
                result['memory_used'] for result in memory_results.values() 
                if result is not None
            )
            print(f"   📊 Uso total estimado: {total_memory:.1f} MB")

def main():
    """Función principal para ejecutar benchmarks."""
    
    print("🏁 BENCHMARK DE RENDIMIENTO - STEEL REBAR PREDICTOR")
    print("=" * 70)
    print("Evaluando tiempos de entrenamiento, predicción y uso de recursos")
    print("=" * 70)
    
    benchmark = PerformanceBenchmark()
    
    # Ejecutar benchmarks
    benchmark.benchmark_training_times()
    benchmark.benchmark_prediction_times()
    benchmark.benchmark_memory_usage()
    
    # API benchmark (opcional)
    api_url = input("\n¿Proporcionar URL de API para benchmark? (opcional): ").strip()
    if api_url:
        benchmark.benchmark_api_performance(api_url)
    
    # Generar reporte
    report = benchmark.generate_report()
    
    print(f"\n✅ BENCHMARKS COMPLETADOS")
    print(f"   📊 {len(benchmark.results)} categorías evaluadas")
    print(f"   📋 Reporte generado con recomendaciones")
    print(f"   🎯 Listo para optimizaciones de producción")

if __name__ == "__main__":
    main()
