"""Main FastAPI application for Steel Rebar Price Predictor."""

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
import logging
import asyncio
from typing import Optional

from app.config import settings
from app.models.schemas import (
    PredictionResponse, 
    ServiceInfoResponse, 
    ErrorResponse,
    ModelExplanationResponse
)
from app.services.data_collector import DataCollector
from app.services.cache_service import CacheService
from app.models.ml_model import SteelRebarPredictor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Steel Rebar Price Predictor",
    description="API for predicting steel rebar prices using machine learning",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
data_collector = DataCollector()
cache_service = CacheService(settings.redis_url)
ml_model = SteelRebarPredictor()

# Global variables
last_model_update = None
model_training_in_progress = False


def verify_api_key(x_api_key: str = Header(None)) -> str:
    """Verify API key."""
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key required")
    
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    # Check rate limit
    if not cache_service.increment_rate_limit(x_api_key, settings.rate_limit):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    return x_api_key


async def get_cached_prediction() -> Optional[PredictionResponse]:
    """Get cached prediction if available and not expired."""
    cached_data = cache_service.get_prediction()
    
    if cached_data:
        # Check if cache is still valid (less than 1 hour old)
        cached_at = datetime.fromisoformat(cached_data['cached_at'])
        if datetime.now() - cached_at < timedelta(seconds=settings.cache_ttl):
            logger.info("Returning cached prediction")
            return PredictionResponse(**cached_data['prediction'])
    
    return None


async def train_model_if_needed():
    """Train the model if it's outdated or doesn't exist."""
    global last_model_update, model_training_in_progress
    
    if model_training_in_progress:
        logger.info("Model training already in progress")
        return
    
    # Check if model needs retraining
    if last_model_update is None or \
       datetime.now() - last_model_update > timedelta(hours=settings.model_update_frequency):
        
        model_training_in_progress = True
        try:
            logger.info("Starting model training...")
            
            # Check cache first
            training_data = cache_service.get_training_data()
            
            if training_data is None:
                # Collect new data
                logger.info("Collecting fresh data for training...")
                economic_data = data_collector.get_all_economic_data()
                training_data = data_collector.combine_data_for_training(economic_data)
                
                # Cache the training data
                cache_service.set_training_data(training_data, ttl=86400)  # 24 hours
            
            if training_data.empty:
                raise ValueError("No training data available")
            
            # Train the model
            training_result = ml_model.train(training_data)
            last_model_update = datetime.now()
            
            logger.info(f"Model training completed: {training_result}")
            
        except Exception as e:
            logger.error(f"Model training failed: {e}")
            raise HTTPException(status_code=500, detail=f"Model training failed: {str(e)}")
        finally:
            model_training_in_progress = False


@app.get("/", response_model=ServiceInfoResponse)
async def root():
    """Get service information."""
    return ServiceInfoResponse(
        service="Steel Rebar Price Predictor",
        version="1.0",
        documentation_url="https://github.com/your-repo/steel-rebar-predictor",
        data_sources=settings.data_sources,
        last_model_update=last_model_update.isoformat() if last_model_update else "Never"
    )


@app.get("/predict/steel-rebar-price", response_model=PredictionResponse)
async def predict_steel_rebar_price(api_key: str = Depends(verify_api_key)):
    """Predict steel rebar price for the next day."""
    
    try:
        # Check for cached prediction first
        cached_prediction = await get_cached_prediction()
        if cached_prediction:
            return cached_prediction
        
        # Ensure model is trained
        await train_model_if_needed()
        
        # Collect latest data for prediction
        logger.info("Collecting latest data for prediction...")
        economic_data = data_collector.get_all_economic_data()
        latest_data = data_collector.combine_data_for_training(economic_data)
        
        if latest_data.empty:
            raise HTTPException(status_code=503, detail="No data available for prediction")
        
        # Make prediction
        prediction, prediction_details = ml_model.predict(latest_data)
        
        # Calculate next day's date
        next_day = datetime.now() + timedelta(days=1)
        
        # Create response
        response_data = {
            "prediction_date": next_day.strftime("%Y-%m-%d"),
            "predicted_price_usd_per_ton": round(prediction, 2),
            "currency": "USD",
            "unit": "metric ton",
            "model_confidence": round(prediction_details['confidence'], 3),
            "timestamp": datetime.now().isoformat() + "Z"
        }
        
        prediction_response = PredictionResponse(**response_data)
        
        # Cache the prediction
        cache_data = {
            'prediction': response_data,
            'prediction_details': prediction_details
        }
        cache_service.set_prediction(cache_data, settings.cache_ttl)
        
        logger.info(f"Prediction made: ${prediction:.2f} USD/ton")
        return prediction_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.get("/explain/{prediction_date}", response_model=ModelExplanationResponse)
async def explain_prediction(prediction_date: str, api_key: str = Depends(verify_api_key)):
    """Explain the factors influencing a prediction."""
    
    try:
        # Get cached prediction details
        cached_data = cache_service.get_prediction()
        
        if not cached_data or cached_data.get('prediction', {}).get('prediction_date') != prediction_date:
            raise HTTPException(status_code=404, detail="Prediction not found or expired")
        
        prediction_details = cached_data.get('prediction_details', {})
        feature_importance = prediction_details.get('feature_importance', {})
        current_features = prediction_details.get('current_features', {})
        
        # Create key factors list
        key_factors = []
        for feature, importance in sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:5]:
            key_factors.append({
                'factor': feature,
                'importance': round(importance, 4),
                'current_value': round(current_features.get(feature, 0), 4)
            })
        
        return ModelExplanationResponse(
            prediction_date=prediction_date,
            predicted_price=prediction_details.get('prediction', 0),
            key_factors=key_factors,
            model_type=prediction_details.get('model_type', 'Unknown'),
            timestamp=datetime.now().isoformat() + "Z"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Explanation error: {e}")
        raise HTTPException(status_code=500, detail=f"Explanation failed: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Check cache connection
        cache_stats = cache_service.get_cache_stats()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat() + "Z",
            "cache": cache_stats,
            "model_trained": last_model_update is not None,
            "last_model_update": last_model_update.isoformat() if last_model_update else None
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "timestamp": datetime.now().isoformat() + "Z",
                "error": str(e)
            }
        )


@app.get("/stats")
async def get_stats(api_key: str = Depends(verify_api_key)):
    """Get API statistics."""
    try:
        cache_stats = cache_service.get_cache_stats()
        
        return {
            "timestamp": datetime.now().isoformat() + "Z",
            "model": {
                "last_training": last_model_update.isoformat() if last_model_update else None,
                "training_in_progress": model_training_in_progress,
                "confidence": ml_model.model_confidence if hasattr(ml_model, 'model_confidence') else None
            },
            "cache": cache_stats,
            "data_sources": settings.data_sources
        }
    except Exception as e:
        logger.error(f"Stats error: {e}")
        raise HTTPException(status_code=500, detail=f"Stats failed: {str(e)}")


@app.on_event("startup")
async def startup_event():
    """Initialize the application on startup."""
    logger.info("Starting Steel Rebar Price Predictor API...")
    
    # Try to load existing model
    try:
        ml_model.load_model("model.joblib")
        global last_model_update
        last_model_update = ml_model.last_training_date
        logger.info("Loaded existing model")
    except FileNotFoundError:
        logger.info("No existing model found, will train on first request")
    except Exception as e:
        logger.warning(f"Failed to load existing model: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down Steel Rebar Price Predictor API...")
    
    # Save model if trained
    if hasattr(ml_model, 'model') and ml_model.model is not None:
        try:
            ml_model.save_model("model.joblib")
            logger.info("Model saved successfully")
        except Exception as e:
            logger.error(f"Failed to save model: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
