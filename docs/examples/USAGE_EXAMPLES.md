# 🚀 **EJEMPLOS DE USO - API Steel Rebar Predictor**
## DeAcero - Guía Práctica de Integración

> **Ejemplos reales de uso de la API con tu URL desplegada**

---

## 🎯 **INFORMACIÓN DE TU API**

### **URL de Producción**
```
https://steel-rebar-predictor-646072255295.us-central1.run.app
```

### **Estado Actual**
- ✅ **API Activa**: Funcionando en producción
- ✅ **Versión**: 2.1.0
- ✅ **Última actualización**: 2025-09-28T21:41:10.655871Z

---

## 🔗 **ENDPOINTS DISPONIBLES**

### **1. 🏠 Información del Servicio**
```http
GET https://steel-rebar-predictor-646072255295.us-central1.run.app/
```

### **2. 🔮 Predicción de Precios**
```http
GET https://steel-rebar-predictor-646072255295.us-central1.run.app/predict/steel-rebar-price
Headers: X-API-Key: your-api-key
```

---

## 🧪 **EJEMPLOS PRÁCTICOS**

### **1. 📋 Verificar Estado del Servicio**

#### **cURL**
```bash
curl -X GET "https://steel-rebar-predictor-646072255295.us-central1.run.app/"
```

#### **Respuesta Esperada**
```json
{
  "service": "Steel Rebar Price Predictor",
  "version": "2.1.0",
  "documentation_url": "https://github.com/Deacero-arodriguez/steel-rebar-price-predictor-deacero",
  "data_sources": [
    "Yahoo Finance",
    "Alpha Vantage",
    "FRED (Federal Reserve Economic Data)",
    "Trading Economics"
  ],
  "last_model_update": "2025-09-28T21:41:10.655871Z"
}
```

### **2. 🔮 Obtener Predicción de Precios**

#### **cURL**
```bash
curl -X GET \
  "https://steel-rebar-predictor-646072255295.us-central1.run.app/predict/steel-rebar-price" \
  -H "X-API-Key: your-api-key-here"
```

#### **Respuesta Esperada**
```json
{
  "prediction_date": "2025-01-29",
  "predicted_price_usd_per_ton": 750.45,
  "currency": "USD",
  "unit": "metric ton",
  "model_confidence": 0.85,
  "timestamp": "2025-01-28T23:59:59Z"
}
```

---

## 🐍 **INTEGRACIÓN EN PYTHON**

### **Script Básico**
```python
import requests
import json
from datetime import datetime

class SteelRebarAPI:
    def __init__(self, api_key):
        self.base_url = "https://steel-rebar-predictor-646072255295.us-central1.run.app"
        self.headers = {"X-API-Key": api_key}
    
    def get_service_info(self):
        """Obtener información del servicio."""
        response = requests.get(f"{self.base_url}/", headers=self.headers)
        return response.json()
    
    def get_price_prediction(self):
        """Obtener predicción de precio de varilla."""
        response = requests.get(
            f"{self.base_url}/predict/steel-rebar-price", 
            headers=self.headers
        )
        return response.json()

# Uso del API
api = SteelRebarAPI("your-api-key-here")

# Verificar estado
service_info = api.get_service_info()
print(f"Servicio: {service_info['service']}")
print(f"Versión: {service_info['version']}")
print(f"Fuentes de datos: {len(service_info['data_sources'])}")

# Obtener predicción
prediction = api.get_price_prediction()
print(f"Precio predicho: ${prediction['predicted_price_usd_per_ton']}/ton")
print(f"Confianza: {prediction['model_confidence']*100:.1f}%")
```

### **Script Avanzado con Manejo de Errores**
```python
import requests
import time
from typing import Optional, Dict

class SteelRebarAPIClient:
    def __init__(self, api_key: str):
        self.base_url = "https://steel-rebar-predictor-646072255295.us-central1.run.app"
        self.headers = {"X-API-Key": api_key}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def _make_request(self, endpoint: str, max_retries: int = 3) -> Optional[Dict]:
        """Hacer request con reintentos automáticos."""
        for attempt in range(max_retries):
            try:
                response = self.session.get(f"{self.base_url}{endpoint}", timeout=10)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                print(f"Intento {attempt + 1} falló: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Backoff exponencial
                else:
                    raise e
        return None
    
    def get_service_status(self) -> Dict:
        """Obtener estado del servicio."""
        return self._make_request("/")
    
    def get_price_prediction(self) -> Dict:
        """Obtener predicción de precio."""
        return self._make_request("/predict/steel-rebar-price")
    
    def monitor_prices(self, interval_minutes: int = 60):
        """Monitorear precios continuamente."""
        while True:
            try:
                prediction = self.get_price_prediction()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                price = prediction['predicted_price_usd_per_ton']
                confidence = prediction['model_confidence']
                
                print(f"[{timestamp}] Precio: ${price:.2f}/ton | Confianza: {confidence*100:.1f}%")
                
                # Alertas personalizadas
                if price > 800:
                    print("🚨 ALERTA: Precio alto detectado")
                elif price < 700:
                    print("📉 ALERTA: Precio bajo detectado")
                
            except Exception as e:
                print(f"Error en monitoreo: {e}")
            
            time.sleep(interval_minutes * 60)

# Uso avanzado
client = SteelRebarAPIClient("your-api-key-here")

# Verificar estado
status = client.get_service_status()
print(f"Estado del servicio: {status['service']} v{status['version']}")

# Obtener predicción
prediction = client.get_price_prediction()
print(f"Precio predicho: ${prediction['predicted_price_usd_per_ton']}/ton")

# Monitoreo continuo (opcional)
# client.monitor_prices(interval_minutes=60)
```

---

## 🌐 **INTEGRACIÓN EN JAVASCRIPT**

### **Cliente JavaScript**
```javascript
class SteelRebarAPIClient {
    constructor(apiKey) {
        this.baseUrl = 'https://steel-rebar-predictor-646072255295.us-central1.run.app';
        this.headers = {
            'X-API-Key': apiKey,
            'Content-Type': 'application/json'
        };
    }
    
    async makeRequest(endpoint) {
        try {
            const response = await fetch(`${this.baseUrl}${endpoint}`, {
                headers: this.headers,
                method: 'GET'
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }
    
    async getServiceInfo() {
        return await this.makeRequest('/');
    }
    
    async getPricePrediction() {
        return await this.makeRequest('/predict/steel-rebar-price');
    }
    
    async startPriceMonitoring(intervalMs = 60000) {
        const monitor = async () => {
            try {
                const prediction = await this.getPricePrediction();
                const timestamp = new Date().toLocaleString();
                const price = prediction.predicted_price_usd_per_ton;
                const confidence = prediction.model_confidence;
                
                console.log(`[${timestamp}] Precio: $${price.toFixed(2)}/ton | Confianza: ${(confidence * 100).toFixed(1)}%`);
                
                // Alertas
                if (price > 800) {
                    console.warn('🚨 ALERTA: Precio alto detectado');
                } else if (price < 700) {
                    console.warn('📉 ALERTA: Precio bajo detectado');
                }
                
            } catch (error) {
                console.error('Error en monitoreo:', error);
            }
        };
        
        // Ejecutar inmediatamente
        await monitor();
        
        // Configurar intervalo
        return setInterval(monitor, intervalMs);
    }
}

// Uso del cliente
const client = new SteelRebarAPIClient('your-api-key-here');

// Verificar estado
client.getServiceInfo()
    .then(info => {
        console.log(`Servicio: ${info.service} v${info.version}`);
        console.log(`Fuentes: ${info.data_sources.join(', ')}`);
    })
    .catch(error => console.error('Error:', error));

// Obtener predicción
client.getPricePrediction()
    .then(prediction => {
        console.log(`Precio predicho: $${prediction.predicted_price_usd_per_ton}/ton`);
        console.log(`Confianza: ${(prediction.model_confidence * 100).toFixed(1)}%`);
    })
    .catch(error => console.error('Error:', error));

// Monitoreo continuo
// client.startPriceMonitoring(60000); // Cada minuto
```

---

## 📊 **INTEGRACIÓN EN EXCEL/POWER BI**

### **Power Query (Excel)**
```m
let
    // Configuración
    BaseUrl = "https://steel-rebar-predictor-646072255295.us-central1.run.app",
    ApiKey = "your-api-key-here",
    
    // Headers
    Headers = [
        #"X-API-Key" = ApiKey,
        #"Content-Type" = "application/json"
    ],
    
    // Obtener información del servicio
    ServiceInfo = Json.Document(
        Web.Contents(
            BaseUrl,
            [Headers = Headers]
        )
    ),
    
    // Obtener predicción
    Prediction = Json.Document(
        Web.Contents(
            BaseUrl & "/predict/steel-rebar-price",
            [Headers = Headers]
        )
    ),
    
    // Crear tabla de resultados
    Result = Table.FromRecords({
        [
            Servicio = ServiceInfo[service],
            Version = ServiceInfo[version],
            Fecha_Prediccion = Prediction[prediction_date],
            Precio_Predicho = Prediction[predicted_price_usd_per_ton],
            Confianza = Prediction[model_confidence],
            Timestamp = Prediction[timestamp]
        ]
    })
in
    Result
```

---

## 🔧 **CONFIGURACIÓN DE MONITOREO**

### **Script de Monitoreo Automático**
```python
#!/usr/bin/env python3
"""
Script de monitoreo automático para la API de Steel Rebar Predictor
"""

import requests
import time
import logging
from datetime import datetime
from typing import Dict, Optional

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('steel_rebar_monitor.log'),
        logging.StreamHandler()
    ]
)

class APIMonitor:
    def __init__(self, api_key: str):
        self.base_url = "https://steel-rebar-predictor-646072255295.us-central1.run.app"
        self.headers = {"X-API-Key": api_key}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def check_health(self) -> bool:
        """Verificar salud del servicio."""
        try:
            response = self.session.get(f"{self.base_url}/", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logging.error(f"Health check failed: {e}")
            return False
    
    def get_prediction(self) -> Optional[Dict]:
        """Obtener predicción de precio."""
        try:
            response = self.session.get(
                f"{self.base_url}/predict/steel-rebar-price",
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"Prediction failed: {e}")
            return None
    
    def monitor(self, interval_seconds: int = 3600):
        """Monitoreo continuo."""
        logging.info("Iniciando monitoreo de la API...")
        
        while True:
            try:
                # Verificar salud
                if not self.check_health():
                    logging.error("❌ Servicio no disponible")
                    time.sleep(60)  # Reintentar en 1 minuto
                    continue
                
                # Obtener predicción
                prediction = self.get_prediction()
                if prediction:
                    price = prediction['predicted_price_usd_per_ton']
                    confidence = prediction['model_confidence']
                    
                    logging.info(f"✅ Precio: ${price:.2f}/ton | Confianza: {confidence*100:.1f}%")
                    
                    # Alertas
                    if price > 800:
                        logging.warning(f"🚨 ALERTA: Precio alto ${price:.2f}/ton")
                    elif price < 700:
                        logging.warning(f"📉 ALERTA: Precio bajo ${price:.2f}/ton")
                
                # Esperar intervalo
                time.sleep(interval_seconds)
                
            except KeyboardInterrupt:
                logging.info("Monitoreo detenido por usuario")
                break
            except Exception as e:
                logging.error(f"Error en monitoreo: {e}")
                time.sleep(60)

if __name__ == "__main__":
    # Configurar API key
    API_KEY = "your-api-key-here"
    
    # Crear monitor
    monitor = APIMonitor(API_KEY)
    
    # Iniciar monitoreo (cada hora)
    monitor.monitor(interval_seconds=3600)
```

---

## 🚨 **MANEJO DE ERRORES**

### **Códigos de Error Comunes**

| Código | Error | Solución |
|--------|-------|----------|
| `401` | Unauthorized | Verificar API key |
| `429` | Rate limit exceeded | Esperar y reintentar |
| `500` | Internal server error | Contactar soporte |
| `503` | Service unavailable | Servicio en mantenimiento |

### **Ejemplo de Manejo de Errores**
```python
import requests
from typing import Optional, Dict

def safe_api_call(url: str, headers: Dict, max_retries: int = 3) -> Optional[Dict]:
    """Llamada segura a la API con manejo de errores."""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                raise ValueError("API key inválida")
            elif response.status_code == 429:
                wait_time = 2 ** attempt
                print(f"Rate limit alcanzado. Esperando {wait_time} segundos...")
                time.sleep(wait_time)
                continue
            elif response.status_code >= 500:
                print(f"Error del servidor: {response.status_code}")
                time.sleep(5)
                continue
            else:
                response.raise_for_status()
                
        except requests.exceptions.Timeout:
            print(f"Timeout en intento {attempt + 1}")
        except requests.exceptions.ConnectionError:
            print(f"Error de conexión en intento {attempt + 1}")
        except Exception as e:
            print(f"Error inesperado: {e}")
        
        if attempt < max_retries - 1:
            time.sleep(2 ** attempt)
    
    return None

# Uso
result = safe_api_call(
    "https://steel-rebar-predictor-646072255295.us-central1.run.app/predict/steel-rebar-price",
    {"X-API-Key": "your-api-key"}
)

if result:
    print(f"Precio: ${result['predicted_price_usd_per_ton']}/ton")
else:
    print("No se pudo obtener la predicción")
```

---

## 📞 **SOPORTE**

### **Contacto**
- **Email**: soporte-deacero@deacero.com
- **Documentación**: `/docs/api/API_REFERENCE.md`
- **Estado del servicio**: https://steel-rebar-predictor-646072255295.us-central1.run.app/

### **Recursos Adicionales**
- **GitHub**: https://github.com/Deacero-arodriguez/steel-rebar-price-predictor-deacero
- **Documentación técnica**: `/docs/model/MODEL_DOCUMENTATION.md`
- **Guía de despliegue**: `/docs/deployment/DEPLOYMENT_GUIDE.md`

---

**🎉 API LISTA PARA USO EN PRODUCCIÓN**

---

**Última actualización**: 29 de septiembre de 2025  
**Versión de la API**: 2.1.0  
**Estado**: ✅ Producción
