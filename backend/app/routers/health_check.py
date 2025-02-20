from app.logging_config import logger
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check() -> dict:
    logger.info("Helath check accessed")
    return {"status": "ok"}
