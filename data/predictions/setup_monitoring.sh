#!/bin/bash
# Script para configurar monitoreo del proyecto
# Proyecto: steel-rebar-predictor-deacero

echo "📊 Configurando monitoreo..."

# Habilitar APIs necesarias
gcloud services enable monitoring.googleapis.com --project=steel-rebar-predictor-deacero
gcloud services enable logging.googleapis.com --project=steel-rebar-predictor-deacero

# Crear políticas de alerta
gcloud alpha monitoring policies create \
    --policy-from-file=cpu_alert_policy.yaml \
    --project=steel-rebar-predictor-deacero

gcloud alpha monitoring policies create \
    --policy-from-file=memory_alert_policy.yaml \
    --project=steel-rebar-predictor-deacero

gcloud alpha monitoring policies create \
    --policy-from-file=cost_alert_policy.yaml \
    --project=steel-rebar-predictor-deacero

echo "✅ Monitoreo configurado exitosamente"
echo "🔔 Políticas de alerta creadas"
echo "📊 Revisar configuración en Cloud Monitoring"
