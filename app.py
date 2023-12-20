import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import nasdaqdatalink
import calendar
import datetime

from datetime import date
import numpy as np
api_key = st.secrets["api_key"]
# Set the API key
api_key = st.secrets["api_key"]
nasdaqdatalink.ApiConfig.api_key = api_key
mydata = nasdaqdatalink.get_table('QDL/OPEC')
df = mydata.copy()
st.markdown("<h6 style='text-align: center;'>Please select the years to compare average prices </h6>", unsafe_allow_html=True)
fig1, ax1 = plt.subplots()
# Adding labels and title
ax1.set_xlabel('Time')
ax1.set_ylabel('Price')
ax1.set_title('Price of OPEC oil (barrel)')

# Set the default value for the date input widget to the minimum date in the DataFrame
min_date = mydata['date'].min()
max_date = mydata['date'].max()

#default_date = mydata['date'].max()
# Create date input widget for start date with limits
#start_date = st.date_input("Please define start date:", min_value=mydata['date'].min())
#end_date = st.date_input("Please define end date:",  max_value= mydata['date'].max(), value = default_date)

start_date = st.date_input("Please define start date:", min_value = min_date)
end_date = st.date_input("Please define end date:",  min_value = min_date, max_value = max_date )

if start_date > end_date:
    st.warning("Start date cannot be greater than end date.")
elif start_date == end_date:
    st.warning("Start date and end date cannot be the same.")
else:
    mask = df[(df['date'] >= np.datetime64(start_date) ) & (df['date'] <= np.datetime64(end_date))]
    ax1.plot(mask['date'],mask['value'])
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=60, ha='right')

# Displaying the plot using Streamlit
st.pyplot(fig1)



#The second graph
st.markdown("---")
st.markdown("<h6 style='text-align: center;'>Please select the years to compare average prices </h6>", unsafe_allow_html=True)
df.set_index('date', inplace=True)
# Year selection with default value
# Set default selected year to the current year
default_year = datetime.datetime.now().year
years = st.multiselect('Select Years', list(df.index.year.unique()), default=[default_year])

# Filter data based on selected years
filtered_data = df[df.index.year.isin(years)]

# Calculate average value for each month
average_monthly_data = filtered_data.groupby([filtered_data.index.year, filtered_data.index.month]).mean()
average_monthly_data.index.names = ['Year', 'Month']
average_monthly_data.reset_index(inplace=True)
average_monthly_data['Month'] = average_monthly_data['Month'].apply(lambda x: calendar.month_abbr[x])

# Main content: Line chart with average prices for each month
st.markdown("<h6 style='text-align: center;'>Average Monthly Oil Prices (barrel) </h6>", unsafe_allow_html=True)
fig2, ax2 = plt.subplots()

for year in years:
    subset = average_monthly_data[average_monthly_data['Year'] == year]
    ax2.plot(subset['Month'], subset['value'], label=str(year))

ax2.set_xlabel('Month')
ax2.set_ylabel('Price')
ax2.legend()

# Display the plot using Streamlit
st.pyplot(fig2)

# Data Source
st.markdown("---")
st.markdown("### Data Source:")
st.markdown("<div> The data used is taken live from <a href='https://www.nasdaq.com/'> https://www.nasdaq.com/</a>. The live data is automatically updated based on OPEC dataset. <ul> <p>The <em>OPEC</em> is a comprehensive collection of crude oil prices declared by oil-producing countries over time.<li>Data is updated at 08:30am ET Monday to Friday with the same day's data.</li> </ul></div>", unsafe_allow_html=True)
