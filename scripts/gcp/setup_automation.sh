#!/bin/bash

# Steel Rebar Price Predictor - Configuración de Automatización en GCP
# Este script configura todos los recursos necesarios para la automatización

set -e

echo "🚀 CONFIGURANDO AUTOMATIZACIÓN EN GCP"
echo "======================================"

# Variables de configuración
PROJECT_ID="steel-rebar-predictor-deacero"
REGION="us-central1"
API_URL="https://steel-rebar-predictor-646072255295.us-central1.run.app"
API_KEY="deacero_steel_predictor_2025_key"

echo "📋 Configuración:"
echo "   Proyecto: $PROJECT_ID"
echo "   Región: $REGION"
echo "   API URL: $API_URL"
echo ""

# Verificar que gcloud esté configurado
echo "🔍 Verificando configuración de gcloud..."
if ! gcloud config get-value project > /dev/null 2>&1; then
    echo "❌ Error: gcloud no está configurado"
    echo "   Ejecuta: gcloud auth login"
    echo "   Ejecuta: gcloud config set project $PROJECT_ID"
    exit 1
fi

CURRENT_PROJECT=$(gcloud config get-value project)
if [ "$CURRENT_PROJECT" != "$PROJECT_ID" ]; then
    echo "⚠️ Proyecto actual: $CURRENT_PROJECT"
    echo "   Configurando proyecto correcto: $PROJECT_ID"
    gcloud config set project $PROJECT_ID
fi

echo "✅ gcloud configurado correctamente"
echo ""

# Habilitar APIs necesarias
echo "🔧 Habilitando APIs necesarias..."
APIS=(
    "cloudbuild.googleapis.com"
    "run.googleapis.com"
    "scheduler.googleapis.com"
    "monitoring.googleapis.com"
    "redis.googleapis.com"
    "storage.googleapis.com"
    "logging.googleapis.com"
)

for api in "${APIS[@]}"; do
    echo "   Habilitando $api..."
    gcloud services enable $api --quiet
done

echo "✅ APIs habilitadas correctamente"
echo ""

# Crear buckets de Cloud Storage
echo "🗄️ Configurando Cloud Storage..."
STORAGE_BUCKETS=(
    "steel-rebar-data"
    "steel-rebar-models"
    "steel-rebar-backups"
)

for bucket in "${STORAGE_BUCKETS[@]}"; do
    BUCKET_NAME="gs://${PROJECT_ID}-${bucket}"
    echo "   Creando bucket: $BUCKET_NAME"
    
    if gsutil ls $BUCKET_NAME > /dev/null 2>&1; then
        echo "     ✅ Bucket ya existe"
    else
        gsutil mb -l $REGION $BUCKET_NAME
        echo "     ✅ Bucket creado"
    fi
done

echo "✅ Cloud Storage configurado"
echo ""

# Configurar Redis (opcional, puede ser costoso)
echo "⚡ Configurando Redis Cache..."
REDIS_INSTANCE="steel-rebar-cache"

if gcloud redis instances describe $REDIS_INSTANCE --region=$REGION > /dev/null 2>&1; then
    echo "   ✅ Instancia Redis ya existe"
else
    echo "   ⚠️ Creando instancia Redis (esto puede tomar varios minutos)..."
    gcloud redis instances create $REDIS_INSTANCE \
        --size=1 \
        --region=$REGION \
        --redis-version=redis_6_x \
        --tier=basic \
        --memory-size-gb=1 \
        --quiet
    
    echo "   ✅ Instancia Redis creada"
fi

echo "✅ Redis configurado"
echo ""

# Crear jobs de Cloud Scheduler
echo "⏰ Configurando Cloud Scheduler..."

# Job 1: Actualización diaria de datos
echo "   Creando job de actualización diaria de datos..."
gcloud scheduler jobs create http daily-data-update \
    --schedule="0 2 * * *" \
    --uri="$API_URL/update-data" \
    --http-method=POST \
    --headers="X-API-Key=$API_KEY,Content-Type=application/json" \
    --time-zone="America/Mexico_City" \
    --description="Actualización diaria de datos de mercado a las 2:00 AM" \
    --location=$REGION \
    --quiet || echo "   ⚠️ Job ya existe"

# Job 2: Reentrenamiento semanal
echo "   Creando job de reentrenamiento semanal..."
gcloud scheduler jobs create http weekly-retraining \
    --schedule="0 3 * * 1" \
    --uri="$API_URL/retrain-model" \
    --http-method=POST \
    --headers="X-API-Key=$API_KEY,Content-Type=application/json" \
    --time-zone="America/Mexico_City" \
    --description="Reentrenamiento semanal del modelo ML los lunes a las 3:00 AM" \
    --location=$REGION \
    --quiet || echo "   ⚠️ Job ya existe"

# Job 3: Monitoreo de rendimiento
echo "   Creando job de monitoreo de rendimiento..."
gcloud scheduler jobs create http performance-monitoring \
    --schedule="0 */6 * * *" \
    --uri="$API_URL/monitor-performance" \
    --http-method=POST \
    --headers="X-API-Key=$API_KEY,Content-Type=application/json" \
    --time-zone="America/Mexico_City" \
    --description="Monitoreo de rendimiento cada 6 horas" \
    --location=$REGION \
    --quiet || echo "   ⚠️ Job ya existe"

echo "✅ Cloud Scheduler configurado"
echo ""

# Configurar presupuesto y alertas
echo "💰 Configurando presupuesto y alertas..."

# Crear presupuesto de $5 USD/mes
BILLING_ACCOUNT=$(gcloud billing accounts list --format="value(name)" --limit=1)
if [ -n "$BILLING_ACCOUNT" ]; then
    echo "   Creando presupuesto de $5 USD/mes..."
    gcloud billing budgets create \
        --billing-account=$BILLING_ACCOUNT \
        --display-name="Steel Rebar API Budget" \
        --budget-amount=5USD \
        --threshold-rule=percent=50 \
        --threshold-rule=percent=80 \
        --threshold-rule=percent=100 \
        --quiet || echo "   ⚠️ Presupuesto ya existe"
    
    echo "   ✅ Presupuesto configurado"
else
    echo "   ⚠️ No se encontró cuenta de facturación"
fi

echo "✅ Presupuesto configurado"
echo ""

# Verificar configuración
echo "🔍 Verificando configuración..."
echo ""

echo "📋 RESUMEN DE CONFIGURACIÓN:"
echo "=============================="

# Verificar jobs de scheduler
echo "⏰ Jobs de Cloud Scheduler:"
gcloud scheduler jobs list --location=$REGION --format="table(name,schedule,state)"

echo ""

# Verificar buckets de storage
echo "🗄️ Buckets de Cloud Storage:"
gsutil ls | grep $PROJECT_ID || echo "   No se encontraron buckets"

echo ""

# Verificar instancia Redis
echo "⚡ Instancia Redis:"
gcloud redis instances list --region=$REGION --format="table(name,region,tier,memorySizeGb,state" || echo "   No se encontró instancia Redis"

echo ""

# Verificar APIs habilitadas
echo "🔧 APIs habilitadas:"
gcloud services list --enabled --filter="name:(cloudbuild.googleapis.com OR run.googleapis.com OR scheduler.googleapis.com)" --format="table(name,title)"

echo ""

echo "🎉 CONFIGURACIÓN COMPLETADA EXITOSAMENTE"
echo "========================================"
echo ""
echo "✅ Recursos configurados:"
echo "   - Cloud Scheduler jobs (3)"
echo "   - Cloud Storage buckets (3)"
echo "   - Redis instance (1)"
echo "   - Presupuesto configurado"
echo "   - APIs habilitadas"
echo ""
echo "📅 Próximos pasos:"
echo "   1. Verificar que la API esté funcionando"
echo "   2. Probar los endpoints de automatización"
echo "   3. Monitorear el primer job programado"
echo ""
echo "🔗 Enlaces útiles:"
echo "   - Cloud Console: https://console.cloud.google.com/welcome?project=$PROJECT_ID"
echo "   - Cloud Scheduler: https://console.cloud.google.com/cloudscheduler?project=$PROJECT_ID"
echo "   - Cloud Storage: https://console.cloud.google.com/storage?project=$PROJECT_ID"
echo "   - Cloud Run: https://console.cloud.google.com/run?project=$PROJECT_ID"
echo ""
echo "📊 Para monitorear el sistema:"
echo "   gcloud scheduler jobs list --location=$REGION"
echo "   gcloud logging tail 'resource.type=cloud_run_revision'"
echo ""
echo "🚀 Sistema de automatización listo para operar!"
