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
    Analyze and compare stocks with interactive charts and technical indicators. 
    Enter stock symbols to begin your analysis.
""")

# Sidebar
with st.sidebar:
    st.header("Configuration")

    # Multiple stock selection
    symbols_input = st.text_input("Enter Stock Symbols (comma-separated)", "AAPL, MSFT").upper()
    symbols = [sym.strip() for sym in symbols_input.split(',')]

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

# Create tabs for single stock analysis and comparison
tab1, tab2 = st.tabs(["Single Stock Analysis", "Stock Comparison"])

with tab1:
    # Single stock analysis (original functionality)
    try:
        main_symbol = symbols[0]
        stock = stock_data.get_stock_data(main_symbol, period, interval)
        company_info = stock_data.get_company_info(main_symbol)

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
        tab1_1, tab1_2 = st.tabs(["📈 Price Chart", "📊 Technical Analysis"])

        with tab1_1:
            charts.plot_stock_price(stock, main_symbol)

        with tab1_2:
            technical_analysis.display_technical_analysis(stock)

        # Mathematical Analysis
        st.header("Mathematical Analysis")
        col1, col2 = st.columns(2)

        with col1:
            calculations.display_statistical_analysis(stock)

        with col2:
            calculations.display_momentum_indicators(stock)

        # Company Information
        st.header("Company Information")
        st.markdown(f"""
        **{company_info['name']}**\n
        {company_info['description']}
        """)

    except Exception as e:
        st.error(f"Error: Unable to fetch data for symbol '{main_symbol}'. Please check if the symbol is correct.")
        st.exception(e)

with tab2:
    try:
        # Load data for all symbols
        stocks_data = {symbol: stock_data.get_stock_data(symbol, period, interval) for symbol in symbols}

        # Performance Comparison
        st.header("Performance Comparison")

        # Normalize prices for comparison
        normalized_prices = {}
        for symbol, data in stocks_data.items():
            first_price = data['Close'].iloc[0]
            normalized_prices[symbol] = (data['Close'] / first_price - 1) * 100

        # Create comparison chart
        charts.plot_price_comparison(normalized_prices, symbols)

        # Key Metrics Comparison
        st.header("Key Metrics Comparison")
        metrics_df = calculations.compare_key_metrics(stocks_data)
        st.dataframe(metrics_df)

        # Volume Comparison
        st.header("Volume Comparison")
        charts.plot_volume_comparison(stocks_data, symbols)

    except Exception as e:
        st.error("Error: Unable to compare stocks. Please check if all symbols are correct.")
        st.exception(e)