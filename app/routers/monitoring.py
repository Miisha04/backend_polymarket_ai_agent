from fastapi import APIRouter

router = APIRouter(
    prefix="/monitoring",
    tags=["Monitoring"]
)

@router.get("/health")
async def health_check():
    return {"status": "ok"}
