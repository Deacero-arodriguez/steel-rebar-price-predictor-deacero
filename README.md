# Steel Rebar Price Predictor API - Dynamic Confidence Edition

Un API REST de vanguardia para predecir precios de varilla corrugada utilizando machine learning comprehensivo con **sistema de confianza dinámica**.

## 📁 Estructura del Proyecto

```
steel-rebar-predictor/
├── src/                          # Código fuente principal
│   └── app/                      # Aplicación FastAPI
│       ├── models/               # Modelos de datos y ML
│       ├── services/             # Servicios de negocio
│       └── utils/                # Utilidades
├── scripts/                      # Scripts organizados por propósito
│   ├── data_collection/          # Recolección de datos
│   ├── model_training/           # Entrenamiento de modelos
│   ├── predictions/              # Scripts de predicción
│   └── utilities/                # Utilidades generales
├── docs/                         # Documentación
│   ├── api/                      # Documentación de API
│   ├── technical/                # Documentación técnica
│   ├── predictions/              # Análisis de predicciones
│   └── deployment/               # Guías de despliegue
├── data/                         # Datos organizados
│   ├── raw/                      # Datos sin procesar
│   ├── processed/                # Datos procesados
│   ├── models/                   # Modelos entrenados
│   └── predictions/              # Resultados de predicciones
├── tests/                        # Tests organizados
│   ├── unit/                     # Tests unitarios
│   ├── integration/              # Tests de integración
│   └── fixtures/                 # Datos de prueba
├── config/                       # Configuración
├── deployment/                   # Archivos de despliegue
│   ├── docker/                   # Configuración Docker
│   └── cloud/                    # Configuración cloud
├── notebooks/                    # Jupyter notebooks
├── assets/                       # Recursos estáticos
└── README.md                     # Este archivo
```

## 🚀 Inicio Rápido

### Desarrollo Local
```bash
# Instalar dependencias
pip install -r config/requirements.txt

# Ejecutar aplicación
python scripts/utilities/run_local.py

# Ejecutar demo (sin servidor)
python scripts/utilities/demo.py

# Ejecutar tests
pytest tests/

# Probar predicción con confianza dinámica
python scripts/predictions/predict_october_2025_with_dynamic_confidence.py
```

### Despliegue
```bash
# Docker (desde la raíz del proyecto)
docker build -f deployment/docker/Dockerfile -t steel-rebar-predictor .
docker run -p 8000:8000 steel-rebar-predictor

# Docker Compose
docker-compose -f deployment/docker/docker-compose.yml up

# Google Cloud (CI/CD automático)
bash deployment/cloud/deploy.sh

# GitHub Actions (automático en push a main)
# El workflow está en .github/workflows/ci-cd.yml
```

## 📊 Predicciones Disponibles

- **Octubre 2025**: Ver `docs/predictions/`
- **Análisis de confianza dinámica**: Ver `scripts/predictions/`
- **Documentación técnica**: Ver `docs/technical/`

## ⚡ Optimizaciones Implementadas

### **Perfiles de Entrenamiento Optimizados**
```bash
# Entrenamiento ultra rápido (desarrollo)
python scripts/model_training/optimized_training.py --profile ultra_fast

# Entrenamiento balanceado (producción recomendado)
python scripts/model_training/optimized_training.py --profile balanced

# Entrenamiento de alta precisión (análisis especializado)
python scripts/model_training/optimized_training.py --profile high_precision
```

### **Optimizaciones de Costos GCP**
```bash
# Aplicar optimizaciones de Cloud Run
python scripts/utilities/apply_cloud_run_optimizations.py

# Analizar costos y generar reportes
python scripts/utilities/cost_optimization_analyzer.py

# Benchmark de rendimiento
python scripts/utilities/performance_benchmark.py
```

### **Resultados de Optimización**
- **Tiempo de entrenamiento**: Reducido de 5-8 min a 3-4 min (perfil balanced)
- **Costo mensual**: Reducido de $19.18 a ~$4.82 USD/mes
- **Cumplimiento presupuesto**: ✅ SÍ ($4.82 < $5.00)
- **Precisión del modelo**: Mantenida en 90%+

## 🎯 Características Principales

- **Confianza dinámica**: 90.1% vs 85% estático
- **13 fuentes de datos** integradas
- **136 features** en el modelo
- **Intervalos de predicción** reales
- **Análisis USD/MXN** para DeAcero
- **Perfiles de entrenamiento optimizados**: 1-8 min según necesidades
- **Costos optimizados**: < $5 USD/mes (cumple presupuesto)
- **Monitoreo automático** de rendimiento y costos

---

**Desarrollado por**: Armando Rodriguez Rocha  
**Contacto**: [rr.armando@gmail.com]  
**Versión**: 2.2.0 - Optimized Performance Edition
