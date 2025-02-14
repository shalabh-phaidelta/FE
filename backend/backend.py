from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

API_KEY = ""
BASE_URL = "https://www.alphavantage.co/query"

@app.get("/stocks/{symbol}")
async def get_stock_data(symbol: str):
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    print("Raw API Response:", data)  # Debugging output

    if "Time Series (Daily)" not in data:
        raise HTTPException(status_code=400, detail="Invalid API response")

    time_series = data["Time Series (Daily)"]
    formatted_data = [
        {"date": date, "close": float(values["4. close"])}
        for date, values in time_series.items()
    ]

    print("Formatted Data:", formatted_data)  # Debugging output
    return formatted_data
