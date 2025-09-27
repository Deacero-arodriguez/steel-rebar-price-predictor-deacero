"""Pydantic schemas for API request/response models."""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class PredictionResponse(BaseModel):
    """Response model for steel rebar price prediction."""
    
    prediction_date: str = Field(..., description="Date for the prediction (YYYY-MM-DD)")
    predicted_price_usd_per_ton: float = Field(..., description="Predicted price in USD per metric ton")
    currency: str = Field(default="USD", description="Currency of the prediction")
    unit: str = Field(default="metric ton", description="Unit of measurement")
    model_confidence: float = Field(..., ge=0.0, le=1.0, description="Model confidence score")
    timestamp: str = Field(..., description="ISO timestamp of the prediction")


class ServiceInfoResponse(BaseModel):
    """Response model for service information."""
    
    service: str = Field(default="Steel Rebar Price Predictor")
    version: str = Field(default="1.0")
    documentation_url: str = Field(default="https://github.com/your-repo/steel-rebar-predictor")
    data_sources: List[str] = Field(default=[], description="List of data sources used")
    last_model_update: str = Field(..., description="ISO timestamp of last model update")


class ErrorResponse(BaseModel):
    """Error response model."""
    
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    timestamp: str = Field(..., description="ISO timestamp of the error")


class ModelExplanationResponse(BaseModel):
    """Response model for model explanation."""
    
    prediction_date: str = Field(..., description="Date for the prediction")
    predicted_price: float = Field(..., description="Predicted price")
    key_factors: List[dict] = Field(..., description="Key factors influencing the prediction")
    model_type: str = Field(..., description="Type of model used")
    timestamp: str = Field(..., description="ISO timestamp")
