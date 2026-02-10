from fastapi import APIRouter, Depends, status
from .schema import UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register(user: UserCreate):
    return UserResponse(
        id=1,
        email=user.email,
        created_at="2026-02-10T22:30:00Z",
        updated_at="2026-02-10T22:30:00Z"
    )