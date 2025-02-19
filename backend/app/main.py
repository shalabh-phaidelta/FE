from fastapi import FastAPI, Request
from app.routers import health_check, stocks
from app.logging_config import logger

app = FastAPI()

app.include_router(health_check.router)
app.include_router(stocks.router)

@app.get("/")
def hello():
    logger.info("Home route accessed")
    return {"message" : "Hello world!"}

logger.info("FastAPI app started successfully")

# @app.get("/health")
# async def get_health():
#     await health_check.health_check()
