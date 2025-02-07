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

# Set the range for the slider based on the minimum and maximum dates in the dataset
min_date = min(df_unpivoted['Date']).date()  # Convert to datetime.date
max_date = max(df_unpivoted['Date']).date()  # Convert to datetime.date

# Custom CSS to reduce the size of the date pickers
st.markdown("""
    <style>
        .stDateInput > label {
            font-size: 12px !important;
        }
        .stDateInput input {
            font-size: 15px !important;
            padding: 5px !important;
            height: 25px !important;
            width: 120px !important;  /* Reducing the width */
        }
    </style>
""", unsafe_allow_html=True)

# Create two columns for the date pickers
col1, col2 = st.columns(2)

# Display the Start and End Date Pickers horizontally
with col1:
    start_date_picker = st.date_input('Start Date', min_date, key="start_date_picker")
with col2:
    end_date_picker = st.date_input('End Date', max_date, key="end_date_picker")

# Link slider to date range: Create a date range slider
start_date_slider, end_date_slider = st.slider(
    'Select Date Range',
    min_value=min_date,
    max_value=max_date,
    value=(start_date_picker, end_date_picker),  # Default value to the selected range from date pickers
    format="YYYY-MM-DD"
)

# When the slider changes, update the date pickers
start_date_picker = start_date_slider
end_date_picker = end_date_slider

# Convert start and end date pickers to pandas Timestamps to match the 'Date' column in df_unpivoted
start_date = pd.to_datetime(start_date_picker)
end_date = pd.to_datetime(end_date_picker)

# Dropdown for selecting a stock name
selected_stock = st.selectbox('Select a stock', stock_names)

# Filter the data based on the selected stock and date range
filtered_df = df_unpivoted[(df_unpivoted['Stock_Name'] == selected_stock) & 
                            (df_unpivoted['Date'] >= start_date) & 
                            (df_unpivoted['Date'] <= end_date)]

# Check if there is any data after filtering
if not filtered_df.empty:
    # Create a line chart using matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create a line chart with 'Date' on the x-axis and the selected stock's price on the y-axis
    ax.plot(filtered_df['Date'], filtered_df['Stock_Price'], color='skyblue', linewidth=2)

    # Add data labels on each point
    for i, row in filtered_df.iterrows():
        ax.text(row['Date'], row['Stock_Price'], f'{row["Stock_Price"]:.2f}', 
                ha='center', va='bottom', fontsize=8, color='black')

    # Set labels and title
   
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
