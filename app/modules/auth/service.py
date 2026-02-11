from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import UserRepository
from .schema import UserCreate, UserSearch
from .model import User
from typing import Annotated
from app.db.session import get_db


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = UserRepository(db)

    async def register(self, data: UserCreate) -> User:
        print(f'Service User data: {data}')
        existing = await self.repository.get_user_by_email(data.email)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
        return await self.repository.create(User(**data.model_dump()))

    async def get_users(self, search: UserSearch) -> list[User]:
        print(f"Service get_users data: {search}")
        return await self.repository.get_users(search)



async def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(db)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
