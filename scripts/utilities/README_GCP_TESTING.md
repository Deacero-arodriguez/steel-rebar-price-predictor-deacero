# 🧪 Testing de API en GCP - Steel Rebar Predictor

Este directorio contiene scripts para realizar tests de 10 llamadas a la API desplegada en Google Cloud Platform.

## 📋 Archivos Incluidos

- `test_api_gcp.py` - Script principal de testing con 10 llamadas concurrentes
- `deploy_and_test_gcp.py` - Script completo de deployment y testing
- `run_gcp_test.py` - Script simplificado para ejecutar solo tests
- `gcp_config.py` - Configuración de GCP y parámetros
- `README_GCP_TESTING.md` - Este archivo de documentación

## 🚀 Opciones de Uso

### Opción 1: Test Rápido (API ya desplegada)

Si ya tienes la API desplegada en GCP:

```bash
# Navegar al directorio
cd Parte\ Técnica/steel-rebar-predictor/scripts/utilities/

# Ejecutar test con URL específica
python run_gcp_test.py https://steel-rebar-predictor-TU-PROJECT-ID-uc.a.run.app

# O usar variable de entorno
set GCP_API_URL=https://tu-api-url.a.run.app
python run_gcp_test.py
```

### Opción 2: Deployment Completo + Test

Para hacer deployment completo y luego testing:

```bash
# Navegar al directorio
cd Parte\ Técnica/steel-rebar-predictor/scripts/utilities/

# Ejecutar deployment y test completo
python deploy_and_test_gcp.py TU-PROJECT-ID
```

### Opción 3: Test Directo

Para ejecutar directamente el script de test:

```bash
# Navegar al directorio
cd Parte\ Técnica/steel-rebar-predictor/scripts/utilities/

# Ejecutar test directamente
python test_api_gcp.py https://tu-api-url.a.run.app
```

## ⚙️ Configuración Previa

### 1. Actualizar Project ID

Edita el archivo `gcp_config.py` y cambia:

```python
"PROJECT_ID": "tu-project-id-real",  # Cambiar por tu Project ID
```

### 2. Verificar gcloud CLI

Asegúrate de tener gcloud CLI instalado y configurado:

```bash
# Verificar instalación
gcloud --version

# Autenticarse
gcloud auth login

# Configurar proyecto
gcloud config set project TU-PROJECT-ID

# Habilitar APIs necesarias
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### 3. Instalar Dependencias

```bash
# Instalar dependencias de Python
pip install aiohttp asyncio
```

## 📊 Qué Hace el Test

El script realiza las siguientes pruebas:

### 1. Endpoints Básicos
- ✅ Health Check (`/health`)
- ✅ Service Info (`/`)

### 2. Tests de Predicción (10 llamadas)
- 📈 Endpoint: `/predict/steel-rebar-price`
- 🔑 Autenticación con API Key
- ⚡ Llamadas concurrentes
- 📊 Medición de tiempos de respuesta

### 3. Métricas Generadas
- 🎯 Tasa de éxito
- ⏱️ Tiempos de respuesta (min, max, promedio, mediana, P95)
- 💰 Estadísticas de predicciones
- 📈 Niveles de confianza
- ❌ Análisis de errores

## 📈 Resultados Esperados

### Test Exitoso (≥90% éxito)
```
🎉 TEST EXITOSO: 100.0% de éxito

📊 ESTADÍSTICAS DE TIEMPO DE RESPUESTA
   Mínimo: 245.67ms
   Máximo: 892.34ms
   Promedio: 456.78ms
   Mediana: 423.45ms
   P95: 756.23ms

💰 ESTADÍSTICAS DE PREDICCIONES
   Precio promedio: $880.12 USD/ton
   Rango: $875.45 - $884.79 USD/ton
   Confianza promedio: 0.847
```

### Archivos de Resultados

Los resultados se guardan en:
- `data/predictions/api_test_results_YYYYMMDD_HHMMSS.json`
- `data/predictions/deployment_report_YYYYMMDD_HHMMSS.json`

## 🔧 Solución de Problemas

### Error: "API key required"
```bash
# Verificar que la API Key esté configurada correctamente
# En gcp_config.py debe ser: "deacero_steel_predictor_2025_key"
```

### Error: "Connection refused"
```bash
# Verificar que la URL de la API sea correcta
# Debe ser: https://steel-rebar-predictor-TU-PROJECT-ID-uc.a.run.app
```

### Error: "gcloud not found"
```bash
# Instalar Google Cloud SDK
# Windows: https://cloud.google.com/sdk/docs/install-sdk
```

### Error: "Project not found"
```bash
# Verificar Project ID
gcloud config get-value project

# Cambiar proyecto si es necesario
gcloud config set project TU-PROJECT-ID
```

## 📝 Códigos de Salida

- `0` - Test exitoso (≥90% éxito)
- `1` - Test parcialmente exitoso (70-89% éxito)
- `2` - Test fallido (<70% éxito)
- `3` - Interrumpido por usuario
- `4` - Error inesperado

## 🎯 Próximos Pasos

Después de un test exitoso:

1. ✅ La API está funcionando correctamente
2. 📊 Revisar métricas de rendimiento
3. 🔄 Configurar monitoreo continuo
4. 📈 Analizar patrones de uso
5. 🚀 Considerar optimizaciones si es necesario

## 📞 Soporte

Si encuentras problemas:

1. 📋 Revisar logs en Cloud Run Console
2. 🔍 Verificar configuración en `gcp_config.py`
3. 🧪 Ejecutar tests individuales
4. 📊 Analizar archivos de resultados JSON

---

**Nota**: Este script está diseñado para el entorno DeAcero y sigue los estándares de la solución LegalIA. [[memory:8769320]]
