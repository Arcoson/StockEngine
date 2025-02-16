import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
import pandas as pd

def plot_stock_price(data, symbol):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                       vertical_spacing=0.03, 
                       row_heights=[0.7, 0.3])

    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='OHLC'
        ),
        row=1, col=1
    )

    # Volume bar chart
    fig.add_trace(
        go.Bar(
            x=data.index,
            y=data['Volume'],
            name='Volume'
        ),
        row=2, col=1
    )

    # Update layout
    fig.update_layout(
        title=f'{symbol} Stock Price',
        yaxis_title='Stock Price (USD)',
        yaxis2_title='Volume',
        xaxis_rangeslider_visible=False,
        height=800,
        template='plotly_dark',
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

def plot_price_comparison(normalized_prices: dict, symbols: list):
    """Create a comparison chart of normalized prices"""
    fig = go.Figure()

    for symbol, prices in normalized_prices.items():
        fig.add_trace(
            go.Scatter(
                x=prices.index,
                y=prices,
                name=symbol,
                mode='lines',
                hovertemplate='%{y:.2f}%<extra></extra>'
            )
        )

    fig.update_layout(
        title='Relative Price Performance (%)',
        yaxis_title='Price Change (%)',
        height=600,
        template='plotly_dark',
        hovermode='x unified',
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)

def plot_volume_comparison(stocks_data: dict, symbols: list):
    """Create a comparison chart of trading volumes"""
    fig = go.Figure()

    for symbol, data in stocks_data.items():
        fig.add_trace(
            go.Bar(
                x=data.index,
                y=data['Volume'],
                name=symbol,
                visible='legendonly' if symbol != symbols[0] else True
            )
        )

    fig.update_layout(
        title='Volume Comparison',
        yaxis_title='Volume',
        height=400,
        template='plotly_dark',
        barmode='group',
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)