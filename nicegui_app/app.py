import pandas as pd
from nicegui import ui
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Load stock data
try:
    stock_data = pd.read_csv('../stock_data.csv', parse_dates=['Date'], dayfirst=True)
except Exception as e:
    ui.notify(f'Error loading stock data: {e}', type='negative')

# Extract company names from CSV headers
companies = stock_data.columns[1:].tolist()

# UI Layout
ui.label('📈 Stock Analysis Dashboard').classes('text-2xl font-bold mt-4')

# Create a dropdown with a default selection
selected_company = ui.select(['All Companies'] + companies, value='All Companies').classes('w-64').props('label="Select a Company"')

# Empty UI elements for table and chart
table_container = ui.column()

# Function to update UI when a company is selected
def show_stock_data(_):
    company = selected_company.value
    table_container.clear()

    if company == 'All Companies':
        # Display all data
        with table_container:
            ui.label('Showing Data for All Companies').classes('text-lg font-semibold mt-2')
            ui.table(
                rows=stock_data.to_dict('records'),
                columns=[{'name': col, 'label': col, 'field': col} for col in stock_data.columns]
            ).classes('w-full')

    elif company in companies:
        # Display data for the selected company
        stock_filtered = stock_data[['Date', company]]

        with table_container:
            ui.label(f'Showing Data for {company}').classes('text-lg font-semibold mt-2')
            ui.table(
                rows=stock_filtered.to_dict('records'),
                columns=[
                    {'name': 'Date', 'label': 'Date', 'field': 'Date'},
                    {'name': company, 'label': 'Closing Price', 'field': company}
                ]
            ).classes('w-full')

# Attach event listener to dropdown
selected_company.on('update:model-value', show_stock_data)

# Initial load trigger to show all data
show_stock_data(None)

# Run the UI
ui.run()