#!/bin/bash
# Script para configurar presupuesto de $5.0 USD/mes
# Proyecto: steel-rebar-predictor-deacero

echo "💰 Configurando presupuesto de $5.0 USD/mes..."

# Verificar que el usuario esté autenticado
gcloud auth list --filter=status:ACTIVE --format="value(account)" | head -1

# Crear presupuesto con alertas
gcloud billing budgets create \
    --billing-account=BILLING_ACCOUNT_ID \
    --budget-amount=5.0 \
    --threshold-rule=percent=50 \
    --threshold-rule=percent=80 \
    --threshold-rule=percent=95 \
    --project=steel-rebar-predictor-deacero

echo "✅ Presupuesto configurado exitosamente"
echo "📊 Alertas configuradas en 50%, 80% y 95%"
echo "📧 Revisar configuración de notificaciones en GCP Console"
