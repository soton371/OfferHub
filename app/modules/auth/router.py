from fastapi import APIRouter, Depends, status
from .schema import UserCreate, UserResponse
from .service import AuthService
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    print(f'Router User data: {data}')
    service = AuthService(db)
    return await service.register(data)