import streamlit as st
import pandas as pd
import numpy as np

def display_statistical_analysis(data: pd.DataFrame):
    """Display statistical analysis of the stock data"""
    st.subheader("Statistical Metrics")
    
    # Calculate metrics
    returns = data['Close'].pct_change()
    volatility = returns.std() * np.sqrt(252)
    sharpe_ratio = (returns.mean() * 252) / volatility
    
    metrics = {
        "Daily Returns (Mean)": f"{returns.mean()*100:.2f}%",
        "Volatility (Annual)": f"{volatility*100:.2f}%",
        "Sharpe Ratio": f"{sharpe_ratio:.2f}",
        "Maximum Drawdown": f"{((data['Close'].cummax() - data['Close'])/data['Close'].cummax()).max()*100:.2f}%"
    }
    
    for metric, value in metrics.items():
        st.metric(metric, value)

def display_momentum_indicators(data: pd.DataFrame):
    """Display momentum indicators"""
    st.subheader("Momentum Indicators")
    
    # Calculate momentum indicators
    momentum = data['Close'].diff(periods=20)
    rate_of_change = data['Close'].pct_change(periods=20) * 100
    
    metrics = {
        "20-day Momentum": f"{momentum.iloc[-1]:.2f}",
        "Rate of Change": f"{rate_of_change.iloc[-1]:.2f}%",
        "Price Change (%)": f"{((data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1) * 100:.2f}%"
    }
    
    for metric, value in metrics.items():
        st.metric(metric, value)
