import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

def plot_stock_price(data, symbol):
    """Create an interactive stock price chart using Plotly"""
    fig = make_subplots(rows=2, cols=1, shared_xaxis=True, 
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
