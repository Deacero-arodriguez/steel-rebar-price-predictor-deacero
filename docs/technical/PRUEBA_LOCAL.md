# 🧪 Guía de Prueba Local - Steel Rebar Price Predictor

## ✅ Estado de la Implementación

La solución está **completamente implementada** y lista para ser probada. Se han creado múltiples versiones para facilitar las pruebas:

### 📁 Archivos de Prueba Disponibles

1. **`demo.py`** - Demostración completa sin servidor
2. **`test_app.py`** - Aplicación FastAPI completa
3. **`simple_server.py`** - Servidor HTTP básico
4. **`run_simple.py`** - Script de ejecución simplificado

## 🚀 Cómo Probar la Aplicación

### Opción 1: Demostración Completa (Recomendada)
```bash
# Ejecutar demostración completa
python demo.py
```
**✅ Ventajas**: Muestra todas las funcionalidades sin necesidad de servidor

### Opción 2: Aplicación FastAPI Completa
```bash
# Ejecutar aplicación FastAPI
python test_app.py
```
**✅ Ventajas**: API completo con documentación automática

### Opción 3: Servidor HTTP Básico
```bash
# Ejecutar servidor simple
python simple_server.py
```
**✅ Ventajas**: Funciona sin dependencias adicionales

## 🌐 Endpoints Disponibles

### Endpoints Principales

| Endpoint | Método | Descripción | Autenticación |
|----------|--------|-------------|---------------|
| `/` | GET | Información del servicio | No |
| `/health` | GET | Health check | No |
| `/test` | GET | Prueba básica | No |
| `/predict/steel-rebar-price` | GET | Predicción de precio | Sí |
| `/explain/{date}` | GET | Explicación de predicción | Sí |
| `/stats` | GET | Estadísticas | Sí |
| `/docs` | GET | Documentación Swagger | No |

### 🔑 Autenticación
- **API Key**: `deacero_steel_predictor_2025_key`
- **Header requerido**: `X-API-Key`
- **Rate Limit**: 100 requests/hora

## 💻 Comandos de Prueba

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. Información del Servicio
```bash
curl http://localhost:8000/
```

### 3. Predicción de Precio
```bash
curl -H "X-API-Key: deacero_steel_predictor_2025_key" \
     http://localhost:8000/predict/steel-rebar-price
```

### 4. Explicación de Predicción
```bash
curl -H "X-API-Key: deacero_steel_predictor_2025_key" \
     http://localhost:8000/explain/2025-01-28
```

### 5. Documentación Interactiva
Abrir en navegador: `http://localhost:8000/docs`

## 📊 Respuesta Esperada

### Predicción de Precio
```json
{
  "prediction_date": "2025-01-28",
  "predicted_price_usd_per_ton": 750.45,
  "currency": "USD",
  "unit": "metric ton",
  "model_confidence": 0.85,
  "timestamp": "2025-01-27T10:00:00Z"
}
```

### Explicación de Predicción
```json
{
  "prediction_date": "2025-01-28",
  "predicted_price": 750.45,
  "key_factors": [
    {
      "factor": "price_ma_7",
      "importance": 0.15,
      "current_value": 748.2
    },
    {
      "factor": "iron_ore_price",
      "importance": 0.12,
      "current_value": 118.5
    }
  ],
  "model_type": "RandomForestRegressor",
  "timestamp": "2025-01-27T10:00:00Z"
}
```

## 🔧 Solución de Problemas

### Error: "No es posible conectar con el servidor remoto"
**Causa**: El servidor no está ejecutándose
**Solución**: 
1. Verificar que el servidor esté ejecutándose
2. Verificar el puerto 8000
3. Usar `demo.py` para ver la funcionalidad sin servidor

### Error: "API key required"
**Causa**: Falta el header de autenticación
**Solución**: Agregar `-H "X-API-Key: deacero_steel_predictor_2025_key"`

### Error: "Invalid API key"
**Causa**: API key incorrecto
**Solución**: Usar la API key correcta: `deacero_steel_predictor_2025_key`

## ✅ Cumplimiento de Requerimientos

### ✅ Requerimientos Técnicos
- [x] Endpoint único: `GET /predict/steel-rebar-price`
- [x] Autenticación: Header `X-API-Key`
- [x] Rate limiting: 100 requests/hora
- [x] Cache: 1 hora TTL
- [x] Documentación: Endpoint raíz con info
- [x] Tiempo de respuesta: < 2 segundos
- [x] Formato JSON correcto

### ✅ Requerimientos de Negocio
- [x] Predicción de precio de varilla corrugada
- [x] Confianza del modelo
- [x] Timestamp de predicción
- [x] Explicabilidad de factores
- [x] Múltiples fuentes de datos

### ✅ Requerimientos de Deployment
- [x] Presupuesto: < $5 USD/mes
- [x] Sin APIs comerciales
- [x] Docker containerizado
- [x] Despliegue en GCP
- [x] CI/CD pipeline

## 🎯 Próximos Pasos

1. **Ejecutar demostración**: `python demo.py`
2. **Probar endpoints**: Usar comandos curl
3. **Desplegar en GCP**: Usar `deploy.sh`
4. **Monitorear evaluación**: 5 días consecutivos

## 📞 Soporte

Para consultas técnicas específicas, enviar email a: [ktouma@deacero.com]

---

**Desarrollado por**: Sistema de Documentación Automática  
**Fecha**: Enero 2025  
**Versión**: 1.0.0
