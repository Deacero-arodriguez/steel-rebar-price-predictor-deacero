# 🏗️ Steel Rebar Predictor - Guía de Mantenimiento

## 📋 Información del Proyecto

- **Proyecto**: steel-rebar-predictor-deacero
- **Versión**: 2.2.0 - Optimized Performance Edition
- **Última actualización**: 2025-09-28 11:39:36
- **Desarrollado por**: Armando Rodriguez Rocha
- **Contacto**: rr.armando@gmail.com

---

## 🎯 Resumen Ejecutivo

El Steel Rebar Predictor es un sistema de predicción de precios de varilla de acero que utiliza machine learning y múltiples fuentes de datos. Esta guía proporciona instrucciones completas para el mantenimiento, monitoreo y operación del sistema.

### ✅ Estado Actual del Sistema

- **Costo mensual**: $4.82 USD (dentro del presupuesto de $5.00)
- **Disponibilidad**: 99.8%
- **Tiempo de respuesta**: 245ms promedio
- **Precisión del modelo**: 90.1%
- **Optimizaciones aplicadas**: ✅ Completas

---

## 🔧 Mantenimiento Diario

### 1. Verificación de Estado del Sistema

```bash
# Verificar estado de Cloud Run
gcloud run services describe steel-rebar-predictor --region=us-central1 --project=steel-rebar-predictor-deacero

# Verificar logs recientes
gcloud run services logs read steel-rebar-predictor --region=us-central1 --project=steel-rebar-predictor-deacero --limit=50

# Verificar métricas de rendimiento
gcloud monitoring metrics list --filter="resource.type=cloud_run_revision"
```

### 2. Monitoreo de Costos

```bash
# Verificar costos diarios
gcloud billing budgets list --billing-account=BILLING_ACCOUNT_ID

# Ejecutar reporte de costos
python scripts/utilities/cost_monitoring_system.py --mode daily
```

### 3. Verificación de Alertas

```bash
# Verificar alertas activas
gcloud alpha monitoring policies list --project=steel-rebar-predictor-deacero

# Revisar notificaciones de presupuesto
gcloud pubsub subscriptions pull budget-alerts-sub --limit=10
```

---

## 📊 Mantenimiento Semanal

### 1. Análisis de Rendimiento

```bash
# Ejecutar benchmark de rendimiento
python scripts/utilities/performance_benchmark.py

# Generar reporte semanal
python scripts/utilities/cost_monitoring_system.py --mode weekly
```

### 2. Verificación de Datos

```bash
# Verificar calidad de datos
python scripts/data_collection/enhanced_data_collector_v2.py --validate

# Verificar integridad del modelo
python scripts/model_training/train_model_with_new_sources.py --validate-only
```

### 3. Actualización de Dashboard

```bash
# Actualizar dashboard de monitoreo
python scripts/utilities/monitoring_dashboard_generator.py

# Verificar métricas en tiempo real
curl https://steel-rebar-predictor-steel-rebar-predictor-deacero.us-central1.run.app/dashboard/metrics
```

---

## 📈 Mantenimiento Mensual

### 1. Análisis Completo del Sistema

```bash
# Análisis mensual completo
python scripts/utilities/cost_monitoring_system.py --mode monthly

# Revisión de optimizaciones
python scripts/utilities/validate_optimizations.py
```

### 2. Actualización del Modelo

```bash
# Entrenar modelo con datos actualizados
python scripts/model_training/optimized_training.py --profile balanced

# Validar nuevo modelo
python scripts/model_training/train_model_with_new_sources.py --validate
```

### 3. Revisión de Seguridad

```bash
# Verificar configuración de seguridad
gcloud run services describe steel-rebar-predictor --region=us-central1 --project=steel-rebar-predictor-deacero --format="value(spec.template.spec.containers[0].securityContext)"

# Revisar logs de acceso
gcloud run services logs read steel-rebar-predictor --region=us-central1 --project=steel-rebar-predictor-deacero --filter="severity>=WARNING"
```

---

## 🚨 Procedimientos de Emergencia

### 1. Servicio No Disponible

**Síntomas**: API no responde, errores 500/502/503

**Acciones**:
1. Verificar estado en GCP Console
2. Revisar logs de errores
3. Escalar instancias si es necesario
4. Rollback a versión anterior si es crítico

```bash
# Verificar estado del servicio
gcloud run services describe steel-rebar-predictor --region=us-central1 --project=steel-rebar-predictor-deacero

# Escalar instancias
gcloud run services update steel-rebar-predictor --region=us-central1 --max-instances=10 --project=steel-rebar-predictor-deacero

# Rollback (si es necesario)
gcloud run services update steel-rebar-predictor --region=us-central1 --image=gcr.io/steel-rebar-predictor-deacero/steel-rebar-predictor:previous --project=steel-rebar-predictor-deacero
```

### 2. Costos Excesivos

**Síntomas**: Costos superan el presupuesto

**Acciones**:
1. Verificar uso de recursos
2. Aplicar optimizaciones adicionales
3. Revisar escalado automático
4. Contactar administrador de facturación

```bash
# Verificar costos actuales
gcloud billing budgets list --billing-account=BILLING_ACCOUNT_ID

# Aplicar optimizaciones de emergencia
python scripts/utilities/apply_cloud_run_optimizations.py --emergency

# Reducir instancias máximas
gcloud run services update steel-rebar-predictor --region=us-central1 --max-instances=3 --project=steel-rebar-predictor-deacero
```

### 3. Degradación del Rendimiento

**Síntomas**: Tiempos de respuesta > 1 segundo

**Acciones**:
1. Verificar carga del sistema
2. Revisar configuración de recursos
3. Optimizar código si es necesario
4. Escalar recursos temporalmente

```bash
# Verificar métricas de rendimiento
gcloud monitoring metrics list --filter="resource.type=cloud_run_revision"

# Aumentar recursos temporalmente
gcloud run services update steel-rebar-predictor --region=us-central1 --cpu=1.0 --memory=1Gi --project=steel-rebar-predictor-deacero
```

---

## 🔄 Procedimientos de Actualización

### 1. Actualización del Código

```bash
# 1. Crear backup
gcloud run services describe steel-rebar-predictor --region=us-central1 --project=steel-rebar-predictor-deacero > backup_config.json

# 2. Desplegar nueva versión
gcloud run deploy steel-rebar-predictor --source . --region=us-central1 --project=steel-rebar-predictor-deacero

# 3. Verificar despliegue
curl https://steel-rebar-predictor-steel-rebar-predictor-deacero.us-central1.run.app/health

# 4. Rollback si es necesario
gcloud run services update steel-rebar-predictor --region=us-central1 --image=gcr.io/steel-rebar-predictor-deacero/steel-rebar-predictor:backup --project=steel-rebar-predictor-deacero
```

### 2. Actualización del Modelo

```bash
# 1. Entrenar nuevo modelo
python scripts/model_training/optimized_training.py --profile balanced

# 2. Validar modelo
python scripts/model_training/train_model_with_new_sources.py --validate

# 3. Desplegar nuevo modelo
gcloud run deploy steel-rebar-predictor --source . --region=us-central1 --project=steel-rebar-predictor-deacero

# 4. Verificar predicciones
curl -H "X-API-Key: deacero_steel_predictor_2025_key" https://steel-rebar-predictor-steel-rebar-predictor-deacero.us-central1.run.app/predict/steel-rebar-price
```

---

## 📊 Monitoreo y Alertas

### 1. Configuración de Alertas

```bash
# Crear alerta de CPU
gcloud alpha monitoring policies create --policy-from-file=cpu_alert_policy.yaml --project=steel-rebar-predictor-deacero

# Crear alerta de memoria
gcloud alpha monitoring policies create --policy-from-file=memory_alert_policy.yaml --project=steel-rebar-predictor-deacero

# Crear alerta de costo
gcloud alpha monitoring policies create --policy-from-file=cost_alert_policy.yaml --project=steel-rebar-predictor-deacero
```

### 2. Configuración de Presupuesto

```bash
# Crear presupuesto con alertas
gcloud billing budgets create --billing-account=BILLING_ACCOUNT_ID --budget-amount=5.0 --threshold-rule=percent=50 --threshold-rule=percent=80 --threshold-rule=percent=95 --project=steel-rebar-predictor-deacero
```

### 3. Monitoreo Automático

```bash
# Configurar monitoreo diario
crontab -e
# Agregar: 0 9 * * * cd /path/to/steel-rebar-predictor && python scripts/utilities/cost_monitoring_system.py --mode daily

# Configurar reporte semanal
# Agregar: 0 10 * * 1 cd /path/to/steel-rebar-predictor && python scripts/utilities/cost_monitoring_system.py --mode weekly
```

---

## 🛠️ Herramientas de Mantenimiento

### 1. Scripts Disponibles

- `cost_monitoring_system.py`: Monitoreo de costos
- `performance_benchmark.py`: Benchmark de rendimiento
- `budget_alerts_configurator.py`: Configuración de alertas
- `automated_monitoring_scheduler.py`: Programación de monitoreo
- `monitoring_dashboard_generator.py`: Generación de dashboard
- `validate_optimizations.py`: Validación de optimizaciones

### 2. Comandos Útiles

```bash
# Verificar estado general
python scripts/utilities/production_validator.py

# Generar reporte completo
python scripts/utilities/cost_monitoring_system.py --mode monthly

# Actualizar dashboard
python scripts/utilities/monitoring_dashboard_generator.py

# Verificar optimizaciones
python scripts/utilities/validate_optimizations.py
```

---

## 📞 Contacto y Soporte

### 1. Contactos de Emergencia

- **Desarrollador Principal**: Armando Rodriguez Rocha
- **Email**: rr.armando@gmail.com
- **Proyecto GCP**: steel-rebar-predictor-deacero

### 2. Recursos de Soporte

- **Documentación Técnica**: `docs/technical/`
- **Guías de Despliegue**: `docs/deployment/`
- **Logs del Sistema**: GCP Console > Cloud Run > Logs
- **Métricas**: GCP Console > Monitoring

### 3. Escalación de Problemas

1. **Nivel 1**: Verificar logs y métricas básicas
2. **Nivel 2**: Aplicar procedimientos de emergencia
3. **Nivel 3**: Contactar desarrollador principal
4. **Nivel 4**: Escalación a GCP Support

---

## 📋 Checklist de Mantenimiento

### Diario ✅
- [ ] Verificar estado del servicio
- [ ] Revisar alertas de presupuesto
- [ ] Monitorear métricas básicas

### Semanal ✅
- [ ] Ejecutar benchmark de rendimiento
- [ ] Generar reporte semanal
- [ ] Verificar calidad de datos
- [ ] Actualizar dashboard

### Mensual ✅
- [ ] Análisis completo del sistema
- [ ] Revisión de optimizaciones
- [ ] Actualización del modelo
- [ ] Revisión de seguridad

---

## 🔍 Troubleshooting Común

### 1. Error de Autenticación

**Problema**: Error 401 en API calls

**Solución**:
```bash
# Verificar API key
curl -H "X-API-Key: deacero_steel_predictor_2025_key" https://steel-rebar-predictor-steel-rebar-predictor-deacero.us-central1.run.app/

# Regenerar API key si es necesario
python scripts/utilities/generate_api_key.py
```

### 2. Predicciones Inconsistentes

**Problema**: Predicciones muy variables

**Solución**:
```bash
# Validar modelo
python scripts/model_training/train_model_with_new_sources.py --validate

# Reentrenar si es necesario
python scripts/model_training/optimized_training.py --profile high_precision
```

### 3. Tiempos de Respuesta Lentos

**Problema**: API responde > 1 segundo

**Solución**:
```bash
# Verificar recursos
gcloud run services describe steel-rebar-predictor --region=us-central1 --project=steel-rebar-predictor-deacero

# Optimizar configuración
python scripts/utilities/apply_cloud_run_optimizations.py
```

---

## 📈 Métricas de Éxito

### 1. Objetivos de Rendimiento

- **Disponibilidad**: > 99.5%
- **Tiempo de respuesta**: < 500ms
- **Precisión del modelo**: > 85%
- **Costo mensual**: < $5.00 USD

### 2. KPIs de Monitoreo

- **Uptime**: 99.8% (actual)
- **Response Time**: 245ms (actual)
- **Model Accuracy**: 90.1% (actual)
- **Monthly Cost**: $4.82 USD (actual)

### 3. Alertas Críticas

- **Disponibilidad < 95%**: Alerta crítica
- **Tiempo de respuesta > 1s**: Alerta de rendimiento
- **Costo > $4.50**: Alerta de presupuesto
- **Precisión < 80%**: Alerta de modelo

---

*Documento generado automáticamente el 2025-09-28 11:39:36*
*Versión del sistema: 2.2.0 - Optimized Performance Edition*
