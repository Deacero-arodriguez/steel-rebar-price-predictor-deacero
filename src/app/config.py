"""Configuration settings for the Steel Rebar Price Predictor API."""

import os
from typing import List
try:
    from pydantic_settings import BaseSettings
    from pydantic import ConfigDict
except ImportError:
    from pydantic import BaseSettings, ConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    api_key: str = "deacero_steel_predictor_2025_key"
    redis_url: str = "redis://localhost:6379"
    
    # External APIs
    yahoo_finance_enabled: bool = True
    alpha_vantage_api_key: str = ""
    fred_api_key: str = ""
    
    # Model Configuration
    model_update_frequency: int = 24  # hours
    cache_ttl: int = 3600  # seconds (1 hour)
    rate_limit: int = 100  # requests per hour
    
    # GCP Configuration
    google_cloud_project: str = ""
    google_application_credentials: str = ""
    
    # Data Sources
    data_sources: List[str] = [
        "Yahoo Finance",
        "Alpha Vantage", 
        "FRED (Federal Reserve)",
        "Trading Economics"
    ]
    
    model_config = ConfigDict(env_file=".env")


settings = Settings()
