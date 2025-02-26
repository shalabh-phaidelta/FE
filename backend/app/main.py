from app.logging_config import get_logger
from app.routers import health_check, stocks
from fastapi import FastAPI

logger = get_logger(__name__)

app = FastAPI()

app.include_router(health_check.router, prefix="/v1", tags=["health"])
app.include_router(stocks.router, prefix="/v1", tags=["stocks"])


@app.get("/")
def hello() -> dict:
    logger.info("Home route accessed")
    return {"message": "Hello world!"}


logger.info("FastAPI app started successfully")

# @app.get("/health")
# async def get_health():
#     await health_check.health_check()
