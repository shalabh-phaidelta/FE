from nicegui import ui
import pandas as pd
import httpx
import asyncio

STOCK_SYMBOLS = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]  # Use working stock symbols
API_URL = "http://127.0.0.1:8000/stocks/{}"  # FastAPI endpoint

async def fetch_stock_data(symbol: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(API_URL.format(symbol))
        return response.json()

async def show_stock_data(_):
    stock_dfs = {}
    
    for symbol in STOCK_SYMBOLS:
        data = await fetch_stock_data(symbol)
        
        if isinstance(data, dict) and "detail" in data:
            ui.notify(f"Error fetching {symbol}: {data['detail']}")
            continue  # Skip symbol if API fails
        
        df = pd.DataFrame(data).set_index("date")
        stock_dfs[symbol] = df

    if not stock_dfs:
        ui.notify("No valid stock data fetched!")
        return

    # Merge all stock dataframes
    merged_df = pd.concat(stock_dfs, axis=1, keys=stock_dfs.keys())

    # Fix for KeyError: Ensure correct MultiIndex access
    try:
        merged_df = merged_df.xs('close', level=1, axis=1)
    except KeyError:
        ui.notify("Close price data not found in API response.")
        return

    # Display in UI
    with ui.card():
        ui.label("Stock Closing Prices")
        ui.table(columns=[{"name": s, "label": s, "field": s} for s in STOCK_SYMBOLS],
                 rows=merged_df.reset_index().to_dict(orient="records"))

# UI Layout
ui.label("Stock Data Viewer").classes("text-h4")
ui.button("Load Stock Data", on_click=show_stock_data)

ui.run(port=8080)
