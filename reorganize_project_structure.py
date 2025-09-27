#!/usr/bin/env python3
"""
Script para reorganizar la estructura del proyecto.
Crea una estructura más profesional y organizada.
"""

import os
import shutil
from pathlib import Path

def create_directory_structure():
    """Crear la nueva estructura de directorios."""
    
    directories = [
        # Core application
        "src/app",
        "src/app/models",
        "src/app/services", 
        "src/app/utils",
        
        # Scripts organizados por propósito
        "scripts/data_collection",
        "scripts/model_training",
        "scripts/predictions",
        "scripts/utilities",
        
        # Documentación organizada
        "docs/api",
        "docs/technical",
        "docs/predictions",
        "docs/deployment",
        
        # Datos organizados
        "data/raw",
        "data/processed",
        "data/models",
        "data/predictions",
        
        # Tests organizados
        "tests/unit",
        "tests/integration",
        "tests/fixtures",
        
        # Configuración
        "config",
        
        # Deployment
        "deployment/docker",
        "deployment/cloud",
        
        # Notebooks para análisis
        "notebooks",
        
        # Assets estáticos
        "assets/images",
        "assets/examples"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Creado directorio: {directory}")

def move_files():
    """Mover archivos a sus ubicaciones apropiadas."""
    
    file_moves = {
        # Core application files
        "app/main.py": "src/app/main.py",
        "app/config.py": "src/app/config.py",
        "app/models/ml_model.py": "src/app/models/ml_model.py",
        "app/models/schemas.py": "src/app/models/schemas.py",
        "app/services/data_collector.py": "src/app/services/data_collector.py",
        "app/services/cache_service.py": "src/app/services/cache_service.py",
        "app/utils/data_processor.py": "src/app/utils/data_processor.py",
        
        # Data collection scripts
        "enhanced_data_collector.py": "scripts/data_collection/enhanced_data_collector.py",
        "enhanced_data_collector_v2.py": "scripts/data_collection/enhanced_data_collector_v2.py",
        
        # Model training scripts
        "train_model.py": "scripts/model_training/train_model.py",
        "train_model_with_new_sources.py": "scripts/model_training/train_model_with_new_sources.py",
        "enhanced_ml_model.py": "scripts/model_training/enhanced_ml_model.py",
        
        # Prediction scripts
        "predict_october_2025.py": "scripts/predictions/predict_october_2025.py",
        "predict_october_2025_detailed.py": "scripts/predictions/predict_october_2025_detailed.py",
        "predict_october_2025_with_dynamic_confidence.py": "scripts/predictions/predict_october_2025_with_dynamic_confidence.py",
        "predict_october_simple.py": "scripts/predictions/predict_october_simple.py",
        "predict_with_currency_analysis.py": "scripts/predictions/predict_with_currency_analysis.py",
        
        # Utility scripts
        "dynamic_confidence_calculator.py": "scripts/utilities/dynamic_confidence_calculator.py",
        "verify_api_format.py": "scripts/utilities/verify_api_format.py",
        "api_response_example.py": "scripts/utilities/api_response_example.py",
        
        # Enhanced API
        "enhanced_api_with_dynamic_confidence.py": "src/app/enhanced_api_with_dynamic_confidence.py",
        
        # Data files
        "enhanced_steel_data_v2.csv": "data/processed/enhanced_steel_data_v2.csv",
        "comprehensive_steel_rebar_model.pkl": "data/models/comprehensive_steel_rebar_model.pkl",
        "comprehensive_model_metadata.json": "data/models/comprehensive_model_metadata.json",
        
        # Prediction results
        "october_2025_prediction.json": "data/predictions/october_2025_prediction.json",
        "october_2025_prediction_with_currency.json": "data/predictions/october_2025_prediction_with_currency.json",
        "october_2025_prediction_with_dynamic_confidence.json": "data/predictions/october_2025_prediction_with_dynamic_confidence.json",
        "october_2025_detailed_analysis.json": "data/predictions/october_2025_detailed_analysis.json",
        "api_compliance_report.json": "data/predictions/api_compliance_report.json",
        
        # Documentation
        "README.md": "docs/README.md",
        "TECHNICAL_DOCUMENTATION.md": "docs/technical/TECHNICAL_DOCUMENTATION.md",
        "DATA_SOURCES_SUMMARY.md": "docs/technical/DATA_SOURCES_SUMMARY.md",
        "DEPLOYMENT_INSTRUCTIONS.md": "docs/deployment/DEPLOYMENT_INSTRUCTIONS.md",
        "PREDICCION_OCTUBRE_2025_RESUMEN.md": "docs/predictions/PREDICCION_OCTUBRE_2025_RESUMEN.md",
        "OCTUBRE_2025_CONFIANZA_DINAMICA_RESUMEN.md": "docs/predictions/OCTUBRE_2025_CONFIANZA_DINAMICA_RESUMEN.md",
        "PRUEBA_LOCAL.md": "docs/technical/PRUEBA_LOCAL.md",
        
        # Configuration
        "requirements.txt": "config/requirements.txt",
        "config_local.py": "config/config_local.py",
        
        # Docker and deployment
        "Dockerfile": "deployment/docker/Dockerfile",
        "docker-compose.yml": "deployment/docker/docker-compose.yml",
        "cloudbuild.yaml": "deployment/cloud/cloudbuild.yaml",
        "deploy.sh": "deployment/cloud/deploy.sh",
        ".gcloudignore": "deployment/cloud/.gcloudignore",
        
        # Tests
        "tests/test_api.py": "tests/integration/test_api.py",
        "test_app.py": "tests/unit/test_app.py",
        
        # Development scripts
        "demo.py": "scripts/utilities/demo.py",
        "run_local.py": "scripts/utilities/run_local.py",
        "run_simple.py": "scripts/utilities/run_simple.py",
        "simple_server.py": "scripts/utilities/simple_server.py",
        
        # Build files
        "Makefile": "scripts/utilities/Makefile"
    }
    
    for source, destination in file_moves.items():
        if os.path.exists(source):
            # Crear directorio de destino si no existe
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            
            # Mover archivo
            shutil.move(source, destination)
            print(f"✅ Movido: {source} → {destination}")
        else:
            print(f"⚠️ No encontrado: {source}")

def create_new_files():
    """Crear archivos nuevos para la estructura reorganizada."""
    
    # README principal
    main_readme = """# Steel Rebar Price Predictor API - Dynamic Confidence Edition

Un API REST de vanguardia para predecir precios de varilla corrugada utilizando machine learning comprehensivo con **sistema de confianza dinámica**.

## 📁 Estructura del Proyecto

```
steel-rebar-predictor/
├── src/                          # Código fuente principal
│   └── app/                      # Aplicación FastAPI
│       ├── models/               # Modelos de datos y ML
│       ├── services/             # Servicios de negocio
│       └── utils/                # Utilidades
├── scripts/                      # Scripts organizados por propósito
│   ├── data_collection/          # Recolección de datos
│   ├── model_training/           # Entrenamiento de modelos
│   ├── predictions/              # Scripts de predicción
│   └── utilities/                # Utilidades generales
├── docs/                         # Documentación
│   ├── api/                      # Documentación de API
│   ├── technical/                # Documentación técnica
│   ├── predictions/              # Análisis de predicciones
│   └── deployment/               # Guías de despliegue
├── data/                         # Datos organizados
│   ├── raw/                      # Datos sin procesar
│   ├── processed/                # Datos procesados
│   ├── models/                   # Modelos entrenados
│   └── predictions/              # Resultados de predicciones
├── tests/                        # Tests organizados
│   ├── unit/                     # Tests unitarios
│   ├── integration/              # Tests de integración
│   └── fixtures/                 # Datos de prueba
├── config/                       # Configuración
├── deployment/                   # Archivos de despliegue
│   ├── docker/                   # Configuración Docker
│   └── cloud/                    # Configuración cloud
├── notebooks/                    # Jupyter notebooks
├── assets/                       # Recursos estáticos
└── README.md                     # Este archivo
```

## 🚀 Inicio Rápido

### Desarrollo Local
```bash
# Instalar dependencias
pip install -r config/requirements.txt

# Ejecutar aplicación
python scripts/utilities/run_local.py

# Ejecutar tests
pytest tests/
```

### Despliegue
```bash
# Docker
docker-compose -f deployment/docker/docker-compose.yml up

# Google Cloud
bash deployment/cloud/deploy.sh
```

## 📊 Predicciones Disponibles

- **Octubre 2025**: Ver `docs/predictions/`
- **Análisis de confianza dinámica**: Ver `scripts/predictions/`
- **Documentación técnica**: Ver `docs/technical/`

## 🎯 Características Principales

- **Confianza dinámica**: 90.1% vs 85% estático
- **13 fuentes de datos** integradas
- **136 features** en el modelo
- **Intervalos de predicción** reales
- **Análisis USD/MXN** para DeAcero

---

**Desarrollado por**: Armando Rodriguez Rocha  
**Contacto**: [rr.armando@gmail.com]  
**Versión**: 2.1.0 - Dynamic Confidence Edition
"""
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(main_readme)
    
    # .gitignore actualizado
    gitignore = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
venv/
env/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Project specific
data/raw/*
!data/raw/.gitkeep
data/processed/*
!data/processed/.gitkeep
data/models/*.pkl
data/models/*.joblib
!data/models/.gitkeep
data/predictions/*.json
!data/predictions/.gitkeep

# Logs
*.log
logs/

# Environment variables
.env
.env.local
.env.production

# Temporary files
*.tmp
*.temp
temp/
tmp/

# Coverage reports
htmlcov/
.coverage
.coverage.*
coverage.xml

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# Docker
.dockerignore
"""
    
    with open(".gitignore", "w", encoding="utf-8") as f:
        f.write(gitignore)
    
    # Archivos .gitkeep para mantener directorios vacíos
    gitkeep_dirs = [
        "data/raw",
        "data/processed", 
        "data/models",
        "data/predictions",
        "notebooks",
        "assets/images",
        "assets/examples"
    ]
    
    for directory in gitkeep_dirs:
        gitkeep_path = os.path.join(directory, ".gitkeep")
        os.makedirs(directory, exist_ok=True)
        with open(gitkeep_path, "w") as f:
            f.write("# Este archivo mantiene el directorio en Git\n")
    
    print("✅ Archivos de estructura creados")

def main():
    """Función principal."""
    print("🔧 REORGANIZANDO ESTRUCTURA DEL PROYECTO")
    print("=" * 50)
    
    print("\n📁 Creando estructura de directorios...")
    create_directory_structure()
    
    print("\n📦 Moviendo archivos...")
    move_files()
    
    print("\n📝 Creando archivos de estructura...")
    create_new_files()
    
    print("\n✅ REORGANIZACIÓN COMPLETADA")
    print("=" * 50)
    print("📋 Estructura mejorada:")
    print("   ✅ Código fuente organizado en src/")
    print("   ✅ Scripts categorizados por propósito")
    print("   ✅ Documentación estructurada")
    print("   ✅ Datos organizados por tipo")
    print("   ✅ Tests organizados")
    print("   ✅ Configuración centralizada")
    print("   ✅ Despliegue separado")
    
    print("\n🎯 Beneficios:")
    print("   ✅ Mejor mantenibilidad")
    print("   ✅ Estructura profesional")
    print("   ✅ Fácil navegación")
    print("   ✅ Separación de responsabilidades")
    print("   ✅ Escalabilidad mejorada")

if __name__ == "__main__":
    main()
