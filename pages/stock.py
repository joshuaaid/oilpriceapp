import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime
import yfinance as yf


def main():
    st.markdown("<h6 style='text-align: center;'>Please select the time period </h6>", unsafe_allow_html=True)
    st.markdown("---")
    min_date = datetime(1996, 1, 1)
    start_date = st.date_input("Please define start date:",min_value=min_date)
    end_date = st.date_input("Please define end date:",min_value=min_date)
    if start_date > end_date:
        st.warning("Start date cannot be greater than end date.")
    elif start_date == end_date:
        st.warning("Start date and end date cannot be the same.")
    else:
        symbols = ["TSLA", "AAPL","AMD","PYPL","META","GOOG","MSFT","JPM","WMT","XOM","JNJ"]
        symbol_filter = st.multiselect('Please select the stocks to visualize:', symbols, default=['AAPL'])
        print(type(symbol_filter)
        if len(symbol_filter) == 0:
            st.warning("Please select at least one stock.")
        else:
            data = yf.download(symbol_filter, start=start_date, end=end_date)
            adj_close_data = data['Adj Close']
            fig1 = px.line(adj_close_data, labels={'value': 'Adjusted Close Price','variable' : 'Stock'})
            st.plotly_chart(fig1)
              # Data Source
            st.markdown("---")
            st.markdown("### Data Source:")
            st.markdown("<div> The data used is taken live from <a href='https://finance.yahoo.com/'> finance.yahoo.com </a>. The stock prices are updated regularly and in real-time. </div>",
                unsafe_allow_html=True)
if __name__ == "__main__":
    main()
