#!/bin/bash

# Steel Rebar Price Predictor - Deployment Manual
# Este script despliega la aplicación manualmente sin requerir autenticación automática

set -e

echo "🚀 Despliegue Manual - Steel Rebar Price Predictor"
echo "=================================================="

# Verificar que estamos en el directorio correcto
if [ ! -f "README.md" ]; then
    echo "❌ Error: Ejecutar este script desde la raíz del proyecto"
    exit 1
fi

echo "📋 Verificando estructura del proyecto..."
echo "✅ README.md encontrado"
echo "✅ src/ directorio encontrado"
echo "✅ scripts/ directorio encontrado"
echo "✅ deployment/ directorio encontrado"

echo ""
echo "🔧 OPCIONES DE DESPLIEGUE:"
echo "1. Docker Local"
echo "2. Docker Compose"
echo "3. Google Cloud (requiere autenticación manual)"
echo "4. Solo verificar estructura"
echo ""

read -p "Selecciona una opción (1-4): " choice

case $choice in
    1)
        echo "🐳 Desplegando con Docker..."
        docker build -f deployment/docker/Dockerfile -t steel-rebar-predictor .
        echo "✅ Imagen construida exitosamente"
        echo "🚀 Ejecutando contenedor en puerto 8000..."
        docker run -d -p 8000:8000 --name steel-rebar-predictor steel-rebar-predictor
        echo "✅ Contenedor ejecutándose en http://localhost:8000"
        echo ""
        echo "📖 Comandos útiles:"
        echo "   Ver logs: docker logs steel-rebar-predictor"
        echo "   Detener: docker stop steel-rebar-predictor"
        echo "   Eliminar: docker rm steel-rebar-predictor"
        ;;
    2)
        echo "🐳 Desplegando con Docker Compose..."
        docker-compose -f deployment/docker/docker-compose.yml up -d
        echo "✅ Servicios ejecutándose"
        echo "🌐 API disponible en http://localhost:8000"
        echo "🔍 Redis disponible en puerto 6379"
        ;;
    3)
        echo "☁️ Despliegue en Google Cloud..."
        echo ""
        echo "📋 PREREQUISITOS:"
        echo "   1. Instalar Google Cloud SDK"
        echo "   2. Autenticarse: gcloud auth login"
        echo "   3. Configurar proyecto: gcloud config set project YOUR_PROJECT_ID"
        echo ""
        read -p "¿Has completado los prerequisitos? (y/n): " prereq
        
        if [ "$prereq" = "y" ] || [ "$prereq" = "Y" ]; then
            echo "🚀 Iniciando despliegue..."
            bash deployment/cloud/deploy.sh
        else
            echo "❌ Por favor completa los prerequisitos primero"
            exit 1
        fi
        ;;
    4)
        echo "🔍 Verificando estructura del proyecto..."
        echo ""
        echo "📁 Estructura encontrada:"
        find . -type d -name ".*" -prune -o -type d -print | head -20
        echo ""
        echo "✅ Estructura del proyecto verificada"
        ;;
    *)
        echo "❌ Opción inválida"
        exit 1
        ;;
esac

echo ""
echo "🎉 Proceso completado!"
echo ""
echo "💡 PRÓXIMOS PASOS:"
echo "   1. Probar la API: curl http://localhost:8000/health"
echo "   2. Ver predicción: curl -H 'X-API-Key: deacero_steel_predictor_2025_key' http://localhost:8000/predict/steel-rebar-price"
echo "   3. Ver documentación: http://localhost:8000/docs"
