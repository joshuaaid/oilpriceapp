import streamlit as st
st.set_option('deprecation.showPyplotGlobalUse', False)
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
from prophet import Prophet
import nasdaqdatalink
import time

def main():
    api_key = st.secrets["api_key"]
    nasdaqdatalink.ApiConfig.api_key = api_key
    mydata = nasdaqdatalink.get_table('QDL/OPEC')
    df = mydata.copy()
    df.columns = ['ds', 'y']

    st.title("Live Oil prediction analysis via Prophet model")

    st.markdown("<h6 style='text-align: center;'>Please select the time period to capture seasonality patterns and build model</h6>", unsafe_allow_html=True)
    # Slider for user input
    forecast_days = st.slider("Number of days to forecast", min_value=1, max_value=365, value=30)

    # Fit the Prophet model
    model = Prophet()
    model.fit(df)
    
    # Make a future dataframe for forecast
    future = model.make_future_dataframe(periods=forecast_days)

    # Forecast
    forecast = model.predict(future)

    # Plot actual data points, forecasted values, and uncertainty intervals
    fig1 = model.plot(forecast)
    plt.title('Actual vs Forecasted Values with Uncertainty Intervals')
    plt.legend(['Actual price', 'Predicted prices', 'Uncertainty intervals'])
    st.pyplot(fig1)
    time.sleep(1)
    st.success("Model successfully built!")

    st.markdown("<h6 style='text-align: center;'>Please select the time period to get prediction </h6>", unsafe_allow_html=True)

    min_date = df['ds'].min()  

    start_date = st.date_input("Please define start date:", min_value=min_date)
    end_date = st.date_input("Please define end date:", min_value=min_date)

    if start_date > end_date:
        st.warning("Start date cannot be greater than end date.")
    elif start_date == end_date:
        st.warning("Start date and end date cannot be the same.")
    else:
        # Filter forecast dataframe based on user-selected date range
        cmp_df = forecast.set_index('ds')[['yhat', 'yhat_lower', 'yhat_upper']].join(df.set_index('ds'))
        cmp_df_filtered = cmp_df.loc[start_date:end_date]

        # Convert the index to datetime format
        cmp_df_filtered.index = pd.to_datetime(cmp_df_filtered.index)

        # Display the filtered dataframe with custom column names and formatted date
        st.write("Depending on your selection, the data for the last 20 days is displayed in the table:")
        cmp_df_filtered.columns = ['Forecasted Value', 'Lower Bound', 'Upper Bound', 'Actual Value']
        
        # Center the table on the page
        st.table(cmp_df_filtered.tail(20))
        

        
        # Plot the actual, forecasted, and uncertainty intervals with rotated x-axis labels
        fig2, ax2 = plt.subplots()
        ax2.plot(cmp_df_filtered.index, cmp_df_filtered['Forecasted Value'], label='Forecasted Value')
        ax2.fill_between(cmp_df_filtered.index, cmp_df_filtered['Lower Bound'], cmp_df_filtered['Upper Bound'], color='gray', alpha=0.2, label='Uncertainty Intervals')
        ax2.plot(cmp_df_filtered.index, cmp_df_filtered['Actual Value'], label='Actual Value', linestyle='--', color='red')
        ax2.legend()
        
        # Rotate x-axis labels
        plt.xticks(rotation=45, ha='right')
        
        plt.title('Actual vs Forecasted Values with Uncertainty Intervals')
        st.pyplot(fig2)


if __name__ == "__main__":
    main()
