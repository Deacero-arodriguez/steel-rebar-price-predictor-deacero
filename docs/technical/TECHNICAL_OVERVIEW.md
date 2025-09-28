# 🏗️ Visión Técnica Consolidada - Steel Rebar Price Predictor
## Arquitectura, Diseño y Implementación

> **Documentación técnica completa del sistema de predicción de precios con Machine Learning y confianza dinámica**

---

## 🎯 **Arquitectura General**

### **Diagrama de Alto Nivel**
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Data Sources  │    │   ML Pipeline    │    │   API Service   │
│                 │    │                  │    │                 │
│ • Yahoo Finance │───▶│ • Data Collection│───▶│ • FastAPI       │
│ • FRED          │    │ • Feature Eng.   │    │ • Authentication│
│ • IndexMundi    │    │ • Model Training │    │ • Rate Limiting │
│ • 13 Sources    │    │ • Confidence     │    │ • Caching       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   GCP Cloud      │
                       │                  │
                       │ • Cloud Run      │
                       │ • Container      │
                       │ • Auto-scaling   │
                       │ • Monitoring     │
                       └──────────────────┘
```

---

## 🔧 **Stack Tecnológico**

### **Backend y API**
- **Framework**: FastAPI 0.104.1+
- **Runtime**: Python 3.11
- **ASGI Server**: Uvicorn 0.24.0+
- **Validation**: Pydantic 2.0+
- **Authentication**: JWT + API Key

### **Machine Learning**
- **ML Framework**: Scikit-learn 1.3.0+
- **Algorithm**: Random Forest Regressor
- **Data Processing**: Pandas 2.0.0+, NumPy 1.24.0+
- **Model Persistence**: Joblib

### **Infraestructura**
- **Cloud Platform**: Google Cloud Platform
- **Compute**: Cloud Run
- **Container**: Docker
- **Registry**: Container Registry
- **CI/CD**: GitHub Actions
- **Monitoring**: Cloud Logging

---

## 🤖 **Modelo de Machine Learning**

### **Algoritmo Principal: Random Forest Regressor**
```python
RandomForestRegressor(
    n_estimators=100,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)
```

### **Métricas de Rendimiento**
| Métrica | Valor | Benchmark |
|---------|-------|-----------|
| **MAPE** | 1.3% | < 5% |
| **RMSE** | 12.45 USD/ton | < 20 USD/ton |
| **R²** | 0.89 | > 0.8 |
| **MAE** | 9.87 USD/ton | < 15 USD/ton |

---

## 🔬 **Sistema de Confianza Dinámica**

### **Componentes de Confianza**
1. **Intervalos de Predicción** (25% peso) - Ensemble de árboles
2. **Estabilidad de Features** (20% peso) - Análisis de variabilidad
3. **Calidad de Datos** (20% peso) - Completitud y outliers
4. **Confianza Temporal** (20% peso) - Antigüedad del modelo
5. **Volatilidad del Mercado** (15% peso) - Condiciones económicas

### **Confianza Total**: 90.1% (EXCELLENT)

---

## 📊 **Fuentes de Datos (13 Integradas)**

### **Precios Directos de Acero**
- Yahoo Finance, IndexMundi, Daily Metal Price
- Barchart, Investing.com

### **Materias Primas Relacionadas**
- FocusEconomics, Trading Economics, FRED

### **Datos Regionales Mexicanos**
- S&P Global Platts, Reportacero

### **Tipos de Cambio**
- FRED (USD/MXN, USD/EUR, USD/CNY, USD/JPY)

### **Indicadores Geopolíticos**
- Geopolitical Risk Indicators

---

## 🚀 **Arquitectura de Despliegue**

### **Containerización con Docker**
```dockerfile
FROM python:3.11-slim
COPY config/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
EXPOSE 8080
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### **Google Cloud Run Configuration**
- **CPU**: 0.5 vCPU
- **Memoria**: 512MiB
- **Max Instances**: 3
- **Min Instances**: 0
- **Concurrencia**: 1
- **Timeout**: 30s

---

## 🔄 **Pipeline CI/CD**

### **GitHub Actions Workflow**
- **Test**: Tests unitarios y validación
- **Security Scan**: Análisis de vulnerabilidades
- **Code Quality**: Linting y formateo
- **Build**: Construcción de imagen Docker
- **Deploy**: Despliegue a Cloud Run
- **Health Check**: Validación de funcionamiento

---

## 📈 **Monitoreo y Observabilidad**

### **Métricas de Aplicación**
- **Latencia**: < 2 segundos promedio
- **Throughput**: 100 requests/hour por API key
- **Error Rate**: < 5%
- **Availability**: 99%+ uptime

### **Métricas de Modelo**
- **Prediction Accuracy**: 90.1% confianza promedio
- **Feature Drift**: Monitoreo continuo
- **Data Quality**: 95%+ completitud

---

## 🔒 **Seguridad**

### **Autenticación y Autorización**
- **API Key**: `X-API-Key` header requerido
- **Rate Limiting**: 100 requests/hour por API key
- **HTTPS**: Comunicación encriptada
- **CORS**: Configurado para dominios específicos

---

## 📈 **Escalabilidad y Performance**

### **Escalabilidad Horizontal**
- **Auto-scaling**: 0-3 instancias automáticas
- **Load Balancing**: Distribución automática
- **Stateless**: Sin estado compartido
- **Container-based**: Fácil escalamiento

### **Optimizaciones de Performance**
- **Caching**: Cache de predicciones por 1 hora
- **Async Processing**: Operaciones asíncronas
- **Connection Pooling**: Reutilización de conexiones

---

**📅 Fecha**: Septiembre 28, 2025  
**👨‍💻 Desarrollado por**: Armando Rodriguez Rocha  
**📧 Contacto**: [rr.armando@gmail.com](mailto:rr.armando@gmail.com)  
**🏷️ Versión**: 2.1.0 - Dynamic Confidence Edition
