# Steel Rebar Price Predictor - Makefile
# Comandos útiles para desarrollo y deployment

.PHONY: help install test train run deploy clean lint format

# Variables
PYTHON = python3
PIP = pip3
PROJECT_NAME = steel-rebar-predictor
API_KEY = deacero_steel_predictor_2025_key

help: ## Mostrar ayuda
	@echo "🏗️ Steel Rebar Price Predictor - Comandos disponibles:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Instalar dependencias
	@echo "📦 Instalando dependencias..."
	$(PIP) install -r requirements.txt
	@echo "✅ Dependencias instaladas"

install-dev: ## Instalar dependencias de desarrollo
	@echo "📦 Instalando dependencias de desarrollo..."
	$(PIP) install -r requirements.txt
	$(PIP) install pytest pytest-cov black flake8 mypy
	@echo "✅ Dependencias de desarrollo instaladas"

test: ## Ejecutar tests
	@echo "🧪 Ejecutando tests..."
	$(PYTHON) -m pytest tests/ -v --tb=short
	@echo "✅ Tests completados"

test-cov: ## Ejecutar tests con cobertura
	@echo "🧪 Ejecutando tests con cobertura..."
	$(PYTHON) -m pytest tests/ --cov=app --cov-report=html --cov-report=term
	@echo "✅ Tests con cobertura completados"

train: ## Entrenar el modelo
	@echo "🤖 Entrenando modelo..."
	$(PYTHON) train_model.py
	@echo "✅ Entrenamiento completado"

run: ## Ejecutar aplicación localmente
	@echo "🚀 Iniciando aplicación local..."
	$(PYTHON) run_local.py

run-dev: ## Ejecutar en modo desarrollo
	@echo "🚀 Iniciando en modo desarrollo..."
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

lint: ## Ejecutar linter
	@echo "🔍 Ejecutando linter..."
	flake8 app/ tests/ --max-line-length=100 --ignore=E203,W503
	@echo "✅ Linting completado"

format: ## Formatear código
	@echo "🎨 Formateando código..."
	black app/ tests/ --line-length=100
	@echo "✅ Formateo completado"

type-check: ## Verificar tipos
	@echo "🔍 Verificando tipos..."
	mypy app/ --ignore-missing-imports
	@echo "✅ Verificación de tipos completada"

build: ## Construir imagen Docker
	@echo "🐳 Construyendo imagen Docker..."
	docker build -t $(PROJECT_NAME):latest .
	@echo "✅ Imagen construida"

run-docker: ## Ejecutar en Docker
	@echo "🐳 Ejecutando en Docker..."
	docker run -p 8000:8000 --env-file .env $(PROJECT_NAME):latest

deploy: ## Desplegar a GCP
	@echo "☁️ Desplegando a GCP..."
	chmod +x deploy.sh
	./deploy.sh
	@echo "✅ Despliegue completado"

deploy-manual: ## Despliegue manual a GCP
	@echo "☁️ Despliegue manual a GCP..."
	gcloud builds submit --config cloudbuild.yaml .
	@echo "✅ Despliegue manual completado"

test-api: ## Probar API localmente
	@echo "🔍 Probando API localmente..."
	@echo "Health check:"
	curl -s http://localhost:8000/health | jq .
	@echo ""
	@echo "Predicción:"
	curl -s -H "X-API-Key: $(API_KEY)" http://localhost:8000/predict/steel-rebar-price | jq .

clean: ## Limpiar archivos temporales
	@echo "🧹 Limpiando archivos temporales..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -f *.log
	rm -f training_data.csv
	rm -f model.joblib
	@echo "✅ Limpieza completada"

setup-env: ## Configurar entorno de desarrollo
	@echo "⚙️ Configurando entorno de desarrollo..."
	$(PYTHON) -m venv venv
	@echo "✅ Entorno virtual creado"
	@echo "💡 Ejecuta: source venv/bin/activate (Linux/Mac) o venv\\Scripts\\activate (Windows)"

check-requirements: ## Verificar requerimientos del sistema
	@echo "🔍 Verificando requerimientos del sistema..."
	@command -v $(PYTHON) >/dev/null 2>&1 || { echo "❌ Python no encontrado"; exit 1; }
	@command -v $(PIP) >/dev/null 2>&1 || { echo "❌ pip no encontrado"; exit 1; }
	@command -v docker >/dev/null 2>&1 || { echo "⚠️ Docker no encontrado (opcional)"; }
	@command -v gcloud >/dev/null 2>&1 || { echo "⚠️ gcloud no encontrado (opcional para deployment)"; }
	@echo "✅ Requerimientos verificados"

full-test: ## Ejecutar suite completa de tests
	@echo "🧪 Ejecutando suite completa de tests..."
	$(MAKE) lint
	$(MAKE) type-check
	$(MAKE) test-cov
	@echo "✅ Suite completa de tests completada"

docker-compose-up: ## Ejecutar con Docker Compose (si está disponible)
	@echo "🐳 Ejecutando con Docker Compose..."
	docker-compose up --build
	@echo "✅ Docker Compose completado"

docker-compose-down: ## Detener Docker Compose
	@echo "🐳 Deteniendo Docker Compose..."
	docker-compose down
	@echo "✅ Docker Compose detenido"

# Comandos de desarrollo
dev-install: setup-env install-dev ## Configurar entorno de desarrollo completo
dev-run: run-dev ## Ejecutar en modo desarrollo
dev-test: full-test ## Ejecutar todos los tests de desarrollo

# Comandos de producción
prod-build: build ## Construir para producción
prod-deploy: deploy ## Desplegar a producción
prod-test: test-api ## Probar en producción
