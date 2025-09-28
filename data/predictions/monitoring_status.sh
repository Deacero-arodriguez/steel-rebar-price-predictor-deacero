#!/bin/bash
# Script para verificar el estado del monitoreo
# Proyecto: steel-rebar-predictor-deacero

echo "📊 Estado del Sistema de Monitoreo"
echo "=================================="

# Verificar procesos activos
echo "🔍 Procesos activos:"
ps aux | grep -E "(cost_monitoring|performance_benchmark)" | grep -v grep

# Verificar trabajos de cron
echo "⏰ Trabajos programados:"
crontab -l 2>/dev/null | grep -E "(monitoring|benchmark)" || echo "No hay trabajos programados"

# Verificar logs recientes
echo "📄 Logs recientes:"
if [ -d "logs" ]; then
    ls -la logs/ | tail -5
else
    echo "Directorio de logs no encontrado"
fi

# Verificar archivos de configuración
echo "⚙️ Archivos de configuración:"
ls -la scripts/utilities/*monitoring*.py 2>/dev/null || echo "Scripts de monitoreo no encontrados"

echo "✅ Verificación completada"
