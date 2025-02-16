import yfinance as yf
import pandas as pd

def get_stock_data(symbol: str, period: str, interval: str) -> pd.DataFrame:
    """Fetch stock data using yfinance"""
    stock = yf.Ticker(symbol)
    df = stock.history(period=period, interval=interval)
    return df

def get_company_info(symbol: str) -> dict:
    """Get company information"""
    stock = yf.Ticker(symbol)
    info = stock.info
    
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
