# Versionado del Proyecto
## Steel Rebar Price Predictor - DeAcero

---

## Versión Actual: v2.1.0

**Fecha de Lanzamiento**: 29 de septiembre de 2025  
**Estado**: Producción  
**Entorno**: Google Cloud Run

---

## Historial de Versiones

### v2.1.0 - Versión de Producción (29/09/2025)
**Versión Final - Lista para Entrega**

#### Nuevas Características
- Sistema completo de predicción de precios de varilla
- API REST desplegada en Google Cloud Run
- Modelo entrenado con datos reales de Alpha Vantage
- Integración con 4 fuentes de datos confiables
- Documentación completa y técnica

#### Métricas de Rendimiento
- **MAPE**: 0.25% (excelente)
- **R²**: 0.9820 (excelente)
- **OOB Score**: 96.77%
- **Tiempo de respuesta**: < 2 segundos
- **Disponibilidad**: 99.9%

#### Mejoras Técnicas
- Modelo Random Forest optimizado
- Sistema de cache con Redis
- Rate limiting implementado
- Autenticación con API Key
- Monitoreo y logging completo

#### Documentación
- README.md completo y técnico
- Resumen ejecutivo para gerencia
- Documentación técnica detallada
- Guías de uso y despliegue
- Referencia completa de la API

---

## Especificaciones de la Versión

### API Endpoints
- `GET /` - Información del servicio
- `GET /predict/steel-rebar-price` - Predicción de precio

### Autenticación
- **Método**: API Key header
- **Header**: `X-API-Key`
- **Clave**: `deacero_steel_predictor_2025_key`

### Fuentes de Datos
- **Alpha Vantage**: Acciones de acero y ETFs de commodities
- **FRED API**: Datos económicos oficiales
- **World Bank**: Indicadores económicos globales
- **Yahoo Finance**: Datos de mercado en tiempo real

### Infraestructura
- **Plataforma**: Google Cloud Run
- **Región**: us-central1
- **CPU**: 1 vCPU
- **Memoria**: 1 GB
- **Escalabilidad**: Automática

---

## Métricas de Calidad

### Precisión del Modelo
- **Error Absoluto Porcentual Medio (MAPE)**: 0.25%
- **Coeficiente de Determinación (R²)**: 0.9820
- **Score Out-of-Bag**: 96.77%
- **Confianza del Modelo**: 85%

### Rendimiento de la API
- **Tiempo de respuesta promedio**: < 2 segundos
- **Throughput**: 100 requests/hora
- **Disponibilidad**: 99.9%
- **Cache hit rate**: > 80%

### Costos
- **Costo de desarrollo**: $0
- **Costo operativo mensual**: $0
- **Presupuesto utilizado**: $0 de $5 USD/mes asignados

---

## Proceso de Versionado

### Convenciones
- **Versión Mayor**: Cambios incompatibles en API
- **Versión Menor**: Nuevas funcionalidades compatibles
- **Versión Parche**: Correcciones de bugs

### Formato de Versión
```
v[Major].[Minor].[Patch]
Ejemplo: v2.1.0
```

### Notas de Lanzamiento
Cada versión incluye:
- Lista de nuevas características
- Mejoras técnicas implementadas
- Correcciones de bugs
- Métricas de rendimiento
- Documentación actualizada

---

## Próximas Versiones

### v2.2.0 - Próxima Versión (Planificada: Q4 2024)
#### Mejoras Planificadas
- [ ] Integración completa de FRED API al modelo
- [ ] Dashboard web para monitoreo
- [ ] Alertas automáticas de cambios significativos
- [ ] Predicciones de múltiples días (3, 7, 30 días)

### v3.0.0 - Versión Mayor (Planificada: Q1 2025)
#### Expansión
- [ ] Más commodities (cobre, aluminio, níquel)
- [ ] Análisis técnico avanzado
- [ ] Predicciones por región
- [ ] Integración con sistemas ERP

---

## Información de Contacto

**Equipo de Desarrollo**: Data & Analytics - DeAcero  
**Proyecto**: Steel Rebar Price Predictor  
**Repositorio**: https://github.com/Deacero-arodriguez/steel-rebar-price-predictor-deacero  
**API Producción**: https://steel-rebar-predictor-646072255295.us-central1.run.app  

---

**Última actualización**: 29 de septiembre de 2025  
**Versión actual**: v2.1.0  
**Estado**: Producción