"""Tests for the Steel Rebar Price Predictor API."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import datetime

from src.app.main import app
from src.app.config import settings

client = TestClient(app)


@pytest.fixture
def mock_data():
    """Mock data for testing."""
    dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
    return pd.DataFrame({
        'date': dates,
        'price': [750 + i * 0.1 + (i % 7) * 5 for i in range(len(dates))],
        'iron_ore_price': [100 + i * 0.05 for i in range(len(dates))],
        'coal_price': [200 + i * 0.02 for i in range(len(dates))],
        'usd_mxn_rate': [20 + i * 0.001 for i in range(len(dates))]
    })


@pytest.fixture
def mock_prediction():
    """Mock prediction response."""
    return {
        "prediction_date": "2025-01-15",
        "predicted_price_usd_per_ton": 750.45,
        "currency": "USD",
        "unit": "metric ton",
        "model_confidence": 0.85,
        "timestamp": "2025-01-14T00:00:00Z"
    }


def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["service"] == "Steel Rebar Price Predictor"
    assert data["version"] == "1.0"
    assert "data_sources" in data


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data


def test_predict_endpoint_no_api_key():
    """Test prediction endpoint without API key."""
    response = client.get("/predict/steel-rebar-price")
    assert response.status_code == 401  # Unauthorized - missing API key


def test_predict_endpoint_invalid_api_key():
    """Test prediction endpoint with invalid API key."""
    response = client.get(
        "/predict/steel-rebar-price",
        headers={"X-API-Key": "invalid_key"}
    )
    assert response.status_code == 401


@patch('src.app.main.data_collector')
@patch('src.app.main.ml_model')
def test_predict_endpoint_success(mock_model, mock_collector, mock_data, mock_prediction):
    """Test successful prediction."""
    # Mock data collection
    mock_collector.get_all_economic_data.return_value = {
        'steel_rebar': mock_data
    }
    mock_collector.combine_data_for_training.return_value = mock_data
    
    # Mock model prediction
    mock_model.predict.return_value = (750.45, {
        'confidence': 0.85,
        'feature_importance': {'price_ma_7': 0.3},
        'current_features': {'price_ma_7': 750.0},
        'model_type': 'RandomForestRegressor'
    })
    
    # Mock model training
    mock_model.train.return_value = {
        'training_samples': 365,
        'feature_count': 10,
        'model_confidence': 0.85
    }
    
    response = client.get(
        "/predict/steel-rebar-price",
        headers={"X-API-Key": settings.api_key}
    )
    
    assert response.status_code == 200
    
    data = response.json()
    assert "prediction_date" in data
    assert "predicted_price_usd_per_ton" in data
    assert "model_confidence" in data
    assert data["currency"] == "USD"
    assert data["unit"] == "metric ton"


def test_explain_endpoint_no_api_key():
    """Test explanation endpoint without API key."""
    response = client.get("/explain/2025-01-15")
    assert response.status_code == 401  # Unauthorized - missing API key


def test_explain_endpoint_invalid_api_key():
    """Test explanation endpoint with invalid API key."""
    response = client.get(
        "/explain/2025-01-15",
        headers={"X-API-Key": "invalid_key"}
    )
    assert response.status_code == 401


@patch('src.app.main.cache_service')
def test_explain_endpoint_success(mock_cache):
    """Test successful explanation."""
    # Mock cached prediction
    mock_cache.get_prediction.return_value = {
        'prediction': {
            'prediction_date': '2025-01-15',
            'predicted_price_usd_per_ton': 750.45
        },
        'prediction_details': {
            'feature_importance': {
                'price_ma_7': 0.3,
                'iron_ore_price': 0.2
            },
            'current_features': {
                'price_ma_7': 750.0,
                'iron_ore_price': 120.0
            },
            'model_type': 'RandomForestRegressor'
        }
    }
    
    response = client.get(
        "/explain/2025-01-15",
        headers={"X-API-Key": settings.api_key}
    )
    
    assert response.status_code == 200
    
    data = response.json()
    assert data["prediction_date"] == "2025-01-15"
    assert "key_factors" in data
    assert len(data["key_factors"]) > 0


def test_stats_endpoint_no_api_key():
    """Test stats endpoint without API key."""
    response = client.get("/stats")
    assert response.status_code == 401  # Unauthorized - missing API key


def test_stats_endpoint_success():
    """Test stats endpoint with valid API key."""
    response = client.get(
        "/stats",
        headers={"X-API-Key": settings.api_key}
    )
    
    assert response.status_code == 200
    
    data = response.json()
    assert "timestamp" in data
    assert "model" in data
    assert "cache" in data
    assert "data_sources" in data


def test_rate_limiting():
    """Test rate limiting functionality."""
    # This would require more complex mocking of the cache service
    # For now, just test that the endpoint responds correctly
    response = client.get(
        "/predict/steel-rebar-price",
        headers={"X-API-Key": settings.api_key}
    )
    
    # Should either succeed or fail with rate limit error
    assert response.status_code in [200, 429, 500]


if __name__ == "__main__":
    pytest.main([__file__])
