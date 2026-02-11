from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import UserRepository
from .schema import UserCreate
from .model import User


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register(self, data: UserCreate) -> User:
        print(f'Service User data: {data}')
        repository = UserRepository(self.db)
        existing = await repository.get_user_by_email(data.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")

        user = User(email=data.email)
        return await repository.create(user)