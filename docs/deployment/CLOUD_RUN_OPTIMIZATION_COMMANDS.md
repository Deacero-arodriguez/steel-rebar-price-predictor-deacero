# 🚀 COMANDOS DE OPTIMIZACIÓN DE CLOUD RUN

## 📋 Comando Combinado (Ejecutar todo de una vez)

```bash
gcloud run services update steel-rebar-predictor \
    --region=us-central1 \
    --cpu=0.5 \
    --memory=512Mi \
    --timeout=30s \
    --max-instances=5 \
    --concurrency=50 \
    --project=steel-rebar-predictor-deacero
```

## 🔧 Comandos Individuales

### 1. Reducir CPU a 0.5 vCPU (Ahorro: $8.64/mes)
```bash
gcloud run services update steel-rebar-predictor --region=us-central1 --cpu=0.5 --project=steel-rebar-predictor-deacero
```

### 2. Reducir memoria a 512Mi (Ahorro: $0.90/mes)
```bash
gcloud run services update steel-rebar-predictor --region=us-central1 --memory=512Mi --project=steel-rebar-predictor-deacero
```

### 3. Configurar timeout a 30s (Ahorro: $0.01/mes)
```bash
gcloud run services update steel-rebar-predictor --region=us-central1 --timeout=30s --project=steel-rebar-predictor-deacero
```

### 4. Limitar instancias máximas a 5 (Preventivo)
```bash
gcloud run services update steel-rebar-predictor --region=us-central1 --max-instances=5 --project=steel-rebar-predictor-deacero
```

### 5. Configurar concurrencia a 50 (Eficiencia)
```bash
gcloud run services update steel-rebar-predictor --region=us-central1 --concurrency=50 --project=steel-rebar-predictor-deacero
```

## 🔍 Comandos de Verificación

### Verificar configuración actual
```bash
gcloud run services describe steel-rebar-predictor --region=us-central1 --project=steel-rebar-predictor-deacero
```

### Verificar recursos específicos
```bash
gcloud run services describe steel-rebar-predictor --region=us-central1 --project=steel-rebar-predictor-deacero --format="value(spec.template.spec.containers[0].resources.limits.cpu,spec.template.spec.containers[0].resources.limits.memory)"
```

### Probar servicio
```bash
curl https://steel-rebar-predictor-steel-rebar-predictor-deacero.us-central1.run.app/health
```

## 💰 Análisis de Costos

- **Costo antes**: $19.08/mes
- **Costo después**: $9.54/mes
- **Ahorro total**: $9.54/mes (50.0%)
- **Presupuesto objetivo**: $5.00/mes
- **Cumplimiento**: NO (necesita más optimizaciones)

## 📋 Instrucciones Paso a Paso

1. **Preparar entorno**: `gcloud auth login` y `gcloud config set project steel-rebar-predictor-deacero`
2. **Verificar estado actual**: Ejecutar comando de verificación
3. **Aplicar optimizaciones**: Ejecutar comando combinado
4. **Verificar cambios**: Confirmar que se aplicaron correctamente
5. **Probar servicio**: Verificar que funciona correctamente
