#!/bin/bash

# Script para configurar recursos básicos de GCP para automatización
# Este script configura los recursos que no dependen de los endpoints de automatización

set -e

echo "🚀 CONFIGURANDO RECURSOS BÁSICOS DE GCP"
echo "======================================="

PROJECT_ID="steel-rebar-predictor-deacero"
REGION="us-central1"

echo "📋 Configuración:"
echo "   Proyecto: $PROJECT_ID"
echo "   Región: $REGION"
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

# Configurar presupuesto y alertas
echo "💰 Configurando presupuesto..."

# Obtener ID de cuenta de facturación
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

# Verificar buckets de storage
echo "🗄️ Buckets de Cloud Storage:"
gsutil ls | grep $PROJECT_ID || echo "   No se encontraron buckets"

echo ""

# Verificar APIs habilitadas
echo "🔧 APIs habilitadas:"
gcloud services list --enabled --filter="name:(cloudbuild.googleapis.com OR run.googleapis.com OR scheduler.googleapis.com)" --format="table(name,title)"

echo ""

echo "🎉 CONFIGURACIÓN BÁSICA COMPLETADA"
echo "=================================="
echo ""
echo "✅ Recursos configurados:"
echo "   - Cloud Storage buckets (3)"
echo "   - Presupuesto configurado"
echo "   - APIs habilitadas"
echo ""
echo "📅 Próximos pasos:"
echo "   1. Esperar a que los endpoints de automatización estén disponibles"
echo "   2. Configurar Cloud Scheduler jobs"
echo "   3. Configurar Redis Cache"
echo "   4. Configurar monitoreo"
echo ""
echo "🔗 Enlaces útiles:"
echo "   - Cloud Console: https://console.cloud.google.com/welcome?project=$PROJECT_ID"
echo "   - Cloud Storage: https://console.cloud.google.com/storage?project=$PROJECT_ID"
echo ""
echo "🚀 Recursos básicos listos para automatización!"
