# Steel Rebar Price Predictor
## Sistema de Predicción de Precios de Varilla de Acero para DeAcero

API REST para predecir el precio de cierre del día siguiente de la varilla de acero utilizando Machine Learning.

---

## Resumen del Proyecto

### Objetivo
Desarrollar un sistema de predicción de precios de varilla de acero que permita a DeAcero optimizar sus estrategias de compra de materias primas y fijación de precios.

### Resultados Técnicos
- **Precisión del Modelo**: MAPE 0.25% (Test), R² 0.9820
- **Variables del Modelo**: 37 features específicas de varilla
- **Fuentes de Datos**: 4 fuentes reales integradas
- **Período de Datos**: 2020-2024 (1,827 registros diarios)
- **Costo de Operación**: $0 USD/mes (APIs gratuitas)

### API en Producción
- **URL**: https://steel-rebar-predictor-646072255295.us-central1.run.app
- **Estado**: Activo
- **Disponibilidad**: 24/7
- **Tiempo de respuesta**: < 2 segundos

---

## Documentación del Proyecto

### 📊 Documentación Ejecutiva
- **[Resumen Ejecutivo](docs/executive/EXECUTIVE_SUMMARY.md)** - Resumen para gerencia

### 📋 Documentación del Proyecto
- **[Paquete de Entrega](docs/project/DELIVERY_PACKAGE.md)** - Paquete completo para evaluación
- **[Control de Versiones](docs/project/VERSION.md)** - Historial de versiones

### 🔧 Documentación Técnica
- **[Referencia de API](docs/api/API_REFERENCE.md)** - Documentación completa de la API
- **[Documentación del Modelo](docs/model/MODEL_DOCUMENTATION.md)** - Detalles del modelo ML
- **[Guía de Despliegue](docs/deployment/DEPLOYMENT_GUIDE.md)** - Instrucciones de despliegue
- **[Ejemplos de Uso](docs/examples/USAGE_EXAMPLES.md)** - Ejemplos prácticos

---

## Uso Rápido de la API

### Autenticación
```bash
X-API-Key: deacero_steel_predictor_2025_key
```

### Endpoints
1. **Información del servicio**: `GET /`
2. **Predicción de precio**: `GET /predict/steel-rebar-price`

### Ejemplo de Uso
```bash
curl -H "X-API-Key: deacero_steel_predictor_2025_key" \
     https://steel-rebar-predictor-646072255295.us-central1.run.app/predict/steel-rebar-price
```

---

## Estructura del Proyecto

```
steel-rebar-predictor/
├── docs/                    # Documentación completa
│   ├── executive/          # Documentación ejecutiva
│   ├── project/            # Documentación del proyecto
│   ├── api/                # Documentación de la API
│   ├── model/              # Documentación del modelo
│   ├── deployment/         # Guías de despliegue
│   └── examples/           # Ejemplos de uso
├── src/                    # Código fuente
├── scripts/                # Scripts de entrenamiento
├── config/                 # Configuración
├── data/                   # Datos y modelos
├── deployment/             # Archivos de despliegue
└── assets/                 # Recursos del proyecto
```

---

## Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- pip
- Git

### Instalación
```bash
# Clonar repositorio
git clone https://github.com/Deacero-arodriguez/steel-rebar-price-predictor-deacero.git
cd steel-rebar-price-predictor-deacero

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar API localmente
python main.py
```

---

## Especificaciones Técnicas

### Modelo de Machine Learning
- **Algoritmo**: Random Forest Regressor
- **Árboles**: 100
- **Features**: 37 variables específicas de acero
- **Validación**: Cross-validation temporal 5-fold

### Infraestructura
- **Plataforma**: Google Cloud Run
- **Framework**: FastAPI (Python)
- **Cache**: Redis (1 hora TTL)
- **Monitoreo**: Cloud Logging & Monitoring

### Fuentes de Datos
- **Alpha Vantage**: Acciones de acero, ETFs de commodities
- **FRED API**: Datos económicos oficiales
- **World Bank**: Indicadores económicos globales
- **Yahoo Finance**: Datos de mercado en tiempo real

---

## Cumplimiento de Especificaciones

### Requerimientos Técnicos
- ✅ **API REST**: Implementada con FastAPI
- ✅ **Endpoint único**: `/predict/steel-rebar-price`
- ✅ **Autenticación**: X-API-Key header
- ✅ **Rate Limiting**: 100 requests/hora
- ✅ **Cache**: 1 hora TTL máximo
- ✅ **Tiempo de respuesta**: < 2 segundos
- ✅ **Presupuesto**: < $5 USD/mes

### Requerimientos Funcionales
- ✅ **Predicción de precio**: Precio del día siguiente
- ✅ **Formato JSON**: Respuesta estructurada
- ✅ **Confianza del modelo**: Incluida en respuesta
- ✅ **Datos reales**: Integrados de fuentes confiables
- ✅ **Documentación**: Completa y técnica

---

## Información del Proyecto

- **Desarrollador**: Equipo DeAcero Data & Analytics
- **Empresa**: DeAcero S.A. de C.V.
- **Versión**: 2.1.0
- **Fecha**: 28 de septiembre de 2024
- **Estado**: Completado y en Producción

---

**Para más información, consulta la documentación completa en el directorio `docs/`**