import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import nasdaqdatalink
import calendar
import datetime
# Specify the path to your text file containing the API key
file_path = "api key.txt"

# Read the API key from the text file
with open(file_path, "r") as file:
    api_key = file.read().strip()

# Set the API key
nasdaqdatalink.ApiConfig.api_key = api_key
mydata = nasdaqdatalink.get_table('QDL/OPEC')

df = mydata.copy()

df.set_index('date', inplace=True)
# Set default selected year to the current year
default_year = datetime.datetime.now().year

# Sidebar: Year selection with default value
years = st.sidebar.multiselect('Select Years', list(df.index.year.unique()), default=[default_year])

# Filter data based on selected years
filtered_data = df[df.index.year.isin(years)]

# Calculate average value for each month
average_monthly_data = filtered_data.groupby([filtered_data.index.year, filtered_data.index.month]).mean()
average_monthly_data.index.names = ['Year', 'Month']
average_monthly_data.reset_index(inplace=True)
average_monthly_data['Month'] = average_monthly_data['Month'].apply(lambda x: calendar.month_abbr[x])

# Main content: Line chart with average prices for each month
st.markdown("<h6 style='text-align: center;'>Average Monthly Oil Prices (barrel) </h6>", unsafe_allow_html=True)
fig, ax = plt.subplots()

for year in years:
    subset = average_monthly_data[average_monthly_data['Year'] == year]
    ax.plot(subset['Month'], subset['value'], label=str(year))

ax.set_xlabel('Month')
ax.set_ylabel('Price')
ax.legend()

# Display the plot using Streamlit
st.pyplot(fig)

# Data Source
st.markdown("---")
st.markdown("### Data Source:")
st.markdown("<div> The data used is taken live from <a href='https://www.nasdaq.com/'> https://www.nasdaq.com/</a>. The live data is automatically updated based on OPEC dataset. <ul> <p>The <em>OPEC</em> is a comprehensive collection of crude oil prices declared by oil-producing countries over time.<li>Data is updated at 08:30am ET Monday to Friday with the same day's data.</li> </ul></div>", unsafe_allow_html=True)
