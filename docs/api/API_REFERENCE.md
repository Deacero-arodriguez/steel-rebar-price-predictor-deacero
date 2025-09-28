# 📡 **API REFERENCE - Steel Rebar Price Predictor**
## DeAcero - REST API Documentation

> **Documentación completa de la API REST para predicción de precios de varilla de acero**

---

## 🎯 **INFORMACIÓN GENERAL**

### **Base URL**
```
https://steel-rebar-predictor-646072255295.us-central1.run.app
```

### **Autenticación**
- **Tipo**: API Key
- **Header**: `X-API-Key`
- **Ejemplo**: `X-API-Key: your-api-key-here`

### **Formato de Respuesta**
- **Content-Type**: `application/json`
- **Encoding**: UTF-8

---

## 🔗 **ENDPOINTS**

### **1. 🏠 Información del Servicio**

#### **GET /**
Obtiene información general sobre el servicio.

**Request:**
```http
GET /
Host: steel-rebar-predictor-646072255295.us-central1.run.app
X-API-Key: your-api-key-here
```

**Response (200 OK):**
```json
{
  "service": "Steel Rebar Price Predictor",
  "version": "2.1.0",
  "documentation_url": "https://github.com/Deacero-arodriguez/steel-rebar-price-predictor-deacero",
  "data_sources": [
    "Alpha Vantage (Steel Stocks & Commodity ETFs)",
    "FRED API (Federal Reserve Economic Data)",
    "World Bank",
    "Yahoo Finance",
    "Simulated Steel-Specific Data"
  ],
  "last_model_update": "2025-09-29T21:41:10.655871Z",
  "model_performance": {
    "mape": 0.13,
    "r2_score": 0.9995,
    "confidence": 0.95
  }
}
```

---

### **2. 🔮 Predicción de Precios**

#### **GET /predict/steel-rebar-price**
Predice el precio de cierre de la varilla de acero para el siguiente día.

**Request:**
```http
GET /predict/steel-rebar-price
Host: steel-rebar-predictor-646072255295.us-central1.run.app
X-API-Key: your-api-key-here
```

**Response (200 OK):**
```json
{
  "prediction_date": "2025-01-29",
  "predicted_price_usd_per_ton": 750.45,
  "currency": "USD",
  "unit": "metric ton",
  "model_confidence": 0.85,
  "timestamp": "2025-01-28T23:59:59Z",
  "prediction_details": {
    "model_version": "comprehensive_v2",
    "features_used": 173,
    "data_sources": 23,
    "last_training_date": "2024-09-28T14:20:35Z"
  },
  "confidence_breakdown": {
    "prediction_interval": 0.90,
    "feature_stability": 0.85,
    "data_quality": 0.95,
    "temporal_relevance": 0.80,
    "market_volatility": 0.75
  }
}
```

**Response (401 Unauthorized):**
```json
{
  "error": "Unauthorized",
  "message": "API key is required",
  "status_code": 401
}
```

**Response (429 Too Many Requests):**
```json
{
  "error": "Rate limit exceeded",
  "message": "Maximum 100 requests per hour per API key",
  "status_code": 429,
  "retry_after": 3600
}
```

**Response (500 Internal Server Error):**
```json
{
  "error": "Internal server error",
  "message": "Unable to generate prediction at this time",
  "status_code": 500
}
```

---

## 📊 **CÓDIGOS DE ESTADO HTTP**

| Código | Descripción | Cuándo Ocurre |
|--------|-------------|---------------|
| `200` | OK | Solicitud exitosa |
| `401` | Unauthorized | API key faltante o inválida |
| `404` | Not Found | Endpoint no encontrado |
| `429` | Too Many Requests | Límite de rate excedido |
| `500` | Internal Server Error | Error interno del servidor |

---

## 🔒 **AUTENTICACIÓN Y SEGURIDAD**

### **API Keys**
- **Generación**: Contactar al administrador del sistema
- **Formato**: String alfanumérico de 32 caracteres
- **Rotación**: Mensual (recomendado)
- **Almacenamiento**: Seguro en variables de entorno

### **Rate Limiting**
- **Límite**: 100 requests por hora por API key
- **Window**: 1 hora deslizante
- **Headers de respuesta**:
  - `X-RateLimit-Limit`: Límite total (100)
  - `X-RateLimit-Remaining`: Requests restantes
  - `X-RateLimit-Reset`: Timestamp de reset

---

## ⚡ **RENDIMIENTO Y CACHE**

### **Tiempo de Respuesta**
- **Objetivo**: < 2 segundos
- **Promedio**: 1.2 segundos
- **Máximo**: 5 segundos

### **Cache**
- **TTL**: 1 hora (3600 segundos)
- **Estrategia**: Cache de predicciones
- **Invalidación**: Automática por tiempo

### **Disponibilidad**
- **SLA**: 99.5%
- **Monitoreo**: 24/7
- **Mantenimiento**: Ventanas programadas

---

## 🧪 **EJEMPLOS DE USO**

### **cURL**
```bash
# Información del servicio
curl -X GET \
  "https://steel-rebar-predictor-646072255295.us-central1.run.app/" \
  -H "X-API-Key: your-api-key-here"

# Predicción de precios
curl -X GET \
  "https://steel-rebar-predictor-646072255295.us-central1.run.app/predict/steel-rebar-price" \
  -H "X-API-Key: your-api-key-here"
```

### **Python**
```python
import requests

# Configuración
BASE_URL = "https://steel-rebar-predictor-646072255295.us-central1.run.app"
API_KEY = "your-api-key-here"
HEADERS = {"X-API-Key": API_KEY}

# Información del servicio
response = requests.get(f"{BASE_URL}/", headers=HEADERS)
service_info = response.json()
print(f"Servicio: {service_info['service']}")

# Predicción de precios
response = requests.get(f"{BASE_URL}/predict/steel-rebar-price", headers=HEADERS)
prediction = response.json()
print(f"Precio predicho: ${prediction['predicted_price_usd_per_ton']}/ton")
```

### **JavaScript**
```javascript
const BASE_URL = 'https://steel-rebar-predictor-deacero-[PROJECT-ID].a.run.app';
const API_KEY = 'your-api-key-here';

// Función para hacer requests
async function apiRequest(endpoint) {
  const response = await fetch(`${BASE_URL}${endpoint}`, {
    headers: {
      'X-API-Key': API_KEY
    }
  });
  return await response.json();
}

// Uso
apiRequest('/predict/steel-rebar-price')
  .then(prediction => {
    console.log(`Precio predicho: $${prediction.predicted_price_usd_per_ton}/ton`);
  });
```

---

## 📈 **MONITOREO Y MÉTRICAS**

### **Métricas Disponibles**
- **Latencia**: Tiempo de respuesta por endpoint
- **Throughput**: Requests por segundo
- **Error Rate**: Porcentaje de errores
- **Cache Hit Rate**: Efectividad del cache

### **Logs**
- **Nivel**: INFO, WARN, ERROR
- **Formato**: JSON estructurado
- **Retención**: 30 días
- **Acceso**: Cloud Logging (GCP)

---

## 🔧 **MANTENIMIENTO**

### **Actualizaciones del Modelo**
- **Frecuencia**: Semanal
- **Notificación**: 24 horas antes
- **Downtime**: < 5 minutos
- **Rollback**: Automático si hay errores

### **Backup y Recuperación**
- **Modelos**: Backup diario
- **Datos**: Backup cada 6 horas
- **RTO**: 15 minutos
- **RPO**: 1 hora

---

## 📞 **SOPORTE**

### **Contacto**
- **Email**: soporte-deacero@deacero.com
- **Horario**: 24/7
- **Escalación**: Nivel 1 → Nivel 2 → Nivel 3

### **Documentación Adicional**
- **Guía de Integración**: `/docs/examples/`
- **Troubleshooting**: `/docs/troubleshooting.md`
- **Changelog**: `/docs/changelog.md`

---

**Última actualización**: 29 de septiembre de 2025  
**Versión de la API**: 1.0  
**Estado**: ✅ Producción
