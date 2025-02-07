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
with ui.row().classes('items-center'):
    ui.label('📈 Stock Analysis Dashboard').classes('text-2xl font-bold mt-4')
    selected_company = ui.select(['All Companies'] + companies, value='All Companies').classes('w-64 ml-4').props('label="Select a Company"')

# Empty UI elements for table and chart
content_container = ui.column()
table_container = ui.column()
pagination_container = ui.column()
chart_container = ui.column()

# Pagination parameters
ROWS_PER_PAGE = 10

# Function to update UI when a company is selected
def show_stock_data(_):
    company = selected_company.value
    content_container.clear()

    with content_container:
        table_container.clear()
        pagination_container.clear()
        chart_container.clear()

        if company == 'All Companies':
            # Display all data
            total_pages = (len(stock_data) + ROWS_PER_PAGE - 1) // ROWS_PER_PAGE

            def update_table(page):
                start = (page - 1) * ROWS_PER_PAGE
                end = start + ROWS_PER_PAGE
                page_data = stock_data.iloc[start:end]
                table_container.clear()
                with table_container:
                    ui.label('Showing Data for All Companies').classes('text-lg font-semibold mt-2')
                    ui.table(
                        rows=page_data.to_dict('records'),
                        columns=[{'name': col, 'label': col, 'field': col} for col in stock_data.columns]
                    ).classes('w-full')

            update_table(1)

            with pagination_container:
                p = ui.pagination(1, total_pages, direction_links=True)
                p.on('update:model-value', lambda e: update_table(p.value))

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
            total_pages = (len(stock_filtered) + ROWS_PER_PAGE - 1) // ROWS_PER_PAGE

            def update_table(page):
                start = (page - 1) * ROWS_PER_PAGE
                end = start + ROWS_PER_PAGE
                page_data = stock_filtered.iloc[start:end]
                table_container.clear()
                with table_container:
                    ui.label(f'Showing Data for {company}').classes('text-lg font-semibold mt-2')
                    ui.table(
                        rows=page_data.to_dict('records'),
                        columns=[
                            {'name': 'Date', 'label': 'Date', 'field': 'Date'},
                            {'name': company, 'label': 'Closing Price', 'field': company}
                        ]
                    ).classes('w-full')

            update_table(1)

            with pagination_container:
                p = ui.pagination(1, total_pages, direction_links=True)
                p.on('update:model-value', lambda e: update_table(p.value))

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