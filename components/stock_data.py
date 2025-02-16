import yfinance as yf
import pandas as pd
from typing import Dict, Optional

def get_stock_data(symbol: str, period: str, interval: str) -> pd.DataFrame:
    """Fetch stock data using yfinance with error handling"""
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period=period, interval=interval)
        if df.empty:
            raise ValueError(f"No data found for symbol {symbol}")
        return df
    except Exception as e:
        raise ValueError(f"Error fetching data for {symbol}: {str(e)}")

def get_company_info(symbol: str) -> Dict[str, str]:
    """Get company information with error handling"""
    try:
        stock = yf.Ticker(symbol)
        info = stock.info

        if not info:
            return {
                'name': symbol,
                'description': 'No information available',
                'market_cap': 'N/A'
            }

        market_cap = info.get('marketCap', 0)
        if market_cap > 1e12:
            market_cap_str = f"${market_cap/1e12:.2f}T"
        elif market_cap > 1e9:
            market_cap_str = f"${market_cap/1e9:.2f}B"
        else:
            market_cap_str = f"${market_cap/1e6:.2f}M"

        return {
            'name': info.get('longName', symbol),
            'description': info.get('longBusinessSummary', 'No description available'),
            'market_cap': market_cap_str
        }
    except Exception as e:
        return {
            'name': symbol,
            'description': f'Error fetching company info: {str(e)}',
            'market_cap': 'N/A'
        }