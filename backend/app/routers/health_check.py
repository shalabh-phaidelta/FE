from app.logging_config import get_logger
from fastapi import APIRouter

logger = get_logger(__name__)
router = APIRouter()


@router.get("/health")
async def health_check() -> dict:
    logger.info("Health check accessed")
    return {"status": "ok"}
