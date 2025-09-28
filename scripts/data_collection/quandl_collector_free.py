#!/usr/bin/env python3
"""
Quandl/Nasdaq Data Collector - Free tier datasets only
Uses datasets available in the free tier
"""

import pandas as pd
import numpy as np
import requests
import json
import time
from datetime import datetime, timedelta
import logging
from typing import Dict, Optional, List
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QuandlFreeCollector:
    """Collector for free Quandl/Nasdaq datasets."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('QUANDL_API_KEY')
        self.base_url = "https://data.nasdaq.com/api/v3"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Steel-Rebar-Predictor/1.0'
        })
        
        if not self.api_key:
            logger.warning("Quandl API key not found")
    
    def get_free_datasets(self) -> Optional[pd.DataFrame]:
        """Get list of available free datasets."""
        logger.info("📋 Fetching available free datasets...")
        
        try:
            url = f"{self.base_url}/datasets"
            params = {
                'api_key': self.api_key,
                'database_code': 'FREE',
                'per_page': 100
            }
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Found {len(data.get('datasets', []))} free datasets")
                return pd.DataFrame(data.get('datasets', []))
            else:
                logger.error(f"Error fetching datasets: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching datasets: {e}")
            return None
    
    def get_wiki_stock_data(self, symbol: str = "AAPL") -> Optional[pd.DataFrame]:
        """Get stock data from Wiki (free dataset)."""
        logger.info(f"📈 Fetching {symbol} data from Wiki...")
        
        try:
            # Wiki stock data (free)
            url = f"{self.base_url}/datasets/WIKI/{symbol}.json"
            params = {
                'api_key': self.api_key,
                'limit': 1000,
                'order': 'desc'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'dataset' in data and 'data' in data['dataset']:
                    # Convert to DataFrame
                    columns = data['dataset']['column_names']
                    rows = data['dataset']['data']
                    
                    df = pd.DataFrame(rows, columns=columns)
                    df['Date'] = pd.to_datetime(df['Date'])
                    df = df.sort_values('Date').reset_index(drop=True)
                    
                    # Calculate additional metrics
                    df['price_change'] = df['Close'].pct_change()
                    df['price_ma_7'] = df['Close'].rolling(7).mean()
                    df['price_ma_30'] = df['Close'].rolling(30).mean()
                    df['volatility'] = df['price_change'].rolling(7).std()
                    
                    logger.info(f"✅ {symbol} data: {len(df)} records")
                    return df
                else:
                    logger.warning(f"No data found for {symbol}")
                    return None
            else:
                logger.error(f"Quandl API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching {symbol}: {e}")
            return None
    
    def get_economic_data(self) -> Optional[pd.DataFrame]:
        """Get economic indicators (free datasets)."""
        logger.info("📊 Fetching economic indicators...")
        
        try:
            # FRED economic data (free)
            url = f"{self.base_url}/datasets/FRED/GDP.json"
            params = {
                'api_key': self.api_key,
                'limit': 100,
                'order': 'desc'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'dataset' in data and 'data' in data['dataset']:
                    # Convert to DataFrame
                    columns = data['dataset']['column_names']
                    rows = data['dataset']['data']
                    
                    df = pd.DataFrame(rows, columns=columns)
                    df['Date'] = pd.to_datetime(df['Date'])
                    df = df.sort_values('Date').reset_index(drop=True)
                    
                    # Calculate additional metrics
                    df['value_change'] = df['Value'].pct_change()
                    df['value_ma_3'] = df['Value'].rolling(3).mean()
                    
                    logger.info(f"✅ GDP data: {len(df)} records")
                    return df
                else:
                    logger.warning("No GDP data found")
                    return None
            else:
                logger.error(f"Quandl API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching economic data: {e}")
            return None
    
    def test_api_connection(self) -> bool:
        """Test if API key is working."""
        logger.info("🧪 Testing Quandl API connection...")
        
        try:
            # Simple test endpoint
            url = f"{self.base_url}/datasets"
            params = {
                'api_key': self.api_key,
                'per_page': 1
            }
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                logger.info("✅ API connection successful")
                return True
            else:
                logger.error(f"API connection failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"API connection error: {e}")
            return False
    
    def get_all_free_data(self) -> Dict[str, pd.DataFrame]:
        """Get all available free data."""
        logger.info("🚀 COLLECTING ALL FREE QUANDL DATA")
        logger.info("=" * 50)
        
        all_data = {}
        
        if not self.api_key:
            logger.error("Quandl API key not available")
            return all_data
        
        # Test API connection first
        if not self.test_api_connection():
            logger.error("API connection failed, cannot collect data")
            return all_data
        
        # Get available datasets
        datasets_df = self.get_free_datasets()
        if datasets_df is not None and not datasets_df.empty:
            logger.info(f"📋 Available free datasets: {len(datasets_df)}")
            # Save datasets info
            datasets_df.to_csv('quandl_free_datasets.csv', index=False)
            logger.info("💾 Free datasets list saved to quandl_free_datasets.csv")
        
        # Collect specific free data
        free_datasets = {
            'apple_stock': lambda: self.get_wiki_stock_data('AAPL'),
            'microsoft_stock': lambda: self.get_wiki_stock_data('MSFT'),
            'gdp_data': lambda: self.get_economic_data()
        }
        
        for name, fetch_func in free_datasets.items():
            try:
                data = fetch_func()
                if data is not None and not data.empty:
                    all_data[name] = data
                else:
                    logger.warning(f"No data collected for {name}")
                
                # Rate limiting
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Error collecting {name}: {e}")
                continue
        
        # Summary
        logger.info("=" * 50)
        logger.info(f"✅ FREE QUANDL COLLECTION COMPLETE")
        logger.info(f"📊 Datasets collected: {len(all_data)}")
        
        for name, df in all_data.items():
            logger.info(f"   {name}: {len(df)} records")
        
        return all_data

def main():
    """Test the free Quandl collector."""
    print("🧪 TESTING FREE QUANDL COLLECTOR")
    print("=" * 50)
    
    collector = QuandlFreeCollector()
    
    # Collect all free data
    all_data = collector.get_all_free_data()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"quandl_free_data_{timestamp}.json"
    
    # Convert DataFrames to JSON-serializable format
    serializable_data = {}
    for name, df in all_data.items():
        if not df.empty:
            serializable_data[name] = {
                'columns': df.columns.tolist(),
                'shape': df.shape,
                'date_range': {
                    'start': df['Date'].min().isoformat(),
                    'end': df['Date'].max().isoformat()
                },
                'sample_data': df.head().to_dict('records')
            }
    
    with open(output_file, 'w') as f:
        json.dump(serializable_data, f, indent=2, default=str)
    
    print(f"\n💾 Results saved to: {output_file}")
    
    return all_data

if __name__ == "__main__":
    main()
