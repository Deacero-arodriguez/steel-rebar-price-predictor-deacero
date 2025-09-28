#!/bin/bash
# Script para iniciar el sistema de monitoreo automático
# Proyecto: steel-rebar-predictor-deacero

echo "🚀 Iniciando sistema de monitoreo automático..."

# Crear directorio de logs si no existe
mkdir -p logs

# Verificar que Python esté disponible
python3 --version || python --version

# Verificar que los scripts existan
if [ ! -f "scripts/utilities/cost_monitoring_system.py" ]; then
    echo "❌ Error: Script de monitoreo de costos no encontrado"
    exit 1
fi

if [ ! -f "scripts/utilities/performance_benchmark.py" ]; then
    echo "❌ Error: Script de benchmark de rendimiento no encontrado"
    exit 1
fi

echo "✅ Verificaciones completadas"
echo "📅 Sistema de monitoreo iniciado"
echo "📊 Logs se guardarán en: logs/monitoring.log"

# Ejecutar monitoreo inicial
python3 scripts/utilities/cost_monitoring_system.py --mode daily

echo "🎯 Monitoreo inicial completado"
