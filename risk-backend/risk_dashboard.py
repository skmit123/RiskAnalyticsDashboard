print("runnnig")
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns

st.title("📈 Risk Analytics Dashboard")

ticker = st.text_input("Enter Ticker Symbol", "AAPL")

if st.button("Fetch Data"):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1y")

    if data.empty:
        st.error("Invalid ticker or data not available")
    else:
        st.subheader(f"{ticker} Closing Price Chart")
        st.line_chart(data["Close"])

        # compute returns
        returns = data["Close"].pct_change().dropna()

        # risk metrics
        volatility = returns.std() * np.sqrt(252)
        avg_return = returns.mean() * 252
        sharpe_ratio = (avg_return - 0.03) / volatility
        var_95 = returns.mean() - norm.ppf(0.95)*returns.std()

        # show metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Volatility", f"{volatility:.4f}")
        col2.metric("Sharpe Ratio", f"{sharpe_ratio:.4f}")
        col3.metric("VaR (95%)", f"{var_95:.4f}")
        col4.metric("Avg Annual Return", f"{avg_return:.4f}")

        # returns distribution
        st.subheader("Return Distribution")
        fig, ax = plt.subplots()
        sns.histplot(returns, bins=40, kde=True, ax=ax)
        st.pyplot(fig)
