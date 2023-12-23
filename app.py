# Filename: app.py

import streamlit as st
from pages import visualization  # Import your visualization module
from pages import prediction

# Configure the page layout to remove the sidebar
st.set_page_config(layout="wide")

def main():
    st.title("Oil Price Tools")

    # Oil content
    st.write("Welcome to our Oil Price Tools application. Explore the latest oil prices and analysis.")

    # Tool selection
    tool_choice = st.selectbox("Choose an Oil Price Tool:", ["Live oil price visualization", "Live oil price prediction"])

    if tool_choice == "Live oil price visualization":
        visualization.main()
    elif tool_choice == "Live oil price prediction":
        prediction.main()

if __name__ == "__main__":
    main()
