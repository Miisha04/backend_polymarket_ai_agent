from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.post("/invoke")
async def handle_chat_request(db: AsyncSession = Depends(get_session)):
    return {"message": "Chat endpoint is working. Ready for logic!"}