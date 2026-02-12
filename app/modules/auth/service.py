from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import UserRepository
from .schema import UserCreate, UserUpdate, UserSearch
from .model import User
from typing import Annotated
from app.db.session import get_db


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = UserRepository(db)

    async def create_user(self, data: UserCreate) -> User:
        print(f'Service create_user data: {data}')
        existing = await self.repository.get_by_email(data.email)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
        return await self.repository.create(User(**data.model_dump()))

    async def get_users(self, search: UserSearch) -> list[User]:
        print(f"Service get_users data: {search}")
        return await self.repository.get_all(search)

    async def get_user(self, id: int) -> User:
        print(f"Service get_user data: {id}")
        user = await self.repository.get_by_id(id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    async def delete_user(self, id: int) -> User:
        print(f"Service delete_user data: {id}")
        user = await self.repository.get_by_id(id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return await self.repository.delete(user)

    async def update_user(self, id: int, data: UserUpdate) -> User:
        print(f"Service update_user data: {id}")
        user = await self.repository.get_by_id(id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user.name = data.name
        return await self.repository.update(user)


async def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(db)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
