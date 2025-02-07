import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load the data from the CSV
df = pd.read_csv("C:/Users/Neel/Desktop/Streamlit_Charts/stock_data.csv")

# Ensure that the 'Date' column is in datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Unpivot the data so that each stock name is turned into a row
df_unpivoted = pd.melt(df, id_vars=['Date'], var_name='Stock_Name', value_name='Stock_Price')

# Clean stock names: Take everything before the '.' delimiter and remove extra spaces
df_unpivoted['Clean_Stock_Name'] = df_unpivoted['Stock_Name'].apply(lambda x: x.split('.')[0].strip().title())

# Get unique cleaned stock names for the dropdown
stock_names = df_unpivoted['Clean_Stock_Name'].unique()

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
            width: 120px !important; 
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
filtered_df = df_unpivoted[(df_unpivoted['Date'] >= start_date) & 
                            (df_unpivoted['Date'] <= end_date)]

# Display the stock prices for the selected stock as well
if selected_stock:
    filtered_stock_df = df_unpivoted[(df_unpivoted['Clean_Stock_Name'] == selected_stock) & 
                                      (df_unpivoted['Date'] >= start_date) & 
                                      (df_unpivoted['Date'] <= end_date)]
    
    # Create a plotly figure for the selected stock
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=filtered_stock_df['Date'],
        y=filtered_stock_df['Stock_Price'],
        mode='lines', name=selected_stock,
        text=filtered_df['Stock_Price'].apply(lambda x: f'{x:.2f}'),  # Show stock price as labels
        textposition='top center',
        textfont=dict(size=10, color='black'),  # Customize font size and color of the labels
        hoverinfo='text',
        hovertext=filtered_stock_df.apply(lambda row: f"Date: {row['Date'].strftime('%Y-%m-%d')}<br>Price: {row['Stock_Price']:.2f}", axis=1)
    ))

    fig2.update_layout(
        title=f'{selected_stock} Stock Prices over Time',
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig2)

    # Find the top 3 stocks by average stock price
    top_3_stocks = filtered_df.groupby('Clean_Stock_Name')['Stock_Price'].mean().sort_values(ascending=False).head(3)

    # Plot the top 3 stocks as a bar chart
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=top_3_stocks.index,
        y=top_3_stocks.values,
        marker=dict(color='royalblue'),
        text=top_3_stocks.values.round(2),
        textposition='auto',
    ))

    # Update layout for the bar chart
    fig.update_layout(
        title='Top 3 Stocks by Average Price',
        template='plotly_dark'
    )

    # Display the bar chart
    st.plotly_chart(fig)

else:
    st.write("No data available for the selected range or stock.")
