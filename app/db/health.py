from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, APIRouter
from app.db.session import get_db

router = APIRouter()

@router.get("/health/db")
async def db_health(db: AsyncSession = Depends(get_db)):
    await db.execute(text("SELECT 1"))
    return {"database": "ok"}
