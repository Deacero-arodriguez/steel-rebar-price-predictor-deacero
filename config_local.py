# Configuración local para testing
import os

# Configurar variables de entorno para testing local
os.environ['API_KEY'] = 'deacero_steel_predictor_2025_key'
os.environ['REDIS_URL'] = 'redis://localhost:6379'
os.environ['YAHOO_FINANCE_ENABLED'] = 'true'
os.environ['MODEL_UPDATE_FREQUENCY'] = '24'
os.environ['CACHE_TTL'] = '3600'
os.environ['RATE_LIMIT'] = '100'

print("✅ Variables de entorno configuradas para testing local")
