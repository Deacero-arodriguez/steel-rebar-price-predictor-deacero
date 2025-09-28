#!/usr/bin/env python3
"""
Quandl/Nasdaq Data Collector - Real commodity data
Uses the Quandl API key provided by the user
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

class QuandlCollector:
    """Collector for Quandl/Nasdaq data."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('QUANDL_API_KEY')
        self.base_url = "https://data.nasdaq.com/api/v3"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Steel-Rebar-Predictor/1.0'
        })
        
        if not self.api_key:
            logger.warning("Quandl API key not found")
    
    def get_gold_data(self) -> Optional[pd.DataFrame]:
        """Get gold price data from Quandl."""
        logger.info("🥇 Fetching gold data from Quandl...")
        
        try:
            # LBMA Gold prices
            url = f"{self.base_url}/datasets/LBMA/GOLD.json"
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
                    df['price_change'] = df['USD (AM)'].pct_change()
                    df['price_ma_7'] = df['USD (AM)'].rolling(7).mean()
                    df['price_ma_30'] = df['USD (AM)'].rolling(30).mean()
                    df['volatility'] = df['price_change'].rolling(7).std()
                    
                    logger.info(f"✅ Gold data: {len(df)} records")
                    return df
                else:
                    logger.warning("No gold data found in response")
                    return None
            else:
                logger.error(f"Quandl API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching gold data: {e}")
            return None
    
    def get_silver_data(self) -> Optional[pd.DataFrame]:
        """Get silver price data from Quandl."""
        logger.info("🥈 Fetching silver data from Quandl...")
        
        try:
            # LBMA Silver prices
            url = f"{self.base_url}/datasets/LBMA/SILVER.json"
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
                    df['price_change'] = df['USD'].pct_change()
                    df['price_ma_7'] = df['USD'].rolling(7).mean()
                    df['price_ma_30'] = df['USD'].rolling(30).mean()
                    df['volatility'] = df['price_change'].rolling(7).std()
                    
                    logger.info(f"✅ Silver data: {len(df)} records")
                    return df
                else:
                    logger.warning("No silver data found in response")
                    return None
            else:
                logger.error(f"Quandl API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching silver data: {e}")
            return None
    
    def get_oil_data(self) -> Optional[pd.DataFrame]:
        """Get crude oil price data from Quandl."""
        logger.info("🛢️ Fetching oil data from Quandl...")
        
        try:
            # CME Crude Oil futures
            url = f"{self.base_url}/datasets/CHRIS/CME_CL1.json"
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
                    df['price_change'] = df['Settle'].pct_change()
                    df['price_ma_7'] = df['Settle'].rolling(7).mean()
                    df['price_ma_30'] = df['Settle'].rolling(30).mean()
                    df['volatility'] = df['price_change'].rolling(7).std()
                    
                    logger.info(f"✅ Oil data: {len(df)} records")
                    return df
                else:
                    logger.warning("No oil data found in response")
                    return None
            else:
                logger.error(f"Quandl API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching oil data: {e}")
            return None
    
    def get_natural_gas_data(self) -> Optional[pd.DataFrame]:
        """Get natural gas price data from Quandl."""
        logger.info("⛽ Fetching natural gas data from Quandl...")
        
        try:
            # CME Natural Gas futures
            url = f"{self.base_url}/datasets/CHRIS/CME_NG1.json"
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
                    df['price_change'] = df['Settle'].pct_change()
                    df['price_ma_7'] = df['Settle'].rolling(7).mean()
                    df['price_ma_30'] = df['Settle'].rolling(30).mean()
                    df['volatility'] = df['price_change'].rolling(7).std()
                    
                    logger.info(f"✅ Natural gas data: {len(df)} records")
                    return df
                else:
                    logger.warning("No natural gas data found in response")
                    return None
            else:
                logger.error(f"Quandl API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching natural gas data: {e}")
            return None
    
    def get_copper_data(self) -> Optional[pd.DataFrame]:
        """Get copper price data from Quandl."""
        logger.info("🥉 Fetching copper data from Quandl...")
        
        try:
            # COMEX Copper futures
            url = f"{self.base_url}/datasets/CHRIS/CME_HG1.json"
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
                    df['price_change'] = df['Settle'].pct_change()
                    df['price_ma_7'] = df['Settle'].rolling(7).mean()
                    df['price_ma_30'] = df['Settle'].rolling(30).mean()
                    df['volatility'] = df['price_change'].rolling(7).std()
                    
                    logger.info(f"✅ Copper data: {len(df)} records")
                    return df
                else:
                    logger.warning("No copper data found in response")
                    return None
            else:
                logger.error(f"Quandl API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching copper data: {e}")
            return None
    
    def get_all_quandl_data(self) -> Dict[str, pd.DataFrame]:
        """Get all available Quandl data."""
        logger.info("🚀 COLLECTING ALL QUANDL DATA")
        logger.info("=" * 50)
        
        all_data = {}
        
        if not self.api_key:
            logger.error("Quandl API key not available")
            return all_data
        
        # Collect all datasets
        datasets = {
            'gold': self.get_gold_data,
            'silver': self.get_silver_data,
            'oil': self.get_oil_data,
            'natural_gas': self.get_natural_gas_data,
            'copper': self.get_copper_data
        }
        
        for name, fetch_func in datasets.items():
            try:
                data = fetch_func()
                if data is not None and not data.empty:
                    all_data[name] = data
                else:
                    logger.warning(f"No data collected for {name}")
                
                # Rate limiting (Quandl allows 50 requests/day on free plan)
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Error collecting {name}: {e}")
                continue
        
        # Summary
        logger.info("=" * 50)
        logger.info(f"✅ QUANDL COLLECTION COMPLETE")
        logger.info(f"📊 Datasets collected: {len(all_data)}")
        
        for name, df in all_data.items():
            logger.info(f"   {name}: {len(df)} records")
        
        return all_data

def main():
    """Test the Quandl collector."""
    print("🧪 TESTING QUANDL COLLECTOR")
    print("=" * 50)
    
    collector = QuandlCollector()
    
    # Collect all data
    all_data = collector.get_all_quandl_data()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"quandl_data_{timestamp}.json"
    
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
