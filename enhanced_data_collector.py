#!/usr/bin/env python3
"""
Enhanced Data Collector with Currency Exchange Analysis for Steel Rebar Price Prediction.
Integrates multiple sources including exchange rates as suggested in the DeAcero context.
"""

import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
import time
import yfinance as yf

logger = logging.getLogger(__name__)


class EnhancedDataCollector:
    """Enhanced service for collecting data from various sources with currency focus."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Steel-Rebar-Predictor-DeAcero/1.0'
        })
        
        # Currency pairs relevant for DeAcero operations
        self.currency_pairs = {
            'USD_MXN': 'USDMXN=X',
            'USD_EUR': 'EURUSD=X',
            'USD_CNY': 'USDCNY=X',  # Important for Chinese steel prices
            'USD_JPY': 'USDJPY=X'   # For Asian market sentiment
        }
        
        # Steel-related symbols from context
        self.steel_symbols = {
            'steel_rebar_shanghai': 'RB.SHF',  # Shanghai Steel Rebar Futures
            'steel_rebar_london': 'STEEL.L',   # London Steel
            'iron_ore_62': 'IO=F',            # Iron Ore 62% Fe
            'iron_ore_58': 'IO=F',            # Iron Ore 58% Fe
            'coking_coal': 'MTF=F',           # Coking Coal Futures
            'hot_rolled_coil': 'HR=F'         # Hot Rolled Coil Steel
        }
    
    def get_exchange_rates(self) -> Dict[str, pd.DataFrame]:
        """Get historical exchange rates for relevant currency pairs."""
        logger.info("📈 Collecting exchange rate data...")
        
        exchange_data = {}
        
        for pair_name, symbol in self.currency_pairs.items():
            try:
                logger.info(f"   Fetching {pair_name} ({symbol})...")
                
                ticker = yf.Ticker(symbol)
                data = ticker.history(period="2y")
                
                if data.empty:
                    logger.warning(f"No data found for {pair_name}")
                    continue
                
                # Reset index and clean data
                data = data.reset_index()
                data['date'] = pd.to_datetime(data['Date'])
                data = data.drop('Date', axis=1)
                
                # Calculate additional metrics
                data['rate'] = data['Close']
                data['rate_change_1d'] = data['rate'].pct_change(1)
                data['rate_volatility_7d'] = data['rate'].rolling(window=7).std()
                data['rate_ma_7'] = data['rate'].rolling(window=7).mean()
                data['rate_ma_30'] = data['rate'].rolling(window=30).mean()
                
                # Store with pair name
                exchange_data[pair_name] = data[['date', 'rate', 'rate_change_1d', 
                                               'rate_volatility_7d', 'rate_ma_7', 'rate_ma_30']]
                
                logger.info(f"✅ {pair_name}: {len(data)} records")
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                logger.error(f"Error fetching {pair_name}: {e}")
                continue
        
        return exchange_data
    
    def get_steel_prices_from_context_sources(self) -> Dict[str, pd.DataFrame]:
        """Get steel prices from sources mentioned in the DeAcero context."""
        logger.info("🏗️ Collecting steel price data from context sources...")
        
        steel_data = {}
        
        for steel_type, symbol in self.steel_symbols.items():
            try:
                logger.info(f"   Fetching {steel_type} ({symbol})...")
                
                ticker = yf.Ticker(symbol)
                data = ticker.history(period="2y")
                
                if data.empty:
                    logger.warning(f"No data found for {steel_type}")
                    continue
                
                # Reset index and clean data
                data = data.reset_index()
                data['date'] = pd.to_datetime(data['Date'])
                data = data.drop('Date', axis=1)
                
                # Calculate price metrics
                data['price'] = data['Close']
                data['price_change_1d'] = data['price'].pct_change(1)
                data['price_volatility_7d'] = data['price'].rolling(window=7).std()
                data['price_ma_7'] = data['price'].rolling(window=7).mean()
                data['price_ma_14'] = data['price'].rolling(window=14).mean()
                data['price_ma_30'] = data['price'].rolling(window=30).mean()
                
                # Store with steel type
                steel_data[steel_type] = data[['date', 'price', 'price_change_1d', 
                                             'price_volatility_7d', 'price_ma_7', 
                                             'price_ma_14', 'price_ma_30']]
                
                logger.info(f"✅ {steel_type}: {len(data)} records")
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                logger.error(f"Error fetching {steel_type}: {e}")
                continue
        
        return steel_data
    
    def get_commodity_indices(self) -> Dict[str, pd.DataFrame]:
        """Get commodity indices as mentioned in the context."""
        logger.info("📊 Collecting commodity indices...")
        
        indices = {
            'sp_goldman_sachs': 'SPGSCI',
            'dow_jones_commodity': 'DJAIG',
            'crb_index': 'CRB'
        }
        
        commodity_data = {}
        
        for index_name, symbol in indices.items():
            try:
                logger.info(f"   Fetching {index_name} ({symbol})...")
                
                ticker = yf.Ticker(symbol)
                data = ticker.history(period="2y")
                
                if data.empty:
                    logger.warning(f"No data found for {index_name}")
                    continue
                
                # Reset index and clean data
                data = data.reset_index()
                data['date'] = pd.to_datetime(data['Date'])
                data = data.drop('Date', axis=1)
                
                # Calculate index metrics
                data['index_value'] = data['Close']
                data['index_change_1d'] = data['index_value'].pct_change(1)
                data['index_volatility_7d'] = data['index_value'].rolling(window=7).std()
                data['index_ma_7'] = data['index_value'].rolling(window=7).mean()
                
                # Store with index name
                commodity_data[index_name] = data[['date', 'index_value', 'index_change_1d', 
                                                 'index_volatility_7d', 'index_ma_7']]
                
                logger.info(f"✅ {index_name}: {len(data)} records")
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                logger.error(f"Error fetching {index_name}: {e}")
                continue
        
        return commodity_data
    
    def calculate_currency_impact_factors(self, exchange_data: Dict[str, pd.DataFrame], 
                                        steel_data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """Calculate currency impact factors on steel prices."""
        logger.info("💱 Calculating currency impact factors...")
        
        if 'USD_MXN' not in exchange_data:
            logger.warning("USD/MXN data not available for currency impact calculation")
            return pd.DataFrame()
        
        usd_mxn = exchange_data['USD_MXN'].copy()
        
        # Calculate DeAcero-specific factors
        usd_mxn['mxn_strength'] = 1 / usd_mxn['rate']  # Higher = stronger MXN
        usd_mxn['mxn_weakness_impact'] = usd_mxn['rate_change_1d'].apply(
            lambda x: max(0, x) if x > 0 else 0  # Only positive changes (MXN weakening)
        )
        usd_mxn['import_cost_multiplier'] = usd_mxn['rate'] / usd_mxn['rate'].rolling(30).mean()
        
        # Calculate cross-currency correlations
        if 'USD_EUR' in exchange_data and 'USD_CNY' in exchange_data:
            eur_data = exchange_data['USD_EUR']
            cny_data = exchange_data['USD_CNY']
            
            # Merge on date
            currency_analysis = usd_mxn.merge(
                eur_data[['date', 'rate']], on='date', how='left', suffixes=('', '_EUR')
            ).merge(
                cny_data[['date', 'rate']], on='date', how='left', suffixes=('', '_CNY')
            )
            
            # Calculate relative strength
            currency_analysis['mxn_vs_eur'] = currency_analysis['rate'] / currency_analysis['rate_EUR']
            currency_analysis['mxn_vs_cny'] = currency_analysis['rate'] / currency_analysis['rate_CNY']
            currency_analysis['global_currency_sentiment'] = (
                currency_analysis['mxn_vs_eur'] + currency_analysis['mxn_vs_cny']
            ) / 2
        
        logger.info(f"✅ Currency impact factors calculated for {len(usd_mxn)} dates")
        return currency_analysis if 'currency_analysis' in locals() else usd_mxn
    
    def combine_all_data_with_currency_focus(self) -> pd.DataFrame:
        """Combine all data sources with focus on currency impact for DeAcero."""
        logger.info("🔄 Combining all data sources with currency focus...")
        
        # Collect all data
        exchange_data = self.get_exchange_rates()
        steel_data = self.get_steel_prices_from_context_sources()
        commodity_data = self.get_commodity_indices()
        
        if not exchange_data or not steel_data:
            logger.error("Insufficient data for combination")
            return pd.DataFrame()
        
        # Start with USD/MXN as base (most important for DeAcero)
        combined_data = exchange_data['USD_MXN'].copy()
        combined_data = combined_data.rename(columns={'rate': 'usd_mxn_rate'})
        
        # Add currency impact factors
        currency_factors = self.calculate_currency_impact_factors(exchange_data, steel_data)
        if not currency_factors.empty:
            combined_data = combined_data.merge(
                currency_factors[['date', 'mxn_strength', 'mxn_weakness_impact', 
                                'import_cost_multiplier']], 
                on='date', how='left'
            )
        
        # Add steel prices (use first available steel type as primary)
        primary_steel = list(steel_data.keys())[0] if steel_data else None
        if primary_steel:
            steel_primary = steel_data[primary_steel].copy()
            steel_primary = steel_primary.rename(columns={'price': 'steel_price'})
            combined_data = combined_data.merge(
                steel_primary[['date', 'steel_price', 'price_change_1d', 
                             'price_volatility_7d', 'price_ma_7']], 
                on='date', how='left'
            )
        
        # Add other steel types as features
        for steel_type, steel_df in steel_data.items():
            if steel_type != primary_steel:
                feature_name = f"{steel_type}_price"
                steel_df_clean = steel_df[['date', 'price']].copy()
                steel_df_clean = steel_df_clean.rename(columns={'price': feature_name})
                combined_data = combined_data.merge(steel_df_clean, on='date', how='left')
        
        # Add commodity indices
        for index_name, index_df in commodity_data.items():
            feature_name = f"{index_name}_value"
            index_df_clean = index_df[['date', 'index_value']].copy()
            index_df_clean = index_df_clean.rename(columns={'index_value': feature_name})
            combined_data = combined_data.merge(index_df_clean, on='date', how='left')
        
        # Add other currency pairs as features
        for pair_name, pair_df in exchange_data.items():
            if pair_name != 'USD_MXN':
                feature_name = f"{pair_name}_rate"
                pair_df_clean = pair_df[['date', 'rate']].copy()
                pair_df_clean = pair_df_clean.rename(columns={'rate': feature_name})
                combined_data = combined_data.merge(pair_df_clean, on='date', how='left')
        
        # Calculate DeAcero-specific features
        if 'steel_price' in combined_data.columns and 'usd_mxn_rate' in combined_data.columns:
            # Price in MXN terms
            combined_data['steel_price_mxn'] = combined_data['steel_price'] * combined_data['usd_mxn_rate']
            
            # Currency-adjusted price changes
            combined_data['steel_price_mxn_change'] = combined_data['steel_price_mxn'].pct_change(1)
            
            # Import cost impact
            combined_data['import_cost_impact'] = combined_data['usd_mxn_rate'].pct_change(1)
        
        # Forward fill missing values
        combined_data = combined_data.fillna(method='ffill')
        combined_data = combined_data.fillna(method='bfill')
        
        # Remove rows with any remaining NaN values
        combined_data = combined_data.dropna()
        
        logger.info(f"✅ Combined dataset: {len(combined_data)} records with {len(combined_data.columns)} columns")
        logger.info(f"   Columns: {list(combined_data.columns)}")
        
        return combined_data
    
    def analyze_currency_impact_on_prices(self, data: pd.DataFrame) -> Dict:
        """Analyze the impact of currency fluctuations on steel prices."""
        logger.info("📊 Analyzing currency impact on steel prices...")
        
        analysis = {}
        
        if 'steel_price' in data.columns and 'usd_mxn_rate' in data.columns:
            # Correlation analysis
            correlation = data['steel_price'].corr(data['usd_mxn_rate'])
            analysis['price_currency_correlation'] = correlation
            
            # Volatility analysis
            price_vol = data['steel_price'].std()
            currency_vol = data['usd_mxn_rate'].std()
            analysis['price_volatility'] = price_vol
            analysis['currency_volatility'] = currency_vol
            analysis['volatility_ratio'] = price_vol / currency_vol if currency_vol > 0 else 0
            
            # Impact magnitude
            currency_changes = data['usd_mxn_rate'].pct_change().dropna()
            price_changes = data['steel_price'].pct_change().dropna()
            
            # Calculate average impact
            positive_currency_changes = currency_changes[currency_changes > 0]
            corresponding_price_changes = price_changes[positive_currency_changes.index]
            
            if len(corresponding_price_changes) > 0:
                analysis['average_price_impact_per_currency_change'] = corresponding_price_changes.mean()
        
        logger.info(f"✅ Currency impact analysis completed")
        return analysis


def main():
    """Test the enhanced data collector."""
    print("🏗️ Enhanced Data Collector - DeAcero Steel Rebar Predictor")
    print("=" * 60)
    
    collector = EnhancedDataCollector()
    
    # Collect and combine all data
    combined_data = collector.combine_all_data_with_currency_focus()
    
    if not combined_data.empty:
        print(f"✅ Data collection successful!")
        print(f"   Records: {len(combined_data)}")
        print(f"   Columns: {len(combined_data.columns)}")
        print(f"   Date range: {combined_data['date'].min()} to {combined_data['date'].max()}")
        
        # Analyze currency impact
        analysis = collector.analyze_currency_impact_on_prices(combined_data)
        print(f"\n📊 Currency Impact Analysis:")
        for key, value in analysis.items():
            print(f"   {key}: {value:.4f}")
        
        # Save data
        combined_data.to_csv('enhanced_steel_data_with_currency.csv', index=False)
        print(f"\n💾 Data saved to: enhanced_steel_data_with_currency.csv")
        
    else:
        print("❌ Data collection failed")


if __name__ == "__main__":
    main()
