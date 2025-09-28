#!/usr/bin/env python3
"""
Configure Quandl API Key - Secure setup
"""

import os
import getpass

def configure_quandl_api():
    """Configure Quandl API key securely."""
    print("🔑 CONFIGURACIÓN DE QUANDL API KEY")
    print("=" * 50)
    
    print("📝 INSTRUCCIONES:")
    print("1. Ve a: https://data.nasdaq.com/")
    print("2. Inicia sesión en tu cuenta")
    print("3. Ve a tu perfil y copia tu API key")
    print("4. Plan gratuito: 50 requests/día")
    print("")
    
    # Get API key securely
    api_key = getpass.getpass("🔑 Ingresa tu Quandl API key: ").strip()
    
    if not api_key:
        print("❌ API key vacía, cancelando configuración")
        return False
    
    # Test the API key
    print("🧪 Probando API key...")
    
    try:
        import requests
        
        url = "https://data.nasdaq.com/api/v3/datasets/LBMA/GOLD.json"
        params = {
            'api_key': api_key,
            'limit': 1
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            print("✅ API key válida y funcionando")
            
            # Save to .env file
            env_file = ".env"
            
            # Read existing content
            existing_content = ""
            if os.path.exists(env_file):
                with open(env_file, 'r') as f:
                    existing_content = f.read()
            
            # Remove old QUANDL_API_KEY if exists
            lines = existing_content.split('\n')
            lines = [line for line in lines if not line.startswith('QUANDL_API_KEY')]
            
            # Add new API key
            lines.append(f"QUANDL_API_KEY={api_key}")
            
            # Write back to file
            with open(env_file, 'w') as f:
                f.write('\n'.join(lines))
            
            print("💾 API key guardada en .env")
            print("🔒 Archivo .env actualizado")
            
            return True
            
        else:
            print(f"❌ API key inválida: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando API key: {e}")
        return False

def main():
    """Main configuration function."""
    success = configure_quandl_api()
    
    if success:
        print("\n🎉 CONFIGURACIÓN COMPLETADA")
        print("✅ Quandl API key configurada correctamente")
        print("🚀 Puedes proceder con la recolección de datos")
    else:
        print("\n❌ CONFIGURACIÓN FALLIDA")
        print("📋 Revisa tu API key y vuelve a intentar")

if __name__ == "__main__":
    main()
