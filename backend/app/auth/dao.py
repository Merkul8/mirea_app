from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import connection
from app.auth.models import User


class UserDAO:

    @classmethod
    @connection
    async def find_one_or_none(cls, email, session: AsyncSession) -> User:
        query = select(User).where(User.email == email)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    @connection
    async def create_user(cls, data, session: AsyncSession) -> User:
        query = insert(User).returning(User)
        result = await session.execute(query, data)
        await session.commit()
        return result.scalar_one_or_none()

    @classmethod
    @connection
    async def find_one_or_none_by_id(cls, user_id, session: AsyncSession) -> User:
        query = select(User).where(User.id == user_id)
        user = await session.execute(query)
        return user.scalar_one_or_none()
