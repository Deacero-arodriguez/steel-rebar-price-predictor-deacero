#!/bin/bash
# Script para verificar estado del presupuesto
# Proyecto: steel-rebar-predictor-deacero

echo "💰 Verificando estado del presupuesto..."

# Listar presupuestos
echo "📋 Presupuestos configurados:"
gcloud billing budgets list --billing-account=BILLING_ACCOUNT_ID

# Verificar alertas activas
echo "🔔 Alertas activas:"
gcloud alpha monitoring policies list --project=steel-rebar-predictor-deacero

# Verificar costos actuales
echo "📊 Costos actuales:"
gcloud billing budgets list --billing-account=BILLING_ACCOUNT_ID --format="table(displayName,budgetFilter.projects,amount.specifiedAmount.units,thresholdRules.thresholdPercent)"

echo "✅ Verificación completada"
