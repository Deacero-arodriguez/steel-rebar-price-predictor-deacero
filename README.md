# Steel Rebar Price Predictor API

Un API REST para predecir precios de varilla corrugada utilizando machine learning, desarrollado como parte del proceso de selección para el puesto de Gerente de Data y Analítica Senior en DeAcero.

## 🎯 Objetivo

Desarrollar y desplegar un API REST que prediga el precio de cierre del día siguiente para la varilla corrugada, utilizando datos históricos disponibles públicamente.

## 🚀 Características

- **Predicción en tiempo real** del precio de varilla corrugada
- **Autenticación por API Key** con rate limiting
- **Cache inteligente** para optimizar rendimiento
- **Múltiples fuentes de datos** (Yahoo Finance, Alpha Vantage, FRED)
- **Modelo de ML robusto** con Random Forest
- **Despliegue en GCP** optimizado para costos
- **Documentación completa** con OpenAPI/Swagger

## 📊 Endpoints

### Endpoint Principal
```
GET /predict/steel-rebar-price
```

**Headers requeridos:**
```
X-API-Key: deacero_steel_predictor_2025_key
```

**Respuesta:**
```json
{
  "prediction_date": "2025-01-15",
  "predicted_price_usd_per_ton": 750.45,
  "currency": "USD",
  "unit": "metric ton",
  "model_confidence": 0.85,
  "timestamp": "2025-01-14T00:00:00Z"
}
```

### Otros Endpoints

- `GET /` - Información del servicio
- `GET /health` - Health check
- `GET /stats` - Estadísticas del API (requiere API key)
- `GET /explain/{date}` - Explicación de factores de predicción (requiere API key)
- `GET /docs` - Documentación interactiva (Swagger UI)

## 🏗️ Arquitectura

### Stack Tecnológico
- **Backend**: FastAPI (Python 3.11)
- **ML**: Scikit-learn, Random Forest
- **Cache**: Redis (con fallback a memoria)
- **Datos**: Yahoo Finance, Alpha Vantage, FRED
- **Deployment**: Google Cloud Run
- **Container**: Docker

### Fuentes de Datos
1. **Yahoo Finance** - Precios de acciones de empresas siderúrgicas
2. **Alpha Vantage** - Datos de commodities (si está disponible)
3. **FRED** - Indicadores económicos de la Reserva Federal
4. **Trading Economics** - Datos complementarios

### Features del Modelo
- **Precios históricos** con medias móviles (7, 14, 30 días)
- **Indicadores técnicos** (RSI, Bollinger Bands, MACD)
- **Factores económicos** (precio del mineral de hierro, carbón, tipo de cambio)
- **Características estacionales** (mes, día de la semana, trimestre)
- **Volatilidad** y tendencias de precios

## 🛠️ Instalación y Uso Local

### Prerrequisitos
- Python 3.11+
- pip
- Redis (opcional, tiene fallback a memoria)

### Instalación
```bash
# Clonar el repositorio
git clone <repository-url>
cd steel-rebar-predictor

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus claves de API

# Ejecutar la aplicación
uvicorn app.main:app --reload
```

### Uso
```bash
# Health check
curl http://localhost:8000/health

# Predicción (requiere API key)
curl -H "X-API-Key: deacero_steel_predictor_2025_key" \
     http://localhost:8000/predict/steel-rebar-price

# Documentación interactiva
# Abrir http://localhost:8000/docs en el navegador
```

## ☁️ Despliegue en GCP

### Opción 1: Script Automático
```bash
# Hacer ejecutable el script
chmod +x deploy.sh

# Ejecutar despliegue
./deploy.sh
```

### Opción 2: Manual
```bash
# Configurar proyecto
gcloud config set project YOUR_PROJECT_ID

# Habilitar APIs necesarias
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Desplegar usando Cloud Build
gcloud builds submit --config cloudbuild.yaml .
```

### Configuración de Costos
El despliegue está optimizado para mantenerse bajo $5 USD/mes:
- **Cloud Run**: Pago por uso, escala a 0
- **Container Registry**: Almacenamiento mínimo
- **Sin servicios premium**: Solo APIs gratuitas

## 🧪 Testing

```bash
# Ejecutar tests
pytest tests/

# Tests con cobertura
pytest --cov=app tests/

# Tests específicos
pytest tests/test_api.py::test_predict_endpoint_success
```

## 📈 Monitoreo y Métricas

### Métricas Disponibles
- **Tiempo de respuesta** del endpoint principal
- **Precisión del modelo** (MAPE)
- **Disponibilidad del servicio**
- **Uso de cache**
- **Rate limiting**

### Logs
Los logs están disponibles en:
- **Cloud Logging** (GCP)
- **Stdout** (desarrollo local)

## 🔧 Configuración

### Variables de Entorno
```bash
# API Configuration
API_KEY=deacero_steel_predictor_2025_key
REDIS_URL=redis://localhost:6379

# External APIs (opcionales)
ALPHA_VANTAGE_API_KEY=your_key_here
FRED_API_KEY=your_key_here

# Model Configuration
MODEL_UPDATE_FREQUENCY=24  # hours
CACHE_TTL=3600  # seconds
RATE_LIMIT=100  # requests per hour
```

### Rate Limiting
- **Límite**: 100 requests por hora por API key
- **Implementación**: Redis con fallback a memoria
- **Headers**: `X-RateLimit-Limit`, `X-RateLimit-Remaining`

## 📊 Evaluación del Modelo

### Métricas de Evaluación
- **MAPE** (Mean Absolute Percentage Error) - Métrica principal
- **MAE** (Mean Absolute Error)
- **RMSE** (Root Mean Square Error)
- **R²** (Coefficient of Determination)

### Validación
- **Cross-validation** con 5 folds
- **Datos de prueba** separados del entrenamiento
- **Validación temporal** respetando la cronología

## 🚨 Limitaciones y Consideraciones

### Limitaciones Técnicas
- **Presupuesto**: < $5 USD/mes en GCP
- **Datos públicos**: Solo fuentes gratuitas
- **Tiempo de respuesta**: < 2 segundos
- **Sin APIs comerciales**: No servicios de pago

### Limitaciones del Modelo
- **Datos proxy**: Usamos precios de acciones como proxy para precios de varilla
- **Correlación aproximada**: Los factores de escala son estimaciones
- **Volatilidad**: Los precios reales pueden tener mayor volatilidad

### Manejo de Errores
- **Datos faltantes**: Forward fill y backward fill
- **Outliers**: Detección y reemplazo con IQR
- **Fallbacks**: Cache en memoria si Redis falla
- **Timeouts**: Manejo de timeouts en APIs externas

## 🤝 Contribución

1. Fork el repositorio
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📝 Licencia

Este proyecto es parte del proceso de selección para DeAcero y está sujeto a los términos y condiciones del mismo.

## 📞 Contacto

Para consultas técnicas específicas, enviar email a: [ktouma@deacero.com]

---

**Desarrollado por**: Armando Rodriguez Rocha
**Fecha**: Septiembre 2025  
**Versión**: 1.0.0
