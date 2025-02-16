import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
from components import stock_data, technical_analysis, charts
from utils import calculations

st.set_page_config(
    page_title="Stock Analysis Dashboard",
    page_icon="📈",
    layout="wide"
)

# Custom CSS
with open('styles/custom.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# App title and description
st.title('📈 Advanced Stock Analysis Dashboard')
st.markdown("""
    Analyze stocks with interactive charts and technical indicators. 
    Enter a stock symbol to begin your analysis.
""")

# Sidebar
with st.sidebar:
    st.header("Configuration")
    symbol = st.text_input("Enter Stock Symbol", "AAPL").upper()
    period = st.select_slider(
        "Time Period",
        options=['1mo', '3mo', '6mo', '1y', '2y', '5y'],
        value='1y'
    )
    
    interval = st.select_slider(
        "Interval",
        options=['1d', '1wk', '1mo'],
        value='1d'
    )

try:
    # Load stock data
    stock = stock_data.get_stock_data(symbol, period, interval)
    
    # Company info
    company_info = stock_data.get_company_info(symbol)
    
    # Display company overview
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Price", f"${stock['Close'].iloc[-1]:.2f}", 
                 f"{((stock['Close'].iloc[-1] - stock['Close'].iloc[-2])/stock['Close'].iloc[-2]*100):.2f}%")
    with col2:
        st.metric("Market Cap", company_info['market_cap'])
    with col3:
        st.metric("Volume", f"{stock['Volume'].iloc[-1]:,}")
    
    # Main charts
    st.header("Price Analysis")
    tab1, tab2 = st.tabs(["📈 Price Chart", "📊 Technical Analysis"])
    
    with tab1:
        # Interactive price chart
        charts.plot_stock_price(stock, symbol)
        
    with tab2:
        # Technical indicators
        technical_analysis.display_technical_analysis(stock)
    
    # Mathematical Analysis
    st.header("Mathematical Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        calculations.display_statistical_analysis(stock)
        
    with col2:
        calculations.display_momentum_indicators(stock)
    
    # Additional company information
    st.header("Company Information")
    st.markdown(f"""
    **{company_info['name']}**\n
    {company_info['description']}
    """)

except Exception as e:
    st.error(f"Error: Unable to fetch data for symbol '{symbol}'. Please check if the symbol is correct.")
    st.exception(e)
