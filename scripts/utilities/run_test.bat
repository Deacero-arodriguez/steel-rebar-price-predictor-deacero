@echo off
REM Script batch para ejecutar tests de API en GCP
REM Uso: run_test.bat [URL_DE_LA_API] o run_test.bat demo

echo.
echo ========================================
echo   TEST DE API EN GCP - Steel Rebar Predictor
echo ========================================
echo.

REM Verificar argumentos
if "%1"=="" (
    echo ❌ Error: Debes proporcionar una opcion
    echo.
    echo 📋 OPCIONES DISPONIBLES:
    echo   1. Demo: run_test.bat demo
    echo   2. Test real: run_test.bat https://tu-api-url.a.run.app
    echo   3. Deployment completo: run_test.bat deploy [PROJECT-ID]
    echo.
    pause
    exit /b 1
)

REM Navegar al directorio del script
cd /d "%~dp0"

REM Verificar que Python esté disponible
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no está instalado o no está en PATH
    echo    Instala Python desde: https://python.org
    pause
    exit /b 1
)

REM Procesar opciones
if "%1"=="demo" (
    echo 🎭 Ejecutando DEMO de test...
    echo    Esto simula el comportamiento real sin necesidad de API desplegada
    echo.
    python demo_test_gcp.py
) else if "%1"=="deploy" (
    if "%2"=="" (
        echo ❌ Error: Debes proporcionar el Project ID para deployment
        echo    Uso: run_test.bat deploy TU-PROJECT-ID
        pause
        exit /b 1
    )
    echo 🚀 Ejecutando deployment completo y test...
    echo    Project ID: %2
    echo.
    python deploy_and_test_gcp.py %2
) else (
    echo 🧪 Ejecutando test real de API...
    echo    URL: %1
    echo.
    python run_gcp_test.py %1
)

echo.
echo ========================================
echo   Test completado
echo ========================================
echo.
pause
