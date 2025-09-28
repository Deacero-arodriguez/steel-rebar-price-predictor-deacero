# 🚀 **GUÍA DE DESPLIEGUE**
## Steel Rebar Price Predictor - DeAcero

> **Guía completa para el despliegue del sistema en Google Cloud Platform**

---

## 🎯 **RESUMEN EJECUTIVO**

### **Arquitectura de Despliegue**
- **Plataforma**: Google Cloud Platform (GCP)
- **Servicio Principal**: Cloud Run
- **Base de Datos**: Redis (Cloud Memorystore)
- **Orquestación**: Cloud Build + Cloud Scheduler
- **Monitoreo**: Cloud Logging + Cloud Monitoring
- **Costo Objetivo**: < $5 USD/mes

### **Componentes del Sistema**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Cloud Run     │    │   Redis Cache   │    │   Cloud Build   │
│   (API Server)  │◄──►│  (Memorystore)  │    │  (CI/CD)        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Cloud Scheduler │    │  Cloud Logging  │    │ Cloud Functions │
│ (Data Updates)  │    │  (Monitoring)   │    │ (Background)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 📋 **PREREQUISITOS**

### **1. Cuenta de Google Cloud**
- **Proyecto GCP**: Creado y configurado
- **Billing**: Habilitado (presupuesto configurado)
- **APIs habilitadas**:
  - Cloud Run API
  - Cloud Build API
  - Cloud Memorystore API
  - Cloud Scheduler API
  - Cloud Logging API
  - Cloud Monitoring API

### **2. Herramientas Locales**
- **gcloud CLI**: Instalado y configurado
- **Docker**: Instalado y funcionando
- **Python 3.9+**: Entorno de desarrollo
- **Git**: Control de versiones

### **3. API Keys Externas**
- **Yahoo Finance**: Gratuita (no requiere key)
- **Alpha Vantage**: Gratuita (límite 25 req/día)
- **FRED API**: Gratuita (registro requerido)
- **World Bank**: Gratuita (no requiere key)

---

## 🏗️ **CONFIGURACIÓN INICIAL**

### **1. Configurar gcloud CLI**
```bash
# Inicializar gcloud
gcloud init

# Configurar proyecto
gcloud config set project YOUR_PROJECT_ID

# Configurar región
gcloud config set run/region us-central1
gcloud config set run/platform managed
```

### **2. Habilitar APIs Requeridas**
```bash
# Habilitar APIs necesarias
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable redis.googleapis.com
gcloud services enable cloudscheduler.googleapis.com
gcloud services enable logging.googleapis.com
gcloud services enable monitoring.googleapis.com
```

### **3. Configurar Service Account**
```bash
# Crear service account
gcloud iam service-accounts create steel-rebar-api \
    --display-name="Steel Rebar API Service Account" \
    --description="Service account for Steel Rebar Price Predictor"

# Asignar roles necesarios
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:steel-rebar-api@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:steel-rebar-api@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/redis.editor"
```

---

## 🐳 **DESPLIEGUE CON DOCKER**

### **1. Construir Imagen Docker**
```bash
# Navegar al directorio del proyecto
cd steel-rebar-predictor

# Construir imagen
docker build -t gcr.io/YOUR_PROJECT_ID/steel-rebar-api:latest .

# Subir imagen a Container Registry
docker push gcr.io/YOUR_PROJECT_ID/steel-rebar-api:latest
```

### **2. Desplegar en Cloud Run**
```bash
# Desplegar servicio
gcloud run deploy steel-rebar-api \
    --image gcr.io/YOUR_PROJECT_ID/steel-rebar-api:latest \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --concurrency 100 \
    --max-instances 10 \
    --timeout 300 \
    --set-env-vars="REDIS_HOST=YOUR_REDIS_IP,PORT=8080"
```

---

## 🔧 **CONFIGURACIÓN DE REDIS**

### **1. Crear Instancia Redis**
```bash
# Crear instancia Redis
gcloud redis instances create steel-rebar-cache \
    --size=1 \
    --region=us-central1 \
    --redis-version=redis_6_x \
    --tier=basic \
    --memory-size-gb=1
```

### **2. Configurar Variables de Entorno**
```bash
# Obtener IP de Redis
REDIS_IP=$(gcloud redis instances describe steel-rebar-cache \
    --region=us-central1 \
    --format="value(host)")

# Actualizar Cloud Run con IP de Redis
gcloud run services update steel-rebar-api \
    --region=us-central1 \
    --set-env-vars="REDIS_HOST=$REDIS_IP"
```

---

## 📊 **CONFIGURACIÓN DE MONITOREO**

### **1. Configurar Cloud Logging**
```bash
# Crear log sink para errores
gcloud logging sinks create steel-rebar-errors \
    bigquery.googleapis.com/projects/YOUR_PROJECT_ID/datasets/steel_rebar_logs \
    --log-filter="severity>=ERROR AND resource.type=cloud_run_revision"
```

### **2. Configurar Alertas**
```bash
# Crear política de alerta para errores
gcloud alpha monitoring policies create \
    --policy-from-file=deployment/monitoring/error-alert-policy.yaml
```

### **3. Dashboard de Monitoreo**
```bash
# Crear dashboard
gcloud monitoring dashboards create \
    --config-from-file=deployment/monitoring/dashboard-config.json
```

---

## 🔄 **CI/CD CON CLOUD BUILD**

### **1. Configurar cloudbuild.yaml**
```yaml
# deployment/cloud/cloudbuild.yaml
steps:
  # Construir imagen Docker
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/steel-rebar-api:$COMMIT_SHA', '.']
  
  # Subir imagen
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/steel-rebar-api:$COMMIT_SHA']
  
  # Desplegar en Cloud Run
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'steel-rebar-api'
      - '--image=gcr.io/$PROJECT_ID/steel-rebar-api:$COMMIT_SHA'
      - '--region=us-central1'
      - '--platform=managed'
      - '--allow-unauthenticated'
      - '--memory=2Gi'
      - '--cpu=2'
      - '--concurrency=100'
      - '--max-instances=10'
      - '--timeout=300'

options:
  machineType: 'E2_HIGHCPU_8'
  diskSizeGb: 100
```

### **2. Configurar Trigger**
```bash
# Crear trigger de Cloud Build
gcloud builds triggers create github \
    --repo-name=steel-rebar-price-predictor-deacero \
    --repo-owner=Deacero-arodriguez \
    --branch-pattern=main \
    --build-config=deployment/cloud/cloudbuild.yaml
```

---

## ⏰ **AUTOMATIZACIÓN CON CLOUD SCHEDULER**

### **1. Crear Job de Actualización de Datos**
```bash
# Crear job para actualización diaria de datos
gcloud scheduler jobs create http daily-data-update \
    --schedule="0 2 * * *" \
    --uri="https://YOUR_CLOUD_RUN_URL/update-data" \
    --http-method=POST \
    --headers="X-API-Key=YOUR_API_KEY" \
    --time-zone="America/Mexico_City"
```

### **2. Crear Job de Reentrenamiento**
```bash
# Crear job para reentrenamiento semanal
gcloud scheduler jobs create http weekly-retraining \
    --schedule="0 3 * * 0" \
    --uri="https://YOUR_CLOUD_RUN_URL/retrain-model" \
    --http-method=POST \
    --headers="X-API-Key=YOUR_API_KEY" \
    --time-zone="America/Mexico_City"
```

---

## 💰 **OPTIMIZACIÓN DE COSTOS**

### **1. Configurar Presupuesto**
```bash
# Crear presupuesto de $5 USD/mes
gcloud billing budgets create \
    --billing-account=YOUR_BILLING_ACCOUNT \
    --display-name="Steel Rebar API Budget" \
    --budget-amount=5USD \
    --threshold-rule=percent=80 \
    --threshold-rule=percent=100
```

### **2. Optimizaciones de Cloud Run**
```yaml
# Configuración optimizada
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/maxScale: "5"        # Máximo 5 instancias
        autoscaling.knative.dev/minScale: "0"        # Escalamiento a 0
        run.googleapis.com/cpu-throttling: "true"    # Throttling de CPU
    spec:
      containerConcurrency: 100                      # 100 requests por instancia
      timeoutSeconds: 300                            # Timeout de 5 minutos
      containers:
      - image: gcr.io/PROJECT/steel-rebar-api
        resources:
          limits:
            cpu: "2"                                 # 2 vCPUs
            memory: "2Gi"                            # 2GB RAM
        env:
        - name: PORT
          value: "8080"
```

### **3. Configuración de Redis**
```bash
# Redis básico (1GB) - $0.054/hora
gcloud redis instances create steel-rebar-cache \
    --size=1 \
    --region=us-central1 \
    --redis-version=redis_6_x \
    --tier=basic \
    --memory-size-gb=1
```

---

## 📊 **ESTIMACIÓN DE COSTOS**

### **Costos Mensuales Estimados**

| Servicio | Configuración | Costo/Mes |
|----------|---------------|-----------|
| **Cloud Run** | 2 vCPU, 2GB RAM, 100 req/hora | $2.50 |
| **Redis** | 1GB básico | $1.50 |
| **Cloud Build** | 10 builds/mes | $0.50 |
| **Cloud Scheduler** | 2 jobs | $0.20 |
| **Cloud Logging** | 1GB logs/mes | $0.20 |
| **Cloud Monitoring** | Métricas básicas | $0.10 |
| **Container Registry** | 1GB storage | $0.05 |
| **Total** | | **$5.05** |

### **Factores de Escalación**
- **Tráfico bajo** (<100 req/hora): $3-4/mes
- **Tráfico medio** (100-500 req/hora): $5-7/mes
- **Tráfico alto** (500+ req/hora): $8-12/mes

---

## 🔒 **CONFIGURACIÓN DE SEGURIDAD**

### **1. Configurar API Keys**
```bash
# Crear API key para el servicio
gcloud services api-keys create \
    --display-name="Steel Rebar API Key" \
    --restrictions-api-targets="run.googleapis.com"
```

### **2. Configurar IAM**
```bash
# Asignar permisos mínimos
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:steel-rebar-api@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/run.invoker"
```

### **3. Configurar VPC (Opcional)**
```bash
# Crear VPC para Redis
gcloud compute networks create steel-rebar-vpc \
    --subnet-mode=regional \
    --bgp-routing-mode=regional
```

---

## 🧪 **VALIDACIÓN DEL DESPLIEGUE**

### **1. Tests de Salud**
```bash
# Test de conectividad
curl -X GET "https://YOUR_CLOUD_RUN_URL/health"

# Test de predicción
curl -X GET "https://YOUR_CLOUD_RUN_URL/predict/steel-rebar-price" \
     -H "X-API-Key: YOUR_API_KEY"
```

### **2. Tests de Rendimiento**
```bash
# Test de carga (usando Apache Bench)
ab -n 100 -c 10 -H "X-API-Key: YOUR_API_KEY" \
   "https://YOUR_CLOUD_RUN_URL/predict/steel-rebar-price"
```

### **3. Tests de Monitoreo**
```bash
# Verificar logs
gcloud logging read "resource.type=cloud_run_revision" \
    --limit=50 \
    --format="table(timestamp,severity,textPayload)"

# Verificar métricas
gcloud monitoring metrics list --filter="metric.type:run.googleapis.com"
```

---

## 🔧 **MANTENIMIENTO Y OPERACIONES**

### **1. Actualización del Modelo**
```bash
# Trigger manual de reentrenamiento
gcloud scheduler jobs run weekly-retraining \
    --location=us-central1
```

### **2. Backup y Recuperación**
```bash
# Backup del modelo
gsutil cp data/models/*.pkl gs://YOUR_BUCKET/backups/

# Restaurar modelo
gsutil cp gs://YOUR_BUCKET/backups/*.pkl data/models/
```

### **3. Scaling Manual**
```bash
# Escalar manualmente
gcloud run services update steel-rebar-api \
    --region=us-central1 \
    --max-instances=20 \
    --memory=4Gi \
    --cpu=4
```

---

## 📞 **SOPORTE Y TROUBLESHOOTING**

### **Comandos Útiles**
```bash
# Ver logs en tiempo real
gcloud logging tail "resource.type=cloud_run_revision"

# Ver métricas de rendimiento
gcloud monitoring metrics list --filter="metric.type:run.googleapis.com/request_count"

# Ver estado del servicio
gcloud run services describe steel-rebar-api --region=us-central1

# Reiniciar servicio
gcloud run services update steel-rebar-api --region=us-central1
```

### **Problemas Comunes**
1. **Error 429**: Rate limiting - revisar configuración de Redis
2. **Error 500**: Modelo no cargado - verificar logs de inicio
3. **Alta latencia**: Revisar configuración de CPU/memoria
4. **Costos altos**: Revisar configuración de scaling

---

## ✅ **CHECKLIST DE DESPLIEGUE**

### **Pre-Despliegue**
- [ ] Proyecto GCP creado y configurado
- [ ] APIs habilitadas
- [ ] Service account configurado
- [ ] API keys externas obtenidas
- [ ] Presupuesto configurado

### **Despliegue**
- [ ] Imagen Docker construida
- [ ] Cloud Run desplegado
- [ ] Redis configurado
- [ ] Variables de entorno configuradas
- [ ] Monitoreo configurado

### **Post-Despliegue**
- [ ] Tests de salud pasando
- [ ] Tests de rendimiento pasando
- [ ] Monitoreo funcionando
- [ ] Alertas configuradas
- [ ] Documentación actualizada

---

**🎉 SISTEMA LISTO PARA PRODUCCIÓN**

---

**Última actualización**: 28 de septiembre de 2024  
**Versión de despliegue**: 1.0  
**Estado**: ✅ Producción
