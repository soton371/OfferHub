from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, asc
from .model import User
from .schema import UserCreate, UserSearch

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db



    async def get_user_by_email(self, email: str) -> User | None:
        print(f'UserRepository get_user_by_email data: {email}')
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_user_by_id(self, id: int) -> User | None:
        print(f'UserRepository get_user_by_id data: {id}')
        result = await self.db.execute(select(User).where(User.id == id))
        return result.scalar_one_or_none()


    async def create(self, user: UserCreate) -> User:
        print(f'UserRepository User data: {user}')
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete(self, user: User) -> User:
        print(f'UserRepository delete data: {user}')
        await self.db.delete(user)
        await self.db.commit()
        return user


    async def get_users(self, search: UserSearch) -> list[User]:
        print(f"UserRepository get_users data: {search}")
        query = select(User)

        if search.email:
            query = query.where(User.email.contains(search.email))

        if search.sort_by:
            sort_column = getattr(User, search.sort_by, User.created_at)
            if search.sort_order == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))

        offset = (search.page - 1) * search.limit
        query = query.offset(offset).limit(search.limit)

        result = await self.db.execute(query)
        return result.scalars().all()

