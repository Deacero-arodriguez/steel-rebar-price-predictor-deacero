# 🧭 Guía de Navegación del Proyecto

Esta guía te ayuda a navegar eficientemente por la nueva estructura del proyecto Steel Rebar Price Predictor.

## 📁 Estructura Principal

### 🏗️ **src/** - Código Fuente Principal
```
src/
└── app/                    # Aplicación FastAPI principal
    ├── main.py            # Punto de entrada del API
    ├── config.py          # Configuración de la aplicación
    ├── models/            # Modelos de datos y ML
    │   ├── ml_model.py    # Modelo de machine learning
    │   └── schemas.py     # Esquemas Pydantic
    ├── services/          # Servicios de negocio
    │   ├── data_collector.py  # Recolección de datos
    │   └── cache_service.py   # Servicio de caché
    └── utils/             # Utilidades
        └── data_processor.py  # Procesamiento de datos
```

### 📜 **scripts/** - Scripts Organizados por Propósito
```
scripts/
├── data_collection/       # Recolección de datos
│   ├── enhanced_data_collector.py
│   └── enhanced_data_collector_v2.py
├── model_training/        # Entrenamiento de modelos
│   ├── train_model.py
│   ├── train_model_with_new_sources.py
│   └── enhanced_ml_model.py
├── predictions/           # Scripts de predicción
│   ├── predict_october_2025.py
│   ├── predict_october_2025_detailed.py
│   ├── predict_october_2025_with_dynamic_confidence.py
│   ├── predict_october_simple.py
│   └── predict_with_currency_analysis.py
└── utilities/             # Utilidades generales
    ├── demo.py            # Demo del sistema
    ├── run_local.py       # Ejecutar localmente
    ├── simple_server.py   # Servidor simple
    ├── verify_api_format.py
    ├── api_response_example.py
    └── path_setup.py      # Configuración de rutas
```

### 📊 **data/** - Datos Organizados
```
data/
├── raw/                   # Datos sin procesar
├── processed/             # Datos procesados
│   └── enhanced_steel_data_v2.csv
├── models/                # Modelos entrenados
│   ├── comprehensive_steel_rebar_model.pkl
│   └── comprehensive_model_metadata.json
└── predictions/           # Resultados de predicciones
    ├── october_2025_prediction.json
    ├── october_2025_prediction_with_currency.json
    ├── october_2025_prediction_with_dynamic_confidence.json
    ├── october_2025_detailed_analysis.json
    └── api_compliance_report.json
```

### 📚 **docs/** - Documentación
```
docs/
├── README.md              # Documentación principal
├── NAVIGATION_GUIDE.md    # Esta guía
├── api/                   # Documentación de API
├── technical/             # Documentación técnica
│   ├── TECHNICAL_DOCUMENTATION.md
│   ├── DATA_SOURCES_SUMMARY.md
│   └── PRUEBA_LOCAL.md
├── predictions/           # Análisis de predicciones
│   ├── PREDICCION_OCTUBRE_2025_RESUMEN.md
│   └── OCTUBRE_2025_CONFIANZA_DINAMICA_RESUMEN.md
└── deployment/            # Guías de despliegue
    └── DEPLOYMENT_INSTRUCTIONS.md
```

## 🎯 Rutas Rápidas por Tarea

### 🚀 **Ejecutar la Aplicación**
```bash
# Servidor local
python scripts/utilities/run_local.py

# Demo sin servidor
python scripts/utilities/demo.py

# Servidor simple
python scripts/utilities/simple_server.py
```

### 📊 **Generar Predicciones**
```bash
# Predicción octubre 2025 con confianza dinámica
python scripts/predictions/predict_october_2025_with_dynamic_confidence.py

# Predicción detallada
python scripts/predictions/predict_october_2025_detailed.py

# Predicción simple
python scripts/predictions/predict_october_simple.py
```

### 🧪 **Ejecutar Tests**
```bash
# Tests unitarios
pytest tests/unit/

# Tests de integración
pytest tests/integration/

# Todos los tests
pytest tests/
```

### 🔧 **Entrenar Modelos**
```bash
# Modelo básico
python scripts/model_training/train_model.py

# Modelo con nuevas fuentes
python scripts/model_training/train_model_with_new_sources.py

# Modelo mejorado
python scripts/model_training/enhanced_ml_model.py
```

### 📈 **Recolectar Datos**
```bash
# Recolector básico
python scripts/data_collection/enhanced_data_collector.py

# Recolector con 13 fuentes
python scripts/data_collection/enhanced_data_collector_v2.py
```

### ✅ **Verificar Cumplimiento**
```bash
# Verificar formato del API
python scripts/utilities/verify_api_format.py

# Ejemplo de respuestas del API
python scripts/utilities/api_response_example.py
```

## 🐳 **Despliegue**

### **Docker Local**
```bash
# Construir imagen
docker build -f deployment/docker/Dockerfile -t steel-rebar-predictor .

# Ejecutar contenedor
docker run -p 8000:8000 steel-rebar-predictor

# Docker Compose
docker-compose -f deployment/docker/docker-compose.yml up
```

### **Google Cloud**
```bash
# Despliegue completo
bash deployment/cloud/deploy.sh

# Solo build
gcloud builds submit --config deployment/cloud/cloudbuild.yaml .
```

## 📋 **Archivos Clave por Funcionalidad**

### **🎯 API Principal**
- `src/app/main.py` - Endpoints del API
- `src/app/config.py` - Configuración
- `src/app/models/schemas.py` - Esquemas de respuesta

### **🤖 Machine Learning**
- `src/app/models/ml_model.py` - Modelo principal
- `scripts/model_training/` - Scripts de entrenamiento
- `data/models/` - Modelos entrenados

### **📊 Predicciones**
- `scripts/predictions/` - Todos los scripts de predicción
- `scripts/utilities/dynamic_confidence_calculator.py` - Confianza dinámica
- `data/predictions/` - Resultados de predicciones

### **🔧 Configuración**
- `config/requirements.txt` - Dependencias Python
- `config/config_local.py` - Configuración local
- `path_setup.py` - Configuración de rutas

### **🚀 Despliegue**
- `deployment/docker/Dockerfile` - Imagen Docker
- `deployment/cloud/cloudbuild.yaml` - Build de Google Cloud
- `deployment/cloud/deploy.sh` - Script de despliegue
- `.github/workflows/ci-cd.yml` - GitHub Actions

## 🔍 **Búsqueda Rápida**

### **¿Dónde está el código del API?**
→ `src/app/`

### **¿Dónde están las predicciones?**
→ `scripts/predictions/` y `data/predictions/`

### **¿Dónde está la documentación?**
→ `docs/`

### **¿Dónde están los tests?**
→ `tests/`

### **¿Dónde está la configuración?**
→ `config/`

### **¿Dónde están los datos?**
→ `data/`

### **¿Dónde está el despliegue?**
→ `deployment/`

## 💡 **Consejos de Navegación**

1. **Para desarrollo**: Empieza en `src/app/`
2. **Para predicciones**: Ve a `scripts/predictions/`
3. **Para entender el proyecto**: Lee `docs/README.md`
4. **Para desplegar**: Usa `deployment/`
5. **Para tests**: Ejecuta desde `tests/`

## 🆘 **Solución de Problemas**

### **Error de imports**
```bash
# Ejecutar configuración de rutas
python path_setup.py
```

### **Error de dependencias**
```bash
# Reinstalar dependencias
pip install -r config/requirements.txt
```

### **Error de rutas**
```bash
# Verificar estructura
python scripts/utilities/verify_api_format.py
```

---

**💡 Tip**: Usa `Ctrl+F` en tu editor para buscar rápidamente por funcionalidad específica.

**📞 Soporte**: Para consultas técnicas, contactar a [rr.armando@gmail.com]
