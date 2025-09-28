#!/bin/bash
# Script para detener el sistema de monitoreo automático
# Proyecto: steel-rebar-predictor-deacero

echo "⏹️ Deteniendo sistema de monitoreo automático..."

# Matar procesos de monitoreo
pkill -f "cost_monitoring_system.py"
pkill -f "performance_benchmark.py"

# Limpiar trabajos de cron (opcional)
# crontab -r

echo "✅ Sistema de monitoreo detenido"
echo "📊 Logs disponibles en: logs/"
