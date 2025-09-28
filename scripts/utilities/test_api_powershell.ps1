# Test de API con PowerShell
Write-Host "🚀 Probando API de Steel Rebar Price Predictor" -ForegroundColor Green
Write-Host "=" * 60

# URL de la API
$apiUrl = "https://steel-rebar-predictor-646072255295.us-central1.run.app"
$apiKey = "deacero_steel_predictor_2025_key"

# Headers
$headers = @{
    "X-API-Key" = $apiKey
    "Content-Type" = "application/json"
}

Write-Host "📍 URL: $apiUrl" -ForegroundColor Yellow
Write-Host "🔑 API Key: $apiKey" -ForegroundColor Yellow
Write-Host ""

# Test 1: Health Check
Write-Host "🏥 Probando Health Check..." -ForegroundColor Cyan
try {
    $healthResponse = Invoke-RestMethod -Uri "$apiUrl/health" -Method Get
    Write-Host "✅ Health Check exitoso" -ForegroundColor Green
    Write-Host "   Status: $($healthResponse.status)" -ForegroundColor White
    Write-Host "   Model Confidence: $($healthResponse.model_confidence)" -ForegroundColor White
    Write-Host "   Environment: $($healthResponse.environment)" -ForegroundColor White
} catch {
    Write-Host "❌ Health Check falló: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 2: Service Info
Write-Host "ℹ️ Probando Service Info..." -ForegroundColor Cyan
try {
    $serviceResponse = Invoke-RestMethod -Uri "$apiUrl/" -Method Get
    Write-Host "✅ Service Info exitoso" -ForegroundColor Green
    Write-Host "   Service: $($serviceResponse.service)" -ForegroundColor White
    Write-Host "   Version: $($serviceResponse.version)" -ForegroundColor White
    Write-Host "   Data Sources: $($serviceResponse.data_sources.Count) fuentes" -ForegroundColor White
} catch {
    Write-Host "❌ Service Info falló: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 3: Predicción con API Key
Write-Host "🎯 Probando Predicción..." -ForegroundColor Cyan
try {
    $predictionResponse = Invoke-RestMethod -Uri "$apiUrl/predict/steel-rebar-price" -Method Get -Headers $headers
    Write-Host "✅ Predicción exitosa" -ForegroundColor Green
    Write-Host "   Fecha: $($predictionResponse.prediction_date)" -ForegroundColor White
    Write-Host "   Precio USD/ton: `$$($predictionResponse.predicted_price_usd_per_ton)" -ForegroundColor White
    Write-Host "   Moneda: $($predictionResponse.currency)" -ForegroundColor White
    Write-Host "   Unidad: $($predictionResponse.unit)" -ForegroundColor White
    Write-Host "   Confianza: $($predictionResponse.model_confidence * 100)%" -ForegroundColor White
    Write-Host "   Timestamp: $($predictionResponse.timestamp)" -ForegroundColor White
    
    # Verificar si hay componentes de confianza dinámica
    if ($predictionResponse.PSObject.Properties.Name -contains "confidence_components") {
        Write-Host "   🎯 Confianza Dinámica Detectada:" -ForegroundColor Magenta
        $predictionResponse.confidence_components | ForEach-Object {
            $_.PSObject.Properties | ForEach-Object {
                Write-Host "     $($_.Name): $([math]::Round($_.Value * 100, 1))%" -ForegroundColor Magenta
            }
        }
    }
    
    # Verificar si hay intervalo de predicción
    if ($predictionResponse.PSObject.Properties.Name -contains "prediction_interval") {
        Write-Host "   📊 Intervalo de Predicción:" -ForegroundColor Magenta
        Write-Host "     Límite inferior: `$$($predictionResponse.prediction_interval.lower_bound)" -ForegroundColor Magenta
        Write-Host "     Límite superior: `$$($predictionResponse.prediction_interval.upper_bound)" -ForegroundColor Magenta
        Write-Host "     Ancho: `$$($predictionResponse.prediction_interval.width)" -ForegroundColor Magenta
    }
    
} catch {
    Write-Host "❌ Predicción falló: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 4: Sin API Key (debería fallar)
Write-Host "🔒 Probando sin API Key..." -ForegroundColor Cyan
try {
    $noKeyResponse = Invoke-RestMethod -Uri "$apiUrl/predict/steel-rebar-price" -Method Get
    Write-Host "❌ Error: Debería haber fallado sin API key" -ForegroundColor Red
} catch {
    if ($_.Exception.Response.StatusCode -eq 401) {
        Write-Host "✅ Correcto: Sin API key retorna 401" -ForegroundColor Green
    } else {
        Write-Host "❌ Error inesperado: $($_.Exception.Message)" -ForegroundColor Red
    }
}
Write-Host ""

Write-Host "=" * 60
Write-Host "🎉 Test completado" -ForegroundColor Green
