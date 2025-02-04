import pandas as pd
from nicegui import ui

# Load stock data from CSV (use the correct relative path to the CSV file)
stock_data = pd.read_csv('../stock_data.csv', parse_dates=['Date'], dayfirst=True)

# List of companies (based on the CSV columns)
companies = stock_data.columns[1:].tolist()

# Define the dropdown for company selection
company_dropdown = ui.select(companies, label='Select Company')

# Define function to display stock data based on selected company
def show_stock_data():
    symbol = company_dropdown.value
    if symbol:
        stock_data_filtered = stock_data[['Date', symbol]]
        ui.table(stock_data_filtered)

# UI layout
ui.label('Stock Analysis - Company Data')

company_dropdown.on('change', show_stock_data)

ui.run()