#!/usr/bin/env python3
"""
Enhanced ML Model with Currency Exchange Analysis for Steel Rebar Price Prediction.
Specifically designed for DeAcero considering USD/MXN exchange rate impact.
"""

import joblib
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_percentage_error, r2_score
from sklearn.model_selection import cross_val_score
import logging

logger = logging.getLogger(__name__)


class EnhancedSteelRebarPredictor:
    """Enhanced ML model for predicting steel rebar prices with currency focus."""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = []
        self.currency_feature_names = []
        self.last_training_date = None
        self.model_confidence = 0.85
        self.currency_impact_analysis = {}
        
    def prepare_currency_enhanced_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Prepare features with enhanced currency analysis for DeAcero."""
        
        df = data.copy()
        
        # Ensure date column is datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Basic price features
        if 'steel_price' in df.columns:
            df['price_ma_7'] = df['steel_price'].rolling(window=7).mean()
            df['price_ma_14'] = df['steel_price'].rolling(window=14).mean()
            df['price_ma_30'] = df['steel_price'].rolling(window=30).mean()
            df['price_volatility_7'] = df['steel_price'].rolling(window=7).std()
            df['price_volatility_14'] = df['steel_price'].rolling(window=14).std()
            df['price_change_1d'] = df['steel_price'].pct_change(1)
            df['price_change_7d'] = df['steel_price'].pct_change(7)
            df['price_change_30d'] = df['steel_price'].pct_change(30)
        
        # Currency-specific features (Critical for DeAcero)
        if 'usd_mxn_rate' in df.columns:
            # Basic currency features
            df['usd_mxn_ma_7'] = df['usd_mxn_rate'].rolling(window=7).mean()
            df['usd_mxn_ma_14'] = df['usd_mxn_rate'].rolling(window=14).mean()
            df['usd_mxn_ma_30'] = df['usd_mxn_rate'].rolling(window=30).mean()
            df['usd_mxn_volatility_7'] = df['usd_mxn_rate'].rolling(window=7).std()
            df['usd_mxn_change_1d'] = df['usd_mxn_rate'].pct_change(1)
            df['usd_mxn_change_7d'] = df['usd_mxn_rate'].pct_change(7)
            df['usd_mxn_change_30d'] = df['usd_mxn_rate'].pct_change(30)
            
            # DeAcero-specific currency impact features
            df['mxn_strength_index'] = 1 / df['usd_mxn_rate']  # Higher = stronger MXN
            df['mxn_weakness_magnitude'] = df['usd_mxn_change_1d'].apply(
                lambda x: max(0, x) if x > 0 else 0  # Only MXN weakening
            )
            df['import_cost_pressure'] = df['usd_mxn_rate'] / df['usd_mxn_ma_30']
            
            # Currency-adjusted price features
            if 'steel_price' in df.columns:
                df['steel_price_mxn'] = df['steel_price'] * df['usd_mxn_rate']
                df['steel_price_mxn_ma_7'] = df['steel_price_mxn'].rolling(window=7).mean()
                df['steel_price_mxn_change'] = df['steel_price_mxn'].pct_change(1)
                df['price_currency_sensitivity'] = df['steel_price_change_1d'] / df['usd_mxn_change_1d']
        
        # Cross-currency features
        for col in df.columns:
            if col.endswith('_rate') and col != 'usd_mxn_rate':
                currency_name = col.replace('_rate', '')
                df[f'{currency_name}_vs_mxn'] = df[col] / df['usd_mxn_rate']
                df[f'{currency_name}_change_1d'] = df[col].pct_change(1)
        
        # Steel price in MXN terms (DeAcero's local perspective)
        if 'steel_price' in df.columns and 'usd_mxn_rate' in df.columns:
            df['local_steel_price_mxn'] = df['steel_price'] * df['usd_mxn_rate']
            df['local_price_volatility'] = df['local_steel_price_mxn'].rolling(window=7).std()
            df['local_price_trend'] = df['local_steel_price_mxn'].rolling(window=14).apply(
                lambda x: np.polyfit(range(len(x)), x, 1)[0] if len(x) == 14 else 0
            )
        
        # Technical indicators with currency adjustment
        if 'steel_price' in df.columns:
            df['rsi_14'] = self._calculate_rsi(df['steel_price'], 14)
            df['bollinger_upper'] = df['price_ma_14'] + (2 * df['price_volatility_7'])
            df['bollinger_lower'] = df['price_ma_14'] - (2 * df['price_volatility_7'])
            df['bollinger_position'] = (df['steel_price'] - df['bollinger_lower']) / (df['bollinger_upper'] - df['bollinger_lower'])
        
        # Seasonal features
        df['month'] = df['date'].dt.month
        df['day_of_week'] = df['date'].dt.dayofweek
        df['quarter'] = df['date'].dt.quarter
        df['is_month_end'] = df['date'].dt.is_month_end.astype(int)
        df['is_quarter_end'] = df['date'].dt.is_quarter_end.astype(int)
        
        # Cyclical encoding for time features
        df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
        df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
        df['day_of_week_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
        df['day_of_week_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
        
        # Economic indicators (if available)
        for col in df.columns:
            if 'index_value' in col or '_price' in col:
                if col not in ['steel_price', 'steel_price_mxn', 'local_steel_price_mxn']:
                    base_name = col.replace('_price', '').replace('_value', '')
                    df[f'{base_name}_ma_7'] = df[col].rolling(window=7).mean()
                    df[f'{base_name}_change_7d'] = df[col].pct_change(7)
                    df[f'{base_name}_volatility'] = df[col].rolling(window=7).std()
        
        # Drop rows with NaN values
        df = df.dropna()
        
        # Identify currency-specific features
        self.currency_feature_names = [col for col in df.columns if any(
            currency in col.lower() for currency in ['mxn', 'usd', 'currency', 'exchange', 'rate']
        )]
        
        # Select all numeric features for training
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if 'date' in numeric_cols:
            numeric_cols.remove('date')
        
        self.feature_names = numeric_cols
        
        return df[['date'] + numeric_cols]
    
    def _calculate_rsi(self, prices: pd.Series, window: int = 14) -> pd.Series:
        """Calculate Relative Strength Index."""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def analyze_currency_impact(self, data: pd.DataFrame) -> Dict:
        """Analyze the impact of currency fluctuations on steel prices."""
        
        analysis = {}
        
        if 'steel_price' in data.columns and 'usd_mxn_rate' in data.columns:
            # Correlation analysis
            price_currency_corr = data['steel_price'].corr(data['usd_mxn_rate'])
            analysis['price_currency_correlation'] = price_currency_corr
            
            # Volatility analysis
            price_vol = data['steel_price'].std()
            currency_vol = data['usd_mxn_rate'].std()
            analysis['price_volatility'] = price_vol
            analysis['currency_volatility'] = currency_vol
            analysis['volatility_ratio'] = price_vol / currency_vol if currency_vol > 0 else 0
            
            # Impact analysis
            currency_changes = data['usd_mxn_rate'].pct_change().dropna()
            price_changes = data['steel_price'].pct_change().dropna()
            
            # Calculate impact when MXN weakens (USD/MXN increases)
            mxn_weakening_mask = currency_changes > 0
            if mxn_weakening_mask.sum() > 0:
                corresponding_price_changes = price_changes[mxn_weakening_mask]
                analysis['price_impact_on_mxn_weakening'] = corresponding_price_changes.mean()
            
            # Calculate impact when MXN strengthens (USD/MXN decreases)
            mxn_strengthening_mask = currency_changes < 0
            if mxn_strengthening_mask.sum() > 0:
                corresponding_price_changes = price_changes[mxn_strengthening_mask]
                analysis['price_impact_on_mxn_strengthening'] = corresponding_price_changes.mean()
        
        # Store analysis for later use
        self.currency_impact_analysis = analysis
        
        return analysis
    
    def train(self, data: pd.DataFrame) -> Dict:
        """Train the enhanced ML model with currency analysis."""
        
        logger.info("Starting enhanced model training with currency analysis...")
        
        # Prepare features
        df = self.prepare_currency_enhanced_features(data)
        
        if len(df) < 30:
            raise ValueError("Insufficient data for training. Need at least 30 days of data.")
        
        # Analyze currency impact
        currency_analysis = self.analyze_currency_impact(data)
        
        # Split features and target
        X = df[self.feature_names].values
        y = df['steel_price'].values if 'steel_price' in df.columns else df.iloc[:, 1].values
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train enhanced model
        self.model = RandomForestRegressor(
            n_estimators=150,  # Increased for better performance
            max_depth=12,      # Increased for more complex patterns
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        
        self.model.fit(X_scaled, y)
        
        # Calculate model confidence based on cross-validation
        cv_scores = cross_val_score(self.model, X_scaled, y, cv=5, scoring='neg_mean_absolute_percentage_error')
        self.model_confidence = max(0.5, min(0.95, 1 - abs(cv_scores.mean())))
        
        self.last_training_date = datetime.now()
        
        # Calculate feature importance
        feature_importance = dict(zip(self.feature_names, self.model.feature_importances_))
        
        # Separate currency feature importance
        currency_feature_importance = {
            feature: importance for feature, importance in feature_importance.items()
            if feature in self.currency_feature_names
        }
        
        logger.info(f"Enhanced model training completed. Confidence: {self.model_confidence:.3f}")
        logger.info(f"Currency features identified: {len(self.currency_feature_names)}")
        
        return {
            'training_samples': len(df),
            'feature_count': len(self.feature_names),
            'currency_feature_count': len(self.currency_feature_names),
            'model_confidence': self.model_confidence,
            'feature_importance': feature_importance,
            'currency_feature_importance': currency_feature_importance,
            'currency_impact_analysis': currency_analysis,
            'last_training_date': self.last_training_date.isoformat()
        }
    
    def predict_with_currency_analysis(self, data: pd.DataFrame) -> Tuple[float, Dict]:
        """Make prediction with detailed currency impact analysis."""
        
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        # Prepare features for prediction
        df = self.prepare_currency_enhanced_features(data)
        
        if len(df) == 0:
            raise ValueError("No data available for prediction.")
        
        # Get the latest features
        latest_features = df[self.feature_names].iloc[-1].values.reshape(1, -1)
        latest_features_scaled = self.scaler.transform(latest_features)
        
        # Make prediction
        prediction = self.model.predict(latest_features_scaled)[0]
        
        # Get feature importance
        feature_importance = dict(zip(self.feature_names, self.model.feature_importances_))
        
        # Get current feature values
        current_features = df[self.feature_names].iloc[-1].to_dict()
        
        # Analyze currency impact on prediction
        currency_impact_factors = {
            feature: value for feature, value in current_features.items()
            if feature in self.currency_feature_names
        }
        
        # Calculate currency-adjusted prediction confidence
        currency_volatility = current_features.get('usd_mxn_volatility_7', 0)
        base_confidence = self.model_confidence
        
        # Adjust confidence based on currency volatility
        if currency_volatility > 0:
            # Higher currency volatility = lower confidence
            volatility_adjustment = min(0.1, currency_volatility * 0.01)
            adjusted_confidence = base_confidence - volatility_adjustment
        else:
            adjusted_confidence = base_confidence
        
        return prediction, {
            'prediction': prediction,
            'confidence': adjusted_confidence,
            'feature_importance': feature_importance,
            'currency_feature_importance': {
                feature: importance for feature, importance in feature_importance.items()
                if feature in self.currency_feature_names
            },
            'current_features': current_features,
            'currency_impact_factors': currency_impact_factors,
            'currency_impact_analysis': self.currency_impact_analysis,
            'model_type': 'Enhanced RandomForestRegressor with Currency Analysis'
        }
    
    def save_model(self, filepath: str):
        """Save the trained enhanced model."""
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'currency_feature_names': self.currency_feature_names,
            'last_training_date': self.last_training_date,
            'model_confidence': self.model_confidence,
            'currency_impact_analysis': self.currency_impact_analysis
        }
        joblib.dump(model_data, filepath)
        logger.info(f"Enhanced model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load a trained enhanced model."""
        model_data = joblib.load(filepath)
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.feature_names = model_data['feature_names']
        self.currency_feature_names = model_data['currency_feature_names']
        self.last_training_date = model_data['last_training_date']
        self.model_confidence = model_data['model_confidence']
        self.currency_impact_analysis = model_data.get('currency_impact_analysis', {})
        logger.info(f"Enhanced model loaded from {filepath}")


def main():
    """Test the enhanced ML model."""
    print("🤖 Enhanced ML Model - Currency-Aware Steel Rebar Predictor")
    print("=" * 60)
    
    # This would be used with the enhanced data collector
    print("✅ Enhanced model ready for integration with currency data")
    print("   Features: Currency impact analysis, MXN-specific factors")
    print("   Optimized for: DeAcero operations in Mexico")


if __name__ == "__main__":
    main()
