import streamlit as st
import pandas as pd
import plotly.express as px
import nasdaqdatalink
import calendar
import datetime
import numpy as np

from datetime import date

def main():
    api_key = st.secrets["api_key"]
    nasdaqdatalink.ApiConfig.api_key = api_key
    mydata = nasdaqdatalink.get_table('QDL/OPEC')
    df = mydata.copy()

    st.markdown("<h6 style='text-align: center;'>Please select the time period </h6>", unsafe_allow_html=True)

    # First Graph
    st.markdown("---")
    st.subheader("Price of OPEC oil (barrel)")
    min_date = mydata['date'].min()
    
    start_date = st.date_input("Please define start date:", min_value=min_date)
    end_date = st.date_input("Please define end date:", min_value=min_date)

    if start_date > end_date:
        st.warning("Start date cannot be greater than end date.")
    elif start_date == end_date:
        st.warning("Start date and end date cannot be the same.")
    else:
        mask = df.loc[(df['date'] >= np.datetime64(start_date)) & (df['date'] <= np.datetime64(end_date))]
        fig1 = px.line(mask, x='date', y='value', labels={'value': 'Price'}, title='Price of OPEC oil (barrel)')
        st.plotly_chart(fig1)

    # Second Graph
    st.markdown("---")
    st.subheader("Average Monthly Oil Prices (barrel)")

    df.set_index('date', inplace=True)
    default_year = datetime.datetime.now().year
    years = st.multiselect('Select Years', list(df.index.year.unique()), default=[default_year])
    filtered_data = df[df.index.year.isin(years)]

    average_monthly_data = filtered_data.groupby([filtered_data.index.year, filtered_data.index.month]).mean()
    average_monthly_data.index.names = ['Year', 'Month']
    average_monthly_data.reset_index(inplace=True)
    average_monthly_data['Month'] = average_monthly_data['Month'].apply(lambda x: calendar.month_abbr[x])

    fig2 = px.line(average_monthly_data, x='Month', y='value', color='Year', labels={'value': 'Price'},
                   title='Average Monthly Oil Prices (barrel)')
    st.plotly_chart(fig2)

    # Data Source
    st.markdown("---")
    st.markdown("### Data Source:")
    st.markdown("<div> The data used is taken live from <a href='https://www.nasdaq.com/'> https://www.nasdaq.com/</a>. The live data is automatically updated based on OPEC dataset. <ul> <p>The <em>OPEC</em> is a comprehensive collection of crude oil prices declared by oil-producing countries over time.<li>Data is updated at 08:30 am ET Monday to Friday with the same day's data.</li> </ul></div>",
                unsafe_allow_html=True)

if __name__ == "__main__":
    main()
