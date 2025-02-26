# import json

# import pandas as pd
# import plotly.express as px
import requests
from nicegui import ui

response = requests.get("http://backend:8000/v1/health")
data = response.json()

# Display data from FastAPI
ui.label(f"Received from API: {data['status']}")

ui.run(port=8080)  # NiceGUI runs on port 8080

# Load stock data safely
# json_data = None
# try:
#     with open('../stock_data.json', 'r') as file:
#         json_data = json.load(file)

#     stock_data = json_data.get("price", [])  # Extract price history, default to empty list
#     company_name = json_data.get("ticker", "Unknown").upper()  # Default to "Unknown" if missing
# except Exception as e:
#     ui.notify(f'Error loading stock data: {e}', type='negative')
#     stock_data = []
#     company_name = "Unknown"  # Fallback if JSON fails to load

# # Convert JSON to DataFrame format
# if stock_data:
#     df = pd.DataFrame(stock_data)
#     if not {"date", "price"}.issubset(df.columns):
#         ui.notify("JSON data does not contain required columns.", type="negative")
#         df = pd.DataFrame(columns=["date", "price"])  # Empty dataframe fallback
# else:
#     df = pd.DataFrame(columns=["date", "price"])  # Handle empty data case

# df.rename(columns={"date": "Date", "price": "Price"}, inplace=True)  # Ensure correct column names

# table_data = df.to_dict(orient="records")  # Convert back to list of dictionaries

# # UI Layout
# with ui.row().classes('items-center justify-center w-full'):
#     ui.label(f'📈 {company_name} Stock Analysis Dashboard').
#                       classes('text-2xl font-bold mt-4 text-center')

# content_container = ui.column().classes('items-center')
# table_container = ui.column().classes('items-center w-full')
# chart_container = ui.row().classes('w-full justify-around')

# def center_title(fig, title):
#     fig.update_layout(
#         title={
#             'text': title,
#             'x': 0.5,
#             'xanchor': 'center',
#             'font': dict(size=18, family="Arial")
#         }
#     )
#     return fig

# def show_stock_data():
#     content_container.clear()
#     with content_container:
#         table_container.clear()
#         chart_container.clear()

#         if df.empty:
#             ui.notify("No stock data available.", type="warning")
#             return  # Stop execution if no data

#         # Display stock price table
#         with table_container:
#             ui.label(f'Showing Data for {company_name}').
#                           classes('text-lg font-semibold mt-2 text-center')
#             ui.table(
#                 rows=table_data,
#                 columns=[
#                     {'name': 'Date', 'label': 'Date', 'field': 'Date'},
#                     {'name': 'Price', 'label': 'Closing Price', 'field': 'Price'}
#                 ]
#             ).classes('w-3/4')

#         # Generate stock price trend chart
#         fig_line = center_title(px.line(df, x='Date', y='Price', markers=True,
#                                         color_discrete_sequence=['#4c72b0']),
#                                 f'{company_name} Stock Trend')

#         with chart_container:
#             ui.plotly(fig_line).classes('w-2/3')

# # Load and show data on UI start
# show_stock_data()

# # Run the UI
# ui.run()
