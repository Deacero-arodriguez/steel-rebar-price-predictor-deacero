"""Machine Learning model for steel rebar price prediction."""

import joblib
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_percentage_error
import logging

logger = logging.getLogger(__name__)


class SteelRebarPredictor:
    """Machine Learning model for predicting steel rebar prices."""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = []
        self.last_training_date = None
        self.model_confidence = 0.85
        
    def prepare_features(self, historical_data: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for the ML model."""
        
        df = historical_data.copy()
        
        # Basic price features
        df['price_ma_7'] = df['price'].rolling(window=7).mean()
        df['price_ma_14'] = df['price'].rolling(window=14).mean()
        df['price_ma_30'] = df['price'].rolling(window=30).mean()
        
        # Volatility features
        df['price_volatility_7'] = df['price'].rolling(window=7).std()
        df['price_volatility_14'] = df['price'].rolling(window=14).std()
        
        # Trend features
        df['price_change_1d'] = df['price'].pct_change(1)
        df['price_change_7d'] = df['price'].pct_change(7)
        df['price_change_30d'] = df['price'].pct_change(30)
        
        # Technical indicators
        df['rsi_14'] = self._calculate_rsi(df['price'], 14)
        df['bollinger_upper'] = df['price_ma_20'] + (2 * df['price_volatility_20'])
        df['bollinger_lower'] = df['price_ma_20'] - (2 * df['price_volatility_20'])
        df['bollinger_position'] = (df['price'] - df['bollinger_lower']) / (df['bollinger_upper'] - df['bollinger_lower'])
        
        # Seasonal features
        df['month'] = pd.to_datetime(df['date']).dt.month
        df['day_of_week'] = pd.to_datetime(df['date']).dt.dayofweek
        df['quarter'] = pd.to_datetime(df['date']).dt.quarter
        
        # Economic indicators (if available)
        if 'iron_ore_price' in df.columns:
            df['iron_ore_ma_7'] = df['iron_ore_price'].rolling(window=7).mean()
            df['iron_ore_change_7d'] = df['iron_ore_price'].pct_change(7)
            
        if 'coal_price' in df.columns:
            df['coal_ma_7'] = df['coal_price'].rolling(window=7).mean()
            df['coal_change_7d'] = df['coal_price'].pct_change(7)
            
        if 'usd_mxn_rate' in df.columns:
            df['usd_mxn_ma_7'] = df['usd_mxn_rate'].rolling(window=7).mean()
            df['usd_mxn_change_7d'] = df['usd_mxn_rate'].pct_change(7)
        
        # Drop rows with NaN values
        df = df.dropna()
        
        # Select features for training
        feature_columns = [
            'price_ma_7', 'price_ma_14', 'price_ma_30',
            'price_volatility_7', 'price_volatility_14',
            'price_change_1d', 'price_change_7d', 'price_change_30d',
            'rsi_14', 'bollinger_position',
            'month', 'day_of_week', 'quarter'
        ]
        
        # Add economic indicators if available
        if 'iron_ore_ma_7' in df.columns:
            feature_columns.extend(['iron_ore_ma_7', 'iron_ore_change_7d'])
        if 'coal_ma_7' in df.columns:
            feature_columns.extend(['coal_ma_7', 'coal_change_7d'])
        if 'usd_mxn_ma_7' in df.columns:
            feature_columns.extend(['usd_mxn_ma_7', 'usd_mxn_change_7d'])
        
        self.feature_names = feature_columns
        
        return df[['date'] + feature_columns + ['price']]
    
    def _calculate_rsi(self, prices: pd.Series, window: int = 14) -> pd.Series:
        """Calculate Relative Strength Index."""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def train(self, historical_data: pd.DataFrame) -> Dict:
        """Train the ML model."""
        
        logger.info("Starting model training...")
        
        # Prepare features
        df = self.prepare_features(historical_data)
        
        if len(df) < 30:
            raise ValueError("Insufficient data for training. Need at least 30 days of data.")
        
        # Split features and target
        X = df[self.feature_names].values
        y = df['price'].values
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model (using optimized Random Forest for production)
        self.model = RandomForestRegressor(
            n_estimators=150,      # Balanced profile: 150 trees
            max_depth=12,          # Balanced profile: depth 12
            min_samples_split=3,    # More flexible
            min_samples_leaf=1,     # More flexible
            max_features='sqrt',    # Optimized feature selection
            random_state=42,
            n_jobs=-1,
            bootstrap=True,
            oob_score=True
        )
        
        self.model.fit(X_scaled, y)
        
        # Calculate model confidence based on cross-validation
        from sklearn.model_selection import cross_val_score
        cv_scores = cross_val_score(self.model, X_scaled, y, cv=5, scoring='neg_mean_absolute_percentage_error')
        self.model_confidence = max(0.5, min(0.95, 1 - abs(cv_scores.mean())))
        
        self.last_training_date = datetime.now()
        
        # Calculate feature importance
        feature_importance = dict(zip(self.feature_names, self.model.feature_importances_))
        
        logger.info(f"Model training completed. Confidence: {self.model_confidence:.3f}")
        
        return {
            'training_samples': len(df),
            'feature_count': len(self.feature_names),
            'model_confidence': self.model_confidence,
            'feature_importance': feature_importance,
            'last_training_date': self.last_training_date.isoformat()
        }
    
    def predict(self, current_data: pd.DataFrame) -> Tuple[float, Dict]:
        """Make a prediction for the next day's price."""
        
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        # Prepare features for prediction
        df = self.prepare_features(current_data)
        
        if len(df) == 0:
            raise ValueError("No data available for prediction.")
        
        # Get the latest features
        latest_features = df[self.feature_names].iloc[-1].values.reshape(1, -1)
        latest_features_scaled = self.scaler.transform(latest_features)
        
        # Make prediction
        prediction = self.model.predict(latest_features_scaled)[0]
        
        # Get feature importance for explanation
        feature_importance = dict(zip(self.feature_names, self.model.feature_importances_))
        
        # Get current feature values for explanation
        current_features = df[self.feature_names].iloc[-1].to_dict()
        
        return prediction, {
            'prediction': prediction,
            'confidence': self.model_confidence,
            'feature_importance': feature_importance,
            'current_features': current_features,
            'model_type': 'RandomForestRegressor'
        }
    
    def save_model(self, filepath: str):
        """Save the trained model."""
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'last_training_date': self.last_training_date,
            'model_confidence': self.model_confidence
        }
        joblib.dump(model_data, filepath)
        logger.info(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load a trained model."""
        model_data = joblib.load(filepath)
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.feature_names = model_data['feature_names']
        self.last_training_date = model_data['last_training_date']
        self.model_confidence = model_data['model_confidence']
        logger.info(f"Model loaded from {filepath}")
