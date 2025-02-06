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
chart_container = ui.column()

# Function to update UI when a company is selected
def show_stock_data(_):
    company = selected_company.value
    table_container.clear()
    chart_container.clear()

    if company == 'All Companies':
        # Display all data
        with table_container:
            ui.label('Showing Data for All Companies').classes('text-lg font-semibold mt-2')
            ui.table(
                rows=stock_data.to_dict('records'),
                columns=[{'name': col, 'label': col, 'field': col} for col in stock_data.columns]
            ).classes('w-full')

        # Show combined plot for all companies
        with chart_container:
            ui.label('📈 Stock Trends for All Companies').classes('text-lg font-semibold text-gray-800 mb-2')
            fig, ax = plt.subplots(figsize=(8, 4))
            for comp in companies:
                ax.plot(stock_data['Date'], stock_data[comp], label=comp)

            ax.set_title('Stock Prices Over Time')
            ax.set_xlabel('Date')
            ax.set_ylabel('Closing Price')
            ax.legend(loc='upper left', fontsize='small')
            ax.grid(True)

            # Convert Matplotlib plot to image
            img_buf = BytesIO()
            plt.savefig(img_buf, format='png')
            img_buf.seek(0)
            img_base64 = base64.b64encode(img_buf.read()).decode('utf-8')
            plt.close()

            ui.image(f"data:image/png;base64,{img_base64}").classes('w-full')

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

        with chart_container:
            ui.label(f'📈 {company} Stock Trend').classes('text-lg font-semibold text-gray-800 mb-2')
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(stock_filtered['Date'], stock_filtered[company], marker='o', linestyle='-')
            ax.set_title(f'{company} Closing Price Over Time')
            ax.set_xlabel('Date')
            ax.set_ylabel('Closing Price')
            ax.grid(True)

            # Convert plot to image
            img_buf = BytesIO()
            plt.savefig(img_buf, format='png')
            img_buf.seek(0)
            img_base64 = base64.b64encode(img_buf.read()).decode('utf-8')
            plt.close()

            ui.image(f"data:image/png;base64,{img_base64}").classes('w-full')

# Attach event listener to dropdown
selected_company.on('update:model-value', show_stock_data)

# Initial load trigger to show all data
show_stock_data(None)

# Run the UI
ui.run()