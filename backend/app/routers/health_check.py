from fastapi import APIRouter


router = APIRouter(
    prefix="/health_check",
    tags = ["Health Check"]
)

@router.get("/health")
async def health_check():
    return {"status" : "ok"}