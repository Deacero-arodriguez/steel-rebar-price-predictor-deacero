#!/usr/bin/env python3
"""
Configuración unificada de rutas para el proyecto reorganizado.
Importar este módulo al inicio de cualquier script para configurar las rutas correctamente.
"""

import sys
import os
from pathlib import Path

def setup_project_paths():
    """Configurar rutas del proyecto para imports y referencias de archivos."""
    
    # Obtener el directorio raíz del proyecto
    current_file = Path(__file__).resolve()
    
    # Buscar el directorio raíz (donde está el README.md)
    project_root = current_file.parent
    while project_root != project_root.parent:
        if (project_root / "README.md").exists():
            break
        project_root = project_root.parent
    
    # Agregar directorios principales al path
    sys.path.insert(0, str(project_root / "src"))
    sys.path.insert(0, str(project_root / "scripts" / "utilities"))
    sys.path.insert(0, str(project_root / "scripts" / "data_collection"))
    sys.path.insert(0, str(project_root / "scripts" / "model_training"))
    sys.path.insert(0, str(project_root / "scripts" / "predictions"))
    
    return project_root

# Configurar rutas automáticamente al importar
PROJECT_ROOT = setup_project_paths()

# Configurar rutas de datos
DATA_ROOT = PROJECT_ROOT / "data"
MODELS_PATH = DATA_ROOT / "models"
PREDICTIONS_PATH = DATA_ROOT / "predictions"
PROCESSED_DATA_PATH = DATA_ROOT / "processed"
RAW_DATA_PATH = DATA_ROOT / "raw"

def get_model_path(filename):
    """Obtener ruta completa de un archivo de modelo."""
    return str(MODELS_PATH / filename)

def get_prediction_path(filename):
    """Obtener ruta completa de un archivo de predicción."""
    return str(PREDICTIONS_PATH / filename)

def get_data_path(filename):
    """Obtener ruta completa de un archivo de datos procesados."""
    return str(PROCESSED_DATA_PATH / filename)

def get_raw_data_path(filename):
    """Obtener ruta completa de un archivo de datos sin procesar."""
    return str(RAW_DATA_PATH / filename)

# Configurar logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Configuración de rutas completada. Proyecto: {PROJECT_ROOT}")
