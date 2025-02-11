import pandas as pd
from nicegui import ui
import plotly.express as px

# Load stock data
try:
    stock_data = pd.read_csv('../stock_data.csv', parse_dates=['Date'], dayfirst=True)
except Exception as e:
    ui.notify(f'Error loading stock data: {e}', type='negative')

# Extract company names from CSV headers
companies = stock_data.columns[1:].tolist()

# Calculate 7-day moving averages for each company (but don't show in table)
for comp in companies:
    stock_data[f'{comp} 7-Day MA'] = stock_data[comp].rolling(window=7).mean()

# UI Layout
with ui.row().classes('items-center justify-center w-full'):
    ui.label('📈 Stock Analysis Dashboard').classes('text-2xl font-bold mt-4 text-center')
    selected_company = ui.select(['All Companies'] + companies, value='All Companies').classes('w-64 mt-2').props('label="Select a Company"')

# Containers for UI elements
content_container = ui.column().classes('items-center')
table_container = ui.column().classes('items-center w-full')
pagination_container = ui.column().classes('items-center justify-center w-full')
chart_container = ui.row().classes('w-full justify-around')

ROWS_PER_PAGE = 10

def center_title(fig, title):
    fig.update_layout(
        title={
            'text': title, 
            'x': 0.5, 
            'xanchor': 'center',
            'font': dict(size=18, family="Arial", weight="bold")  # bold title
        }
    )
    return fig

def show_stock_data(_):
    company = selected_company.value
    content_container.clear()

    with content_container:
        table_container.clear()
        pagination_container.clear()
        chart_container.clear()

        if company == 'All Companies':
            total_pages = (len(stock_data) + ROWS_PER_PAGE - 1) // ROWS_PER_PAGE

            def update_table(page):
                start = (page - 1) * ROWS_PER_PAGE
                end = start + ROWS_PER_PAGE
                page_data = stock_data.iloc[start:end]
                table_container.clear()
                with table_container:
                    ui.label('Showing Data for All Companies').classes('text-lg font-semibold mt-2 text-center')
                    ui.table(
                        rows=page_data.to_dict('records'),
                        columns=[{'name': col, 'label': col, 'field': col} for col in ['Date'] + companies]
                    ).classes('w-3/4')

            update_table(1)
            with pagination_container:
                p = ui.pagination(1, total_pages, direction_links=True)
                p.on('update:model-value', lambda e: update_table(p.value))

            # Charts for All Companies
            fig_line = center_title(px.line(stock_data, x='Date', y=companies, color_discrete_sequence=px.colors.qualitative.Safe), 'Stock Prices Over Time')
            fig_bar = center_title(px.bar(x=companies, y=[stock_data.iloc[-1][comp] for comp in companies], color_discrete_sequence=['#4c72b0']), 'Latest Closing Prices')
            fig_pie = center_title(px.pie(values=[stock_data.iloc[-1][comp] for comp in companies], names=companies, hole=0.4, color_discrete_sequence=px.colors.sequential.Blues), 'Stock Price Distribution')
            fig_volatility = center_title(px.box(stock_data[companies]), 'Stock Price Volatility')
            fig_correlation = center_title(px.imshow(stock_data[companies].corr(), color_continuous_scale='RdBu'), 'Stock Correlation Heatmap')

            with chart_container:
                ui.plotly(fig_line).classes('w-2/3')
                ui.plotly(fig_bar).classes('w-2/3')
                ui.plotly(fig_pie).classes('w-1/3')
                ui.plotly(fig_volatility).classes('w-2/3')
                ui.plotly(fig_correlation).classes('w-2/3')

        elif company in companies:
            stock_filtered = stock_data[['Date', company, f'{company} 7-Day MA']]
            total_pages = (len(stock_filtered) + ROWS_PER_PAGE - 1) // ROWS_PER_PAGE

            def update_table(page):
                start = (page - 1) * ROWS_PER_PAGE
                end = start + ROWS_PER_PAGE
                page_data = stock_filtered[['Date', company]].iloc[start:end]  # No 7-Day MA column
                table_container.clear()
                with table_container:
                    ui.label(f'Showing Data for {company}').classes('text-lg font-semibold mt-2 text-center')
                    ui.table(
                        rows=page_data.to_dict('records'),
                        columns=[
                            {'name': 'Date', 'label': 'Date', 'field': 'Date'},
                            {'name': company, 'label': 'Closing Price', 'field': company}
                        ]
                    ).classes('w-3/4')

            update_table(1)
            with pagination_container:
                p = ui.pagination(1, total_pages, direction_links=True)
                p.on('update:model-value', lambda e: update_table(p.value))

            # Charts for Selected Company
            fig_line = center_title(px.line(stock_filtered, x='Date', y=company, color_discrete_sequence=['#4c72b0']), f'{company} Stock Trend')
            fig_bar = center_title(px.bar(stock_filtered, x='Date', y=company, color_discrete_sequence=['#4c72b0']), f'{company} Closing Prices')
            fig_pie = center_title(px.pie(values=[stock_filtered[company].iloc[-1]], names=[company], hole=0.4, color_discrete_sequence=['#4c72b0']), 'Stock Price Share')
            fig_moving_avg = center_title(px.line(stock_filtered, x='Date', y=[company, f'{company} 7-Day MA'], color_discrete_sequence=['#4c72b0', '#ff6f61']), f'{company} 7-Day Moving Average')
            fig_histogram = center_title(px.histogram(stock_filtered, x=company, nbins=20, color_discrete_sequence=['#4c72b0']), f'{company} Price Distribution')

            with chart_container:
                ui.plotly(fig_line).classes('w-2/3')
                ui.plotly(fig_bar).classes('w-2/3')
                ui.plotly(fig_pie).classes('w-1/3')
                ui.plotly(fig_moving_avg).classes('w-2/3')
                ui.plotly(fig_histogram).classes('w-2/3')

# Attach event listener to dropdown
selected_company.on('update:model-value', show_stock_data)

# Initial load trigger to show all data
show_stock_data(None)

# Run the UI
ui.run()
