import streamlit as st
import pandas as pd
import ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def display_technical_analysis(data: pd.DataFrame):
    data['SMA20'] = ta.trend.sma_indicator(data['Close'], window=20)
    data['SMA50'] = ta.trend.sma_indicator(data['Close'], window=50)

    # Bollinger Bands
    data['BB_upper'] = ta.volatility.bollinger_hband(data['Close'], window=20, window_dev=2)
    data['BB_middle'] = ta.volatility.bollinger_mavg(data['Close'], window=20)
    data['BB_lower'] = ta.volatility.bollinger_lband(data['Close'], window=20, window_dev=2)

    # MACD
    data['MACD'] = ta.trend.macd_diff(data['Close'])
    data['MACD_signal'] = ta.trend.macd_signal(data['Close'])
    data['MACD_line'] = ta.trend.macd(data['Close'])

    # Stochastic Oscillator
    data['Stoch_k'] = ta.momentum.stoch(data['High'], data['Low'], data['Close'])
    data['Stoch_d'] = ta.momentum.stoch_signal(data['High'], data['Low'], data['Close'])

    # ATR and OBV
    data['ATR'] = ta.volatility.average_true_range(data['High'], data['Low'], data['Close'])
    data['OBV'] = ta.volume.on_balance_volume(data['Close'], data['Volume'])

    # Create tabs for different indicator groups
    tab1, tab2, tab3 = st.tabs(["🎯 Trend Indicators", "📊 Momentum", "📈 Volume & Volatility"])

    with tab1:
        # Bollinger Bands with Price
        fig_bb = go.Figure()
        fig_bb.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Price'))
        fig_bb.add_trace(go.Scatter(x=data.index, y=data['BB_upper'], name='BB Upper',
                                  line=dict(dash='dash')))
        fig_bb.add_trace(go.Scatter(x=data.index, y=data['BB_middle'], name='BB Middle',
                                  line=dict(dash='dash')))
        fig_bb.add_trace(go.Scatter(x=data.index, y=data['BB_lower'], name='BB Lower',
                                  line=dict(dash='dash')))
        fig_bb.update_layout(title='Bollinger Bands', height=500)
        st.plotly_chart(fig_bb, use_container_width=True)

        # MACD
        fig_macd = make_subplots(rows=2, cols=1, shared_xaxes=True,
                                vertical_spacing=0.1, row_heights=[0.7, 0.3])

        fig_macd.add_trace(go.Scatter(x=data.index, y=data['MACD_line'],
                                     name='MACD', line=dict(color='blue')), row=2, col=1)
        fig_macd.add_trace(go.Scatter(x=data.index, y=data['MACD_signal'],
                                     name='Signal', line=dict(color='orange')), row=2, col=1)
        fig_macd.add_trace(go.Bar(x=data.index, y=data['MACD'],
                                 name='MACD Histogram'), row=2, col=1)

        fig_macd.update_layout(title='MACD', height=700)
        st.plotly_chart(fig_macd, use_container_width=True)

    with tab2:
        # Stochastic Oscillator
        fig_stoch = go.Figure()
        fig_stoch.add_trace(go.Scatter(x=data.index, y=data['Stoch_k'],
                                      name='%K', line=dict(color='blue')))
        fig_stoch.add_trace(go.Scatter(x=data.index, y=data['Stoch_d'],
                                      name='%D', line=dict(color='orange')))

        # Add overbought/oversold lines
        fig_stoch.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="Overbought")
        fig_stoch.add_hline(y=20, line_dash="dash", line_color="green", annotation_text="Oversold")

        fig_stoch.update_layout(title='Stochastic Oscillator', height=400)
        st.plotly_chart(fig_stoch, use_container_width=True)

    with tab3:
        col1, col2 = st.columns(2)

        with col1:
            # ATR
            fig_atr = go.Figure()
            fig_atr.add_trace(go.Scatter(x=data.index, y=data['ATR'],
                                       name='ATR', line=dict(color='purple')))
            fig_atr.update_layout(title='Average True Range (ATR)', height=300)
            st.plotly_chart(fig_atr, use_container_width=True)

        with col2:
            # OBV
            fig_obv = go.Figure()
            fig_obv.add_trace(go.Scatter(x=data.index, y=data['OBV'],
                                       name='OBV', line=dict(color='green')))
            fig_obv.update_layout(title='On-Balance Volume (OBV)', height=300)
            st.plotly_chart(fig_obv, use_container_width=True)

        # Add explanations
        st.markdown("""
        ### Indicator Explanations:
        - **ATR (Average True Range)**: Measures market volatility by decomposing the entire range of an asset price for that period.
        - **OBV (On-Balance Volume)**: Measures buying and selling pressure as a cumulative indicator that adds volume on up days and subtracts it on down days.
        """)