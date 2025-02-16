import streamlit as st
import pandas as pd
import ta

def display_technical_analysis(data: pd.DataFrame):
    """Display technical analysis indicators"""
    # Add technical indicators
    data['SMA20'] = ta.trend.sma_indicator(data['Close'], window=20)
    data['SMA50'] = ta.trend.sma_indicator(data['Close'], window=50)
    data['RSI'] = ta.momentum.rsi(data['Close'], window=14)
    data['MACD'] = ta.trend.macd_diff(data['Close'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Moving Averages")
        st.line_chart(data[['Close', 'SMA20', 'SMA50']].tail(100))
        
    with col2:
        st.subheader("RSI")
        rsi_chart = pd.DataFrame({'RSI': data['RSI']}).tail(100)
        st.line_chart(rsi_chart)
        
    st.subheader("MACD")
    macd_chart = pd.DataFrame({'MACD': data['MACD']}).tail(100)
    st.line_chart(macd_chart)
