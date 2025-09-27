#!/usr/bin/env python3
"""
Servidor HTTP simple para probar la funcionalidad básica.
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

# API Key para testing
API_KEY = "deacero_steel_predictor_2025_key"

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Manejar requests GET."""
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "service": "Steel Rebar Price Predictor",
                "version": "1.0",
                "documentation_url": "http://localhost:8000/docs",
                "data_sources": ["Yahoo Finance", "Alpha Vantage", "FRED"],
                "last_model_update": datetime.now().isoformat(),
                "status": "running"
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        elif self.path == "/health":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "service": "steel-rebar-predictor",
                "version": "1.0"
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        elif self.path == "/test":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "message": "¡La aplicación está funcionando correctamente!",
                "timestamp": datetime.now().isoformat(),
                "python_version": "3.13.7",
                "fastapi_version": "0.117.1"
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        elif self.path == "/predict/steel-rebar-price":
            # Verificar API key
            api_key = self.headers.get('X-API-Key')
            
            if not api_key:
                self.send_response(401)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                response = {"error": "API key required"}
                self.wfile.write(json.dumps(response).encode())
                return
                
            if api_key != API_KEY:
                self.send_response(401)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                response = {"error": "Invalid API key"}
                self.wfile.write(json.dumps(response).encode())
                return
            
            # Predicción simulada
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            next_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            
            response = {
                "prediction_date": next_day.strftime("%Y-%m-%d"),
                "predicted_price_usd_per_ton": 750.45,
                "currency": "USD",
                "unit": "metric ton",
                "model_confidence": 0.85,
                "timestamp": datetime.now().isoformat() + "Z",
                "note": "Esta es una predicción simulada para testing"
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {"error": "Endpoint not found"}
            self.wfile.write(json.dumps(response).encode())

def run_server():
    """Ejecutar el servidor."""
    server_address = ('localhost', 8000)
    httpd = HTTPServer(server_address, SimpleHandler)
    
    print("🏗️ Steel Rebar Price Predictor - Servidor Simple")
    print("=" * 50)
    print("🚀 Iniciando servidor...")
    print("📍 URL: http://localhost:8000")
    print("🧪 Test endpoint: http://localhost:8000/test")
    print("🔑 API Key: deacero_steel_predictor_2025_key")
    print("⏹️ Presiona Ctrl+C para detener")
    print("-" * 50)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido")
        httpd.shutdown()

if __name__ == "__main__":
    run_server()
