import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict

def display_statistical_analysis(data: pd.DataFrame):
    """Display statistical analysis of the stock data"""
    try:
        st.subheader("Statistical Metrics")

        # Calculate metrics with proper error handling
        returns = data['Close'].pct_change().dropna()

        if len(returns) == 0:
            st.warning("Not enough data to calculate metrics")
            return

        volatility = returns.std() * np.sqrt(252) if len(returns) > 0 else 0
        avg_return = returns.mean() if len(returns) > 0 else 0
        sharpe_ratio = (avg_return * 252) / volatility if volatility != 0 else 0

        max_drawdown = 0
        if len(data['Close']) > 0:
            peak = data['Close'].expanding(min_periods=1).max()
            drawdown = (peak - data['Close']) / peak
            max_drawdown = drawdown.max()

        metrics = {
            "Daily Returns (Mean)": f"{avg_return*100:.2f}%",
            "Volatility (Annual)": f"{volatility*100:.2f}%",
            "Sharpe Ratio": f"{sharpe_ratio:.2f}",
            "Maximum Drawdown": f"{max_drawdown*100:.2f}%"
        }

        for metric, value in metrics.items():
            st.metric(metric, value)

    except Exception as e:
        st.error(f"Error calculating statistical metrics: {str(e)}")

def display_momentum_indicators(data: pd.DataFrame):
    """Display momentum indicators"""
    try:
        st.subheader("Momentum Indicators")

        if len(data) < 20:
            st.warning("Not enough data points for momentum calculation")
            return

        # Calculate momentum indicators with proper type checking
        momentum = data['Close'].diff(periods=20).iloc[-1] if len(data) >= 20 else 0

        # Calculate rate of change
        price_20_days_ago = data['Close'].iloc[-20] if len(data) >= 20 else data['Close'].iloc[0]
        current_price = data['Close'].iloc[-1]
        rate_of_change = ((current_price / price_20_days_ago) - 1) * 100 if price_20_days_ago != 0 else 0

        # Calculate overall price change
        first_price = data['Close'].iloc[0]
        price_change = ((current_price / first_price) - 1) * 100 if first_price != 0 else 0

        metrics = {
            "20-day Momentum": f"{momentum:.2f}",
            "Rate of Change": f"{rate_of_change:.2f}%",
            "Price Change (%)": f"{price_change:.2f}%"
        }

        for metric, value in metrics.items():
            st.metric(metric, value)

    except Exception as e:
        st.error(f"Error calculating momentum indicators: {str(e)}")