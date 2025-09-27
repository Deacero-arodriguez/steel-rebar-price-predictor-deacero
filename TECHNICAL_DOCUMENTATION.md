# Documentación Técnica - Steel Rebar Price Predictor

## 📋 Resumen Ejecutivo

Esta documentación describe la implementación técnica del API de predicción de precios de varilla corrugada desarrollado para DeAcero. La solución está diseñada para cumplir con todos los requerimientos especificados mientras mantiene costos operativos bajo $5 USD/mes.

## 🏗️ Arquitectura del Sistema

### Diagrama de Arquitectura
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Cliente       │    │   API Gateway   │    │   Cloud Run     │
│   (HTTP)        │────│   (GCP)         │────│   (FastAPI)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                       ┌─────────────────┐              │
                       │   Redis Cache   │──────────────┤
                       │   (Memorystore) │              │
                       └─────────────────┘              │
                                                        │
┌─────────────────┐    ┌─────────────────┐              │
│   Yahoo Finance │    │   Alpha Vantage │──────────────┤
│   (Datos)       │    │   (Datos)       │              │
└─────────────────┘    └─────────────────┘              │
                                                        │
┌─────────────────┐    ┌─────────────────┐              │
│   FRED API      │    │   ML Model      │──────────────┘
│   (Económicos)  │    │   (Scikit-learn)│
└─────────────────┘    └─────────────────┘
```

### Componentes Principales

#### 1. **API REST (FastAPI)**
- **Framework**: FastAPI con Python 3.11
- **Endpoints**: 6 endpoints principales
- **Autenticación**: API Key con rate limiting
- **Documentación**: OpenAPI/Swagger automática

#### 2. **Modelo de Machine Learning**
- **Algoritmo**: Random Forest Regressor
- **Features**: 15+ variables técnicas y económicas
- **Validación**: Cross-validation con 5 folds
- **Confianza**: Score basado en MAPE

#### 3. **Sistema de Cache**
- **Primario**: Redis (Cloud Memorystore)
- **Fallback**: Cache en memoria
- **TTL**: 1 hora para predicciones
- **Rate Limiting**: 100 requests/hora por API key

#### 4. **Fuentes de Datos**
- **Yahoo Finance**: Precios de empresas siderúrgicas
- **Alpha Vantage**: Datos de commodities (opcional)
- **FRED**: Indicadores económicos (opcional)
- **Trading Economics**: Datos complementarios

## 🔧 Implementación Técnica

### Estructura del Proyecto
```
steel-rebar-predictor/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Aplicación FastAPI principal
│   ├── config.py              # Configuración y settings
│   ├── models/
│   │   ├── __init__.py
│   │   ├── schemas.py         # Modelos Pydantic
│   │   └── ml_model.py        # Modelo de ML
│   ├── services/
│   │   ├── __init__.py
│   │   ├── data_collector.py  # Recopilación de datos
│   │   └── cache_service.py   # Servicio de cache
│   └── utils/
│       ├── __init__.py
│       └── data_processor.py  # Procesamiento de datos
├── tests/
│   ├── __init__.py
│   └── test_api.py           # Tests unitarios
├── requirements.txt          # Dependencias Python
├── Dockerfile               # Imagen Docker
├── cloudbuild.yaml          # Configuración GCP Cloud Build
├── deploy.sh               # Script de despliegue
├── train_model.py          # Script de entrenamiento
├── run_local.py           # Script de ejecución local
├── Makefile               # Comandos de desarrollo
├── docker-compose.yml     # Orquestación local
└── README.md              # Documentación principal
```

### Modelo de Machine Learning

#### Features del Modelo
```python
# Features principales
features = [
    'price_ma_7',           # Media móvil 7 días
    'price_ma_14',          # Media móvil 14 días
    'price_ma_30',          # Media móvil 30 días
    'price_volatility_7',   # Volatilidad 7 días
    'price_volatility_14',  # Volatilidad 14 días
    'price_change_1d',      # Cambio 1 día
    'price_change_7d',      # Cambio 7 días
    'price_change_30d',     # Cambio 30 días
    'rsi_14',              # RSI 14 períodos
    'bollinger_position',   # Posición en Bollinger Bands
    'month',               # Mes del año
    'day_of_week',         # Día de la semana
    'quarter'              # Trimestre
]

# Features económicas (si están disponibles)
economic_features = [
    'iron_ore_ma_7',       # Media móvil mineral de hierro
    'iron_ore_change_7d',  # Cambio mineral de hierro
    'coal_ma_7',           # Media móvil carbón
    'coal_change_7d',      # Cambio carbón
    'usd_mxn_ma_7',        # Media móvil USD/MXN
    'usd_mxn_change_7d'    # Cambio USD/MXN
]
```

#### Algoritmo y Parámetros
```python
RandomForestRegressor(
    n_estimators=100,      # 100 árboles
    max_depth=10,          # Profundidad máxima
    random_state=42,       # Semilla fija
    n_jobs=-1             # Paralelización
)
```

#### Validación del Modelo
- **Cross-validation**: 5 folds
- **Métrica principal**: MAPE (Mean Absolute Percentage Error)
- **Métricas secundarias**: MAE, RMSE, R²
- **Confianza del modelo**: 1 - MAPE promedio

### Sistema de Cache

#### Implementación
```python
class CacheService:
    def __init__(self, redis_url):
        # Intento conectar a Redis
        try:
            self.redis_client = redis.from_url(redis_url)
            self.redis_client.ping()
        except:
            # Fallback a memoria
            self.redis_client = None
            self.memory_cache = {}
    
    def set_prediction(self, data, ttl=3600):
        # Cache con TTL de 1 hora
        cache_key = "steel_rebar:prediction:latest"
        self.redis_client.setex(cache_key, ttl, json.dumps(data))
```

#### Estrategia de Cache
- **Predicciones**: TTL 1 hora
- **Datos de entrenamiento**: TTL 24 horas
- **Rate limiting**: TTL 1 hora por API key
- **Fallback**: Memoria local si Redis falla

### Rate Limiting

#### Implementación
```python
def verify_api_key(x_api_key: str = Header(None)):
    # Verificar API key
    if x_api_key != settings.api_key:
        raise HTTPException(401, "Invalid API key")
    
    # Verificar rate limit
    if not cache_service.increment_rate_limit(x_api_key, limit=100):
        raise HTTPException(429, "Rate limit exceeded")
    
    return x_api_key
```

#### Configuración
- **Límite**: 100 requests por hora por API key
- **Ventana**: 1 hora (3600 segundos)
- **Almacenamiento**: Redis con fallback a memoria
- **Headers**: No se exponen headers de rate limit

## 📊 Fuentes de Datos

### Yahoo Finance (Primaria)
```python
# Símbolos utilizados como proxy para precios de varilla
steel_symbols = [
    'CLF',  # Cleveland-Cliffs (mineral de hierro)
    'NUE',  # Nucor Corporation (acero)
    'STLD', # Steel Dynamics (acero)
    'X',    # United States Steel (acero)
]

# Procesamiento
for symbol in steel_symbols:
    data = yf.Ticker(symbol).history(period="2y")
    # Combinar y promediar precios
    # Escalar para aproximar precios de varilla
```

### Alpha Vantage (Secundaria)
```python
# API gratuita con límite de 5 requests/minuto
def get_alpha_vantage_data(symbol, api_key):
    url = "https://www.alphavantage.co/query"
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'apikey': api_key,
        'outputsize': 'full'
    }
    # Procesar respuesta JSON
```

### FRED (Indicadores Económicos)
```python
# Datos de la Reserva Federal
def get_fred_data(series_id, api_key):
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        'series_id': series_id,
        'api_key': api_key,
        'file_type': 'json',
        'limit': 1000
    }
    # Procesar series temporales
```

### Estrategia de Datos
1. **Recopilación diaria**: Cloud Scheduler ejecuta Cloud Functions
2. **Validación**: Verificar calidad y completitud de datos
3. **Limpieza**: Remover outliers, forward fill missing values
4. **Transformación**: Calcular features técnicas y económicas
5. **Almacenamiento**: Cache en Redis, persistencia en BigQuery

## 🚀 Deployment y Escalabilidad

### Google Cloud Platform

#### Servicios Utilizados
```yaml
# cloudbuild.yaml
services:
  - cloudbuild.googleapis.com    # CI/CD
  - run.googleapis.com           # API hosting
  - containerregistry.googleapis.com # Image storage
  - memorystore.googleapis.com   # Redis (opcional)
  - bigquery.googleapis.com      # Data warehouse (opcional)
```

#### Configuración de Cloud Run
```yaml
# cloudbuild.yaml
deploy:
  memory: 1Gi
  cpu: 1
  max_instances: 10
  min_instances: 0
  concurrency: 100
  timeout: 300s
```

#### Optimización de Costos
- **Escala a cero**: Sin requests = sin costos
- **Memoria mínima**: 1GB suficiente para el modelo
- **CPU básico**: 1 vCPU para operaciones ML
- **Sin servicios premium**: Solo tier gratuito

### Docker y Containerización

#### Dockerfile Optimizado
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ ./app/
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Multi-stage Build (Opcional)
```dockerfile
# Build stage
FROM python:3.11-slim as builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage
FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
COPY app/ ./app/
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Monitoreo y Observabilidad

#### Health Checks
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "cache": cache_service.get_cache_stats(),
        "model_trained": last_model_update is not None
    }
```

#### Métricas Importantes
- **Tiempo de respuesta**: < 2 segundos
- **Disponibilidad**: 99.9% uptime
- **Precisión del modelo**: MAPE < 10%
- **Uso de cache**: Hit rate > 80%

#### Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
```

## 🧪 Testing y Calidad

### Tests Unitarios
```python
# test_api.py
def test_predict_endpoint_success():
    response = client.get(
        "/predict/steel-rebar-price",
        headers={"X-API-Key": settings.api_key}
    )
    assert response.status_code == 200
    assert "predicted_price_usd_per_ton" in response.json()
```

### Tests de Integración
```python
def test_full_prediction_flow():
    # Mock data collection
    # Train model
    # Make prediction
    # Verify response format
    # Check cache
```

### Tests de Performance
```python
def test_response_time():
    start_time = time.time()
    response = client.get("/predict/steel-rebar-price", headers=headers)
    response_time = time.time() - start_time
    assert response_time < 2.0  # Menos de 2 segundos
```

### Cobertura de Tests
- **Objetivo**: > 80% cobertura de código
- **Herramienta**: pytest-cov
- **Comando**: `pytest --cov=app tests/`

## 🔒 Seguridad

### Autenticación
- **API Key**: Única por cliente
- **Header requerido**: `X-API-Key`
- **Validación**: Verificación en cada request

### Rate Limiting
- **Límite**: 100 requests/hora
- **Almacenamiento**: Redis con TTL
- **Fallback**: Memoria local

### Validación de Datos
```python
class PredictionResponse(BaseModel):
    predicted_price_usd_per_ton: float = Field(..., ge=0)
    model_confidence: float = Field(..., ge=0.0, le=1.0)
```

### Manejo de Errores
```python
try:
    prediction = ml_model.predict(data)
except Exception as e:
    logger.error(f"Prediction error: {e}")
    raise HTTPException(500, "Prediction failed")
```

## 📈 Optimizaciones y Mejoras Futuras

### Optimizaciones Actuales
1. **Cache inteligente**: Evita recálculos innecesarios
2. **Modelo ligero**: Random Forest eficiente
3. **Datos mínimos**: Solo fuentes esenciales
4. **Escalado automático**: Cloud Run escala según demanda

### Mejoras Futuras
1. **Más fuentes de datos**: APIs especializadas en commodities
2. **Modelos ensemble**: Combinar múltiples algoritmos
3. **Features adicionales**: Sentiment analysis, noticias
4. **Monitoreo avanzado**: Prometheus + Grafana
5. **A/B testing**: Múltiples modelos en paralelo

### Escalabilidad
- **Horizontal**: Múltiples instancias de Cloud Run
- **Vertical**: Aumentar memoria/CPU si es necesario
- **Geográfica**: Despliegue en múltiples regiones
- **Cache distribuido**: Redis Cluster para alta disponibilidad

## 🎯 Métricas de Evaluación

### Criterios de Éxito
1. **MAPE < 10%**: Precisión del modelo
2. **Response time < 2s**: Tiempo de respuesta
3. **Uptime > 99%**: Disponibilidad del servicio
4. **Cost < $5/month**: Presupuesto operativo

### Métricas de Monitoreo
```python
metrics = {
    "prediction_accuracy": "MAPE del modelo",
    "response_time": "Tiempo promedio de respuesta",
    "cache_hit_rate": "Porcentaje de hits en cache",
    "api_usage": "Requests por hora/día",
    "error_rate": "Porcentaje de errores",
    "model_confidence": "Confianza promedio del modelo"
}
```

## 📚 Referencias y Recursos

### Documentación Técnica
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Google Cloud Run](https://cloud.google.com/run)
- [Redis Documentation](https://redis.io/documentation)

### APIs Utilizadas
- [Yahoo Finance](https://pypi.org/project/yfinance/)
- [Alpha Vantage](https://www.alphavantage.co/documentation/)
- [FRED API](https://fred.stlouisfed.org/docs/api/)

### Mejores Prácticas
- [Python Best Practices](https://docs.python-guide.org/)
- [Docker Best Practices](https://docs.docker.com/develop/best-practices/)
- [Google Cloud Best Practices](https://cloud.google.com/docs/best-practices)

---

**Documento generado**: Enero 2025  
**Versión**: 1.0  
**Autor**: Sistema de Documentación Automática
