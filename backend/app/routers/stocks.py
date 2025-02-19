from fastapi import FastAPI, APIRouter, Query
from datetime import datetime, timedelta
from app.logging_config import logger
import random

router = APIRouter(
    prefix="/stocks",
    tags= ["Stocks"]

)

@router.get("/price_history")
def simulate_prices(ticker: str = Query(..., description="Ticker symbol"),
                    start_date:str = Query(..., description="Start date in YYYY-MM-DD format"),
                    end_date:str = Query(..., description="End date in YYYY-MM-DD format")
):
    try:
        logger.info(f"received request: ticker={ticker}, start_date={start_date}, end_date={end_date}")

        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        logger.info(f"Parsed dates: start={start}, end={end}")

        if start > end:
            logger.info("Error: start date must be before or equal to end date")
            return {"error": "start_date must be before or equal to end_date"}
        
        simulated_px_data = []
        price = random.uniform(50,150)
        logger.info(f"Initial price={price}")
        curr_date = start

        while curr_date <= end:
            fluctuation = random.uniform(0.98, 1.05)
            price *= fluctuation
            simulated_px_data.append(
                {
                    "date" : curr_date.strftime("%Y-%m-%d"),
                    "price" : round(price, 2)
            }
        )

            curr_date += timedelta(days=1)
        logger.info("simulated price data")
        return {"ticker": ticker, "price": simulated_px_data} 
    
    except ValueError as e:
        logger.info(f"Error: Invalid date format. {e}")
        return {"error": "Invalid date format. Use YYYY-MM-DD" }

    
