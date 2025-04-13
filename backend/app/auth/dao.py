from typing import Sequence

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import connection
from app.auth.models import User, Role, UserRole


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
        role = await session.execute(
            select(Role).where(Role.name == data.get("role"))
        )
        role = role.scalar_one_or_none()
        if not role:
            raise ValueError("Не передана роль пользователя.")
        user = User(**data)
        user.roles.append(role)
        session.add(user)
        await session.flush()

        user_role = UserRole(user_id=user.id, role_id=role.id)
        session.add(user_role)

        await session.commit()

        return user

    @classmethod
    @connection
    async def find_one_or_none_by_id(cls, user_id: int, session: AsyncSession) -> User:
        query = select(User).where(User.id == int(user_id))
        user = await session.execute(query)
        return user.scalar_one_or_none()

    @classmethod
    @connection
    async def not_activated_users(cls, session: AsyncSession) -> Sequence[User]:
        query = select(User).where(User.is_active == False)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    @connection
    async def activate_user_by_id(cls, user_id: int, session: AsyncSession):
        print(f"Активация пользователя {user_id}")
        stmt = update(User).where(User.id == user_id).values(is_active=True)
        result = await session.execute(stmt)
        await session.commit()
        print(result)
        return result.rowcount