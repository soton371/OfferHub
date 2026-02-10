from fastapi import APIRouter, Depends, status
from .schema import UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    return {
        "email": user.email
    }