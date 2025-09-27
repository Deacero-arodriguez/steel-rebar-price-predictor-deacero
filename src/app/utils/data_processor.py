"""Data processing utilities for the Steel Rebar Price Predictor."""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


class DataProcessor:
    """Utility class for data processing operations."""
    
    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate data."""
        if df.empty:
            return df
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['date'])
        
        # Sort by date
        df = df.sort_values('date')
        
        # Remove outliers using IQR method
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if col != 'date':
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                # Replace outliers with NaN
                df.loc[(df[col] < lower_bound) | (df[col] > upper_bound), col] = np.nan
        
        # Forward fill missing values
        df = df.fillna(method='ffill')
        
        # Backward fill any remaining missing values
        df = df.fillna(method='bfill')
        
        return df
    
    @staticmethod
    def add_technical_indicators(df: pd.DataFrame, price_col: str = 'price') -> pd.DataFrame:
        """Add technical indicators to the data."""
        if df.empty or price_col not in df.columns:
            return df
        
        df = df.copy()
        
        # Moving averages
        for window in [7, 14, 20, 30]:
            df[f'ma_{window}'] = df[price_col].rolling(window=window).mean()
        
        # Exponential moving averages
        for window in [7, 14, 21]:
            df[f'ema_{window}'] = df[price_col].ewm(span=window).mean()
        
        # Bollinger Bands
        df['bb_middle'] = df[price_col].rolling(window=20).mean()
        bb_std = df[price_col].rolling(window=20).std()
        df['bb_upper'] = df['bb_middle'] + (2 * bb_std)
        df['bb_lower'] = df['bb_middle'] - (2 * bb_std)
        df['bb_width'] = df['bb_upper'] - df['bb_lower']
        df['bb_position'] = (df[price_col] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'])
        
        # RSI
        df['rsi_14'] = DataProcessor.calculate_rsi(df[price_col], 14)
        
        # MACD
        ema_12 = df[price_col].ewm(span=12).mean()
        ema_26 = df[price_col].ewm(span=26).mean()
        df['macd'] = ema_12 - ema_26
        df['macd_signal'] = df['macd'].ewm(span=9).mean()
        df['macd_histogram'] = df['macd'] - df['macd_signal']
        
        # Stochastic Oscillator
        df['stoch_k'] = DataProcessor.calculate_stochastic(df[price_col], 14)
        df['stoch_d'] = df['stoch_k'].rolling(window=3).mean()
        
        return df
    
    @staticmethod
    def calculate_rsi(prices: pd.Series, window: int = 14) -> pd.Series:
        """Calculate Relative Strength Index."""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    @staticmethod
    def calculate_stochastic(prices: pd.Series, window: int = 14) -> pd.Series:
        """Calculate Stochastic Oscillator %K."""
        lowest_low = prices.rolling(window=window).min()
        highest_high = prices.rolling(window=window).max()
        stoch_k = 100 * ((prices - lowest_low) / (highest_high - lowest_low))
        return stoch_k
    
    @staticmethod
    def add_seasonal_features(df: pd.DataFrame) -> pd.DataFrame:
        """Add seasonal features to the data."""
        if df.empty or 'date' not in df.columns:
            return df
        
        df = df.copy()
        df['date'] = pd.to_datetime(df['date'])
        
        # Time-based features
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df['day_of_week'] = df['date'].dt.dayofweek
        df['day_of_year'] = df['date'].dt.dayofyear
        df['week_of_year'] = df['date'].dt.isocalendar().week
        df['quarter'] = df['date'].dt.quarter
        
        # Cyclical encoding for time features
        df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
        df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
        df['day_of_week_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
        df['day_of_week_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
        
        return df
    
    @staticmethod
    def add_lag_features(df: pd.DataFrame, price_col: str = 'price', lags: List[int] = None) -> pd.DataFrame:
        """Add lagged features to the data."""
        if df.empty or price_col not in df.columns:
            return df
        
        if lags is None:
            lags = [1, 2, 3, 7, 14, 30]
        
        df = df.copy()
        
        # Add lagged prices
        for lag in lags:
            df[f'{price_col}_lag_{lag}'] = df[price_col].shift(lag)
        
        # Add price changes
        for lag in [1, 7, 14, 30]:
            df[f'{price_col}_change_{lag}d'] = df[price_col].pct_change(lag)
        
        # Add volatility measures
        for window in [7, 14, 30]:
            df[f'{price_col}_volatility_{window}d'] = df[price_col].rolling(window=window).std()
        
        return df
    
    @staticmethod
    def prepare_features_for_training(df: pd.DataFrame, target_col: str = 'price') -> Tuple[pd.DataFrame, pd.Series]:
        """Prepare features and target for machine learning training."""
        if df.empty:
            return pd.DataFrame(), pd.Series()
        
        # Get all numeric columns except target and date
        feature_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if 'date' in feature_cols:
            feature_cols.remove('date')
        if target_col in feature_cols:
            feature_cols.remove(target_col)
        
        # Remove columns with too many missing values
        missing_threshold = 0.5
        valid_cols = []
        for col in feature_cols:
            if df[col].isna().sum() / len(df) < missing_threshold:
                valid_cols.append(col)
        
        features = df[valid_cols].copy()
        target = df[target_col].copy()
        
        # Drop rows with any remaining missing values
        valid_indices = ~(features.isna().any(axis=1) | target.isna())
        features = features[valid_indices]
        target = target[valid_indices]
        
        logger.info(f"Prepared {len(features)} samples with {len(features.columns)} features")
        
        return features, target
    
    @staticmethod
    def create_feature_importance_plot(feature_importance: Dict, top_n: int = 10) -> Dict:
        """Create feature importance data for visualization."""
        if not feature_importance:
            return {}
        
        # Sort features by importance
        sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
        
        # Get top N features
        top_features = sorted_features[:top_n]
        
        return {
            'features': [item[0] for item in top_features],
            'importance': [item[1] for item in top_features]
        }
