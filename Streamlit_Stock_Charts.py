import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors

# Load the data from the CSV
df = pd.read_csv("C:/Users/Neel/Desktop/Streamlit_Charts/stock_data.csv")

# Ensure that the 'Date' column is in datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Unpivot the data so that each stock name is turned into a row
df_unpivoted = pd.melt(df, id_vars=['Date'], var_name='Stock_Name', value_name='Stock_Price')

# Get unique stock names for the dropdown
stock_names = df_unpivoted['Stock_Name'].unique()

# Add a slicer to filter the data based on a date range
start_date = st.date_input('Start date', min(df_unpivoted['Date']), key="start_date")
end_date = st.date_input('End date', max(df_unpivoted['Date']), key="end_date")

# Dropdown for selecting a stock name
selected_stock = st.selectbox('Select a stock', stock_names)

# Filter the data based on the selected stock and date range
filtered_df = df_unpivoted[(df_unpivoted['Stock_Name'] == selected_stock) & 
                            (df_unpivoted['Date'] >= pd.to_datetime(start_date)) & 
                            (df_unpivoted['Date'] <= pd.to_datetime(end_date))]

# Check if there is any data after filtering
if not filtered_df.empty:
    # Create a line chart using matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create a line chart with 'Date' on the x-axis and the selected stock's price on the y-axis
    ax.plot(filtered_df['Date'], filtered_df['Stock_Price'], color='skyblue', linewidth=2)

    # Set labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel('Stock Price')
    ax.set_title(f'{selected_stock} Stock Prices over Time')

    # Rotate x-axis labels for better visibility
    plt.xticks(rotation=45)

    # Add tooltips with mplcursors: show the Date, Stock Price, and Stock Name
    mplcursors.cursor(ax, hover=True).connect("add", lambda sel: sel.annotation.set_text(
        f"Date: {filtered_df['Date'].iloc[sel.index].strftime('%Y-%m-%d')}\n"
        f"Price: {filtered_df['Stock_Price'].iloc[sel.index]:.2f}\n"
        f"Stock: {selected_stock}"
    ))

    # Show the chart in Streamlit app
    st.pyplot(fig)
else:
    st.write("No data available for the selected range or stock.")
