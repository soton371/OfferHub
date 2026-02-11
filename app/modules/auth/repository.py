from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .model import User
from .schema import UserCreate

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user: UserCreate) -> User:
        print(f'UserRepository User data: {user}')
        db_user = User(email=user.email)
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def get_user_by_email(self, email: str) -> User | None:
        print(f'UserRepository get_user_by_email data: {email}')
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_users(self)-> list[User] | None:
        print(f"UserRepository get_users data")
        result = await self.db.execute(select(User))
        return result.scalars().all()

