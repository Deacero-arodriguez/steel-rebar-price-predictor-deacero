#!/usr/bin/env python3
"""
Real Data Collectors - Collect data from real APIs only
Phase 2 of correction plan: Implement real data collectors
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

class RealDataCollector:
    """Collector for real data sources only."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Steel-Rebar-Predictor/1.0'
        })
        
    def get_alpha_vantage_data(self) -> Dict[str, pd.DataFrame]:
        """Get data from Alpha Vantage (working)."""
        logger.info("🔮 Collecting data from Alpha Vantage...")
        
        alpha_data = {}
        
        # Alpha Vantage symbols for commodities
        symbols = {
            'gold': 'GLD',      # Gold ETF
            'silver': 'SLV',    # Silver ETF
            'oil': 'USO',       # Oil ETF
            'steel_proxy': 'X', # US Steel Corporation
            'usd_mxn': 'USDMXN=X'  # USD/MXN (if available)
        }
        
        for name, symbol in symbols.items():
            try:
                logger.info(f"   Fetching {name} ({symbol})...")
                
                # Use Alpha Vantage demo key for testing
                url = f"https://www.alphavantage.co/query"
                params = {
                    'function': 'TIME_SERIES_DAILY',
                    'symbol': symbol,
                    'apikey': 'demo',  # Demo key
                    'outputsize': 'compact'
                }
                
                response = self.session.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if 'Time Series (Daily)' in data:
                        # Convert to DataFrame
                        time_series = data['Time Series (Daily)']
                        df_data = []
                        
                        for date, values in time_series.items():
                            df_data.append({
                                'date': pd.to_datetime(date),
                                'open': float(values['1. open']),
                                'high': float(values['2. high']),
                                'low': float(values['3. low']),
                                'close': float(values['4. close']),
                                'volume': int(values['5. volume'])
                            })
                        
                        df = pd.DataFrame(df_data)
                        df = df.sort_values('date').reset_index(drop=True)
                        
                        # Calculate additional metrics
                        df['price_change'] = df['close'].pct_change()
                        df['price_ma_7'] = df['close'].rolling(7).mean()
                        df['price_ma_30'] = df['close'].rolling(30).mean()
                        df['volatility'] = df['price_change'].rolling(7).std()
                        
                        alpha_data[name] = df
                        logger.info(f"✅ {name}: {len(df)} records")
                        
                    elif 'Error Message' in data:
                        logger.warning(f"Alpha Vantage error for {symbol}: {data['Error Message']}")
                    else:
                        logger.warning(f"No time series data for {symbol}")
                
                # Rate limiting
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error fetching {name} from Alpha Vantage: {e}")
                continue
        
        return alpha_data
    
    def get_world_bank_data(self) -> Dict[str, pd.DataFrame]:
        """Get data from World Bank API."""
        logger.info("🌍 Collecting data from World Bank...")
        
        world_bank_data = {}
        
        # World Bank indicators for commodities
        indicators = {
            'steel_prices': 'PINKST.MTX',      # Steel prices
            'iron_ore_prices': 'PCOMM.IRON',   # Iron ore prices
            'coal_prices': 'PCOMM.COAL',       # Coal prices
            'oil_prices': 'PCOMM.OIL',         # Oil prices
            'aluminum_prices': 'PCOMM.ALUM',   # Aluminum prices
            'copper_prices': 'PCOMM.COPP'      # Copper prices
        }
        
        for name, indicator in indicators.items():
            try:
                logger.info(f"   Fetching {name} ({indicator})...")
                
                # World Bank API endpoint
                url = f"https://api.worldbank.org/v2/country/all/indicator/{indicator}"
                params = {
                    'format': 'json',
                    'per_page': 1000,
                    'date': '2020:2024'  # Last 5 years
                }
                
                response = self.session.get(url, params=params, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if len(data) > 1 and len(data[1]) > 0:
                        # Convert to DataFrame
                        df_data = []
                        for item in data[1]:
                            if item.get('value') is not None:
                                df_data.append({
                                    'date': pd.to_datetime(f"{item['date']}-01-01"),  # Year only
                                    'country': item.get('country', {}).get('value', 'World'),
                                    'indicator': item.get('indicator', {}).get('value', name),
                                    'value': float(item['value'])
                                })
                        
                        if df_data:
                            df = pd.DataFrame(df_data)
                            df = df.sort_values('date').reset_index(drop=True)
                            
                            # Calculate additional metrics
                            df['value_change'] = df['value'].pct_change()
                            df['value_ma_3'] = df['value'].rolling(3).mean()
                            
                            world_bank_data[name] = df
                            logger.info(f"✅ {name}: {len(df)} records")
                        else:
                            logger.warning(f"No valid data for {indicator}")
                    else:
                        logger.warning(f"No data available for {indicator}")
                
                # Rate limiting
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Error fetching {name} from World Bank: {e}")
                continue
        
        return world_bank_data
    
    def get_fred_data(self) -> Dict[str, pd.DataFrame]:
        """Get data from FRED API if available."""
        logger.info("🏛️ Collecting data from FRED...")
        
        fred_data = {}
        
        # FRED series for economic indicators
        series = {
            'us_interest_rate': 'FEDFUNDS',     # Federal Funds Rate
            'us_inflation': 'CPIAUCSL',         # Consumer Price Index
            'us_gdp': 'GDP',                    # Gross Domestic Product
            'us_unemployment': 'UNRATE',        # Unemployment Rate
            'usd_index': 'DTWEXBGS',            # Trade Weighted US Dollar Index
            'gold_price': 'GOLDAMGBD228NLBM'    # Gold Price
        }
        
        # Check if FRED API key is available
        fred_key = os.getenv('FRED_API_KEY')
        if not fred_key:
            logger.warning("FRED_API_KEY not found, skipping FRED data")
            return fred_data
        
        for name, series_id in series.items():
            try:
                logger.info(f"   Fetching {name} ({series_id})...")
                
                # FRED API endpoint
                url = f"https://api.stlouisfed.org/fred/series/observations"
                params = {
                    'series_id': series_id,
                    'api_key': fred_key,
                    'file_type': 'json',
                    'observation_start': '2020-01-01',
                    'observation_end': '2024-12-31',
                    'frequency': 'm'  # Monthly
                }
                
                response = self.session.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if 'observations' in data and len(data['observations']) > 0:
                        # Convert to DataFrame
                        df_data = []
                        for obs in data['observations']:
                            if obs.get('value') != '.' and obs.get('value') is not None:
                                df_data.append({
                                    'date': pd.to_datetime(obs['date']),
                                    'value': float(obs['value'])
                                })
                        
                        if df_data:
                            df = pd.DataFrame(df_data)
                            df = df.sort_values('date').reset_index(drop=True)
                            
                            # Calculate additional metrics
                            df['value_change'] = df['value'].pct_change()
                            df['value_ma_3'] = df['value'].rolling(3).mean()
                            
                            fred_data[name] = df
                            logger.info(f"✅ {name}: {len(df)} records")
                        else:
                            logger.warning(f"No valid data for {series_id}")
                    else:
                        logger.warning(f"No observations for {series_id}")
                
                # Rate limiting
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error fetching {name} from FRED: {e}")
                continue
        
        return fred_data
    
    def get_yahoo_finance_data(self) -> Dict[str, pd.DataFrame]:
        """Get data from Yahoo Finance (with SSL fix)."""
        logger.info("📈 Collecting data from Yahoo Finance...")
        
        yahoo_data = {}
        
        try:
            import yfinance as yf
            
            # Yahoo Finance symbols
            symbols = {
                'usd_mxn': 'USDMXN=X',      # USD/MXN
                'gold': 'GC=F',             # Gold futures
                'silver': 'SI=F',           # Silver futures
                'oil': 'CL=F',              # Crude oil futures
                'steel_proxy': 'X',         # US Steel
                'copper': 'HG=F',           # Copper futures
                'iron_ore_proxy': 'VALE',   # Vale (iron ore producer)
                'coal_proxy': 'BTU'         # Peabody Energy (coal)
            }
            
            for name, symbol in symbols.items():
                try:
                    logger.info(f"   Fetching {name} ({symbol})...")
                    
                    # Download data
                    ticker = yf.Ticker(symbol)
                    data = ticker.history(period="2y")
                    
                    if not data.empty:
                        # Reset index to get date as column
                        data = data.reset_index()
                        data['date'] = pd.to_datetime(data['Date'])
                        data = data.drop('Date', axis=1)
                        
                        # Calculate additional metrics
                        data['price_change'] = data['Close'].pct_change()
                        data['price_ma_7'] = data['Close'].rolling(7).mean()
                        data['price_ma_30'] = data['Close'].rolling(30).mean()
                        data['volatility'] = data['price_change'].rolling(7).std()
                        data['volume_ma_7'] = data['Volume'].rolling(7).mean()
                        
                        yahoo_data[name] = data
                        logger.info(f"✅ {name}: {len(data)} records")
                    
                    # Rate limiting
                    time.sleep(1)
                    
                except Exception as e:
                    logger.error(f"Error fetching {name} from Yahoo Finance: {e}")
                    continue
                    
        except ImportError:
            logger.error("yfinance not available, skipping Yahoo Finance data")
        except Exception as e:
            logger.error(f"Yahoo Finance error: {e}")
        
        return yahoo_data
    
    def get_all_real_data(self) -> Dict[str, Dict[str, pd.DataFrame]]:
        """Get data from all real sources."""
        logger.info("🚀 COLLECTING ALL REAL DATA")
        logger.info("=" * 60)
        
        all_data = {}
        
        # Collect from each source
        all_data['alpha_vantage'] = self.get_alpha_vantage_data()
        all_data['world_bank'] = self.get_world_bank_data()
        all_data['fred'] = self.get_fred_data()
        all_data['yahoo_finance'] = self.get_yahoo_finance_data()
        
        # Summary
        total_sources = 0
        total_datasets = 0
        
        for source, datasets in all_data.items():
            if datasets:
                total_sources += 1
                total_datasets += len(datasets)
                logger.info(f"📊 {source.upper()}: {len(datasets)} datasets")
        
        logger.info("=" * 60)
        logger.info(f"✅ COLLECTION COMPLETE")
        logger.info(f"📈 Sources working: {total_sources}/4")
        logger.info(f"📊 Total datasets: {total_datasets}")
        
        return all_data

def main():
    """Test the real data collectors."""
    print("🧪 TESTING REAL DATA COLLECTORS")
    print("=" * 60)
    
    collector = RealDataCollector()
    
    # Collect all real data
    all_data = collector.get_all_real_data()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"real_data_collection_{timestamp}.json"
    
    # Convert DataFrames to JSON-serializable format
    serializable_data = {}
    for source, datasets in all_data.items():
        serializable_data[source] = {}
        for name, df in datasets.items():
            if not df.empty:
                serializable_data[source][name] = {
                    'columns': df.columns.tolist(),
                    'shape': df.shape,
                    'date_range': {
                        'start': df['date'].min().isoformat() if 'date' in df.columns else None,
                        'end': df['date'].max().isoformat() if 'date' in df.columns else None
                    },
                    'sample_data': df.head().to_dict('records')
                }
    
    with open(output_file, 'w') as f:
        json.dump(serializable_data, f, indent=2, default=str)
    
    print(f"\n💾 Results saved to: {output_file}")
    
    return all_data

if __name__ == "__main__":
    main()
