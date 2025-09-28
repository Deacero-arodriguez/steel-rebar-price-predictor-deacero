# Simple API Test
Write-Host "Testing Steel Rebar Price Predictor API" -ForegroundColor Green

$apiUrl = "https://steel-rebar-predictor-646072255295.us-central1.run.app"
$apiKey = "deacero_steel_predictor_2025_key"

# Test Health Check
Write-Host "Testing Health Check..." -ForegroundColor Yellow
try {
    $healthResponse = Invoke-RestMethod -Uri "$apiUrl/health" -Method Get
    Write-Host "Health Check: SUCCESS" -ForegroundColor Green
    Write-Host "Status: $($healthResponse.status)"
    Write-Host "Model Confidence: $($healthResponse.model_confidence)"
} catch {
    Write-Host "Health Check: FAILED" -ForegroundColor Red
}

Write-Host ""

# Test Prediction
Write-Host "Testing Prediction..." -ForegroundColor Yellow
try {
    $headers = @{"X-API-Key" = $apiKey}
    $predictionResponse = Invoke-RestMethod -Uri "$apiUrl/predict/steel-rebar-price" -Method Get -Headers $headers
    Write-Host "Prediction: SUCCESS" -ForegroundColor Green
    Write-Host "Date: $($predictionResponse.prediction_date)"
    Write-Host "Price USD/ton: `$$($predictionResponse.predicted_price_usd_per_ton)"
    Write-Host "Currency: $($predictionResponse.currency)"
    Write-Host "Unit: $($predictionResponse.unit)"
    Write-Host "Confidence: $($predictionResponse.model_confidence)"
    Write-Host "Timestamp: $($predictionResponse.timestamp)"
} catch {
    Write-Host "Prediction: FAILED" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)"
}

Write-Host ""
Write-Host "Test completed!" -ForegroundColor Green
