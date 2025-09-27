"""Data collection service for steel rebar price prediction."""

import yfinance as yf
import pandas as pd
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
import time

logger = logging.getLogger(__name__)


class DataCollector:
    """Service for collecting data from various sources."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Steel-Rebar-Predictor/1.0'
        })
    
    def get_yahoo_finance_data(self, symbol: str, period: str = "2y") -> pd.DataFrame:
        """Get data from Yahoo Finance."""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            
            if data.empty:
                logger.warning(f"No data found for symbol {symbol}")
                return pd.DataFrame()
            
            # Reset index to get date as column
            data = data.reset_index()
            data['date'] = pd.to_datetime(data['Date'])
            data = data.drop('Date', axis=1)
            
            # Rename Close to price
            data = data.rename(columns={'Close': 'price'})
            
            logger.info(f"Retrieved {len(data)} records for {symbol}")
            return data[['date', 'price']]
            
        except Exception as e:
            logger.error(f"Error fetching Yahoo Finance data for {symbol}: {e}")
            return pd.DataFrame()
    
    def get_alpha_vantage_data(self, symbol: str, api_key: str, function: str = "TIME_SERIES_DAILY") -> pd.DataFrame:
        """Get data from Alpha Vantage API."""
        try:
            url = "https://www.alphavantage.co/query"
            params = {
                'function': function,
                'symbol': symbol,
                'apikey': api_key,
                'outputsize': 'full'
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if 'Time Series (Daily)' not in data:
                logger.warning(f"No time series data found for {symbol}")
                return pd.DataFrame()
            
            # Convert to DataFrame
            time_series = data['Time Series (Daily)']
            df = pd.DataFrame.from_dict(time_series, orient='index')
            df.index = pd.to_datetime(df.index)
            df = df.sort_index()
            
            # Rename columns
            df = df.rename(columns={'4. close': 'price'})
            df['date'] = df.index
            df['price'] = pd.to_numeric(df['price'])
            
            logger.info(f"Retrieved {len(df)} records from Alpha Vantage for {symbol}")
            return df[['date', 'price']]
            
        except Exception as e:
            logger.error(f"Error fetching Alpha Vantage data for {symbol}: {e}")
            return pd.DataFrame()
    
    def get_fred_data(self, series_id: str, api_key: str) -> pd.DataFrame:
        """Get data from FRED API."""
        try:
            url = "https://api.stlouisfed.org/fred/series/observations"
            params = {
                'series_id': series_id,
                'api_key': api_key,
                'file_type': 'json',
                'limit': 1000
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if 'observations' not in data:
                logger.warning(f"No observations found for FRED series {series_id}")
                return pd.DataFrame()
            
            # Convert to DataFrame
            observations = data['observations']
            df = pd.DataFrame(observations)
            
            # Filter out missing values
            df = df[df['value'] != '.']
            df['date'] = pd.to_datetime(df['date'])
            df['price'] = pd.to_numeric(df['value'])
            
            df = df.sort_values('date')
            
            logger.info(f"Retrieved {len(df)} records from FRED for {series_id}")
            return df[['date', 'price']]
            
        except Exception as e:
            logger.error(f"Error fetching FRED data for {series_id}: {e}")
            return pd.DataFrame()
    
    def get_steel_rebar_data(self) -> pd.DataFrame:
        """Get steel rebar price data from multiple sources."""
        
        logger.info("Collecting steel rebar price data...")
        
        # Primary source: Yahoo Finance (Steel futures or related commodities)
        # Using steel-related symbols that are available
        steel_symbols = [
            'CLF',  # Cleveland-Cliffs (iron ore/steel)
            'NUE',  # Nucor Corporation (steel)
            'STLD', # Steel Dynamics
            'X',    # United States Steel
        ]
        
        all_data = []
        
        for symbol in steel_symbols:
            data = self.get_yahoo_finance_data(symbol)
            if not data.empty:
                data['symbol'] = symbol
                all_data.append(data)
            time.sleep(1)  # Rate limiting
        
        if not all_data:
            logger.warning("No steel data found from Yahoo Finance")
            return pd.DataFrame()
        
        # Combine all data and calculate average price
        combined_data = pd.concat(all_data, ignore_index=True)
        
        # Group by date and calculate average price
        daily_prices = combined_data.groupby('date')['price'].mean().reset_index()
        daily_prices = daily_prices.sort_values('date')
        
        # Scale to approximate steel rebar prices (rough estimation)
        # Steel rebar prices are typically higher than steel company stock prices
        daily_prices['price'] = daily_prices['price'] * 15  # Rough scaling factor
        
        logger.info(f"Combined steel data: {len(daily_prices)} records")
        return daily_prices
    
    def get_iron_ore_data(self) -> pd.DataFrame:
        """Get iron ore price data."""
        
        logger.info("Collecting iron ore price data...")
        
        # Try Yahoo Finance first (iron ore futures or related)
        iron_symbols = ['VALE', 'RIO', 'BHP']  # Iron ore companies
        
        all_data = []
        for symbol in iron_symbols:
            data = self.get_yahoo_finance_data(symbol)
            if not data.empty:
                data['symbol'] = symbol
                all_data.append(data)
            time.sleep(1)
        
        if not all_data:
            logger.warning("No iron ore data found")
            return pd.DataFrame()
        
        # Combine and average
        combined_data = pd.concat(all_data, ignore_index=True)
        daily_prices = combined_data.groupby('date')['price'].mean().reset_index()
        daily_prices = daily_prices.sort_values('date')
        
        # Scale to approximate iron ore prices
        daily_prices['price'] = daily_prices['price'] * 5  # Rough scaling
        
        logger.info(f"Combined iron ore data: {len(daily_prices)} records")
        return daily_prices
    
    def get_coal_data(self) -> pd.DataFrame:
        """Get coal price data."""
        
        logger.info("Collecting coal price data...")
        
        # Coal company stocks as proxy
        coal_symbols = ['BTU', 'ARLP', 'HNRG']
        
        all_data = []
        for symbol in coal_symbols:
            data = self.get_yahoo_finance_data(symbol)
            if not data.empty:
                data['symbol'] = symbol
                all_data.append(data)
            time.sleep(1)
        
        if not all_data:
            logger.warning("No coal data found")
            return pd.DataFrame()
        
        # Combine and average
        combined_data = pd.concat(all_data, ignore_index=True)
        daily_prices = combined_data.groupby('date')['price'].mean().reset_index()
        daily_prices = daily_prices.sort_values('date')
        
        # Scale to approximate coal prices
        daily_prices['price'] = daily_prices['price'] * 20  # Rough scaling
        
        logger.info(f"Combined coal data: {len(daily_prices)} records")
        return daily_prices
    
    def get_usd_mxn_rate(self) -> pd.DataFrame:
        """Get USD/MXN exchange rate."""
        
        logger.info("Collecting USD/MXN exchange rate...")
        
        # Yahoo Finance for currency rates
        data = self.get_yahoo_finance_data("USDMXN=X")
        
        if data.empty:
            logger.warning("No USD/MXN data found")
            return pd.DataFrame()
        
        # Rename price to rate
        data = data.rename(columns={'price': 'rate'})
        
        logger.info(f"USD/MXN data: {len(data)} records")
        return data
    
    def get_all_economic_data(self) -> Dict[str, pd.DataFrame]:
        """Get all economic data needed for the model."""
        
        logger.info("Collecting all economic data...")
        
        data = {}
        
        # Steel rebar data (primary)
        steel_data = self.get_steel_rebar_data()
        if not steel_data.empty:
            data['steel_rebar'] = steel_data
        
        # Iron ore data
        iron_data = self.get_iron_ore_data()
        if not iron_data.empty:
            data['iron_ore'] = iron_data
        
        # Coal data
        coal_data = self.get_coal_data()
        if not coal_data.empty:
            data['coal'] = coal_data
        
        # USD/MXN rate
        currency_data = self.get_usd_mxn_rate()
        if not currency_data.empty:
            data['usd_mxn'] = currency_data
        
        logger.info(f"Collected data from {len(data)} sources")
        return data
    
    def combine_data_for_training(self, economic_data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """Combine all economic data into a single DataFrame for training."""
        
        if not economic_data:
            logger.error("No economic data available")
            return pd.DataFrame()
        
        # Start with steel rebar data as the base
        if 'steel_rebar' not in economic_data:
            logger.error("Steel rebar data is required")
            return pd.DataFrame()
        
        df = economic_data['steel_rebar'].copy()
        df = df.rename(columns={'price': 'price'})
        
        # Merge other data sources
        for source, data in economic_data.items():
            if source == 'steel_rebar':
                continue
            
            # Rename price column to source-specific name
            price_col = f"{source}_price"
            if source == 'usd_mxn':
                price_col = 'usd_mxn_rate'
            
            data_renamed = data.rename(columns={'price': price_col})
            
            # Merge on date
            df = df.merge(data_renamed[['date', price_col]], on='date', how='left')
        
        # Forward fill missing values
        df = df.fillna(method='ffill')
        
        # Drop rows with any remaining NaN values
        df = df.dropna()
        
        logger.info(f"Combined dataset: {len(df)} records with {len(df.columns)} columns")
        return df
