import streamlit as st
from pages import visualization  
from pages import prediction
from pages import stock

st.set_page_config(layout="wide")

def main():
    st.title("Oil Price Tools")
    st.write("Welcome to our Oil Price Tools application. Explore the latest oil prices and analysis.")
    tool_choice = st.selectbox("Choose an Oil Price Tool:", ["Live oil price visualization", "Live oil price prediction","Stock analysis"])

    if tool_choice == "Live oil price visualization":
        visualization.main()
    elif tool_choice == "Live oil price prediction":
        prediction.main()
    elif tool_choice == "Stock analysis":
        stock.main()
if __name__ == "__main__":
    main()
