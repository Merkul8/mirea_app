
from typing import Sequence

from sqlalchemy import select, update
from random import randint
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import connection
from app.auth.models import User, Role, UserRole, ActivateCode


class UserDAO:

    @classmethod
    @connection
    async def find_one_or_none(cls, email, session: AsyncSession) -> User:
        query = select(User).where(User.email == email)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    @connection
    async def create_user(cls, data, session: AsyncSession) -> tuple[str, int]:
        role = await session.execute(
            select(Role).where(Role.name == data.get("role"))
        )
        role = role.scalar_one_or_none()
        if not role:
            raise ValueError("Не передана роль пользователя.")
        del data["role"]
        user = User(**data)
        user.roles.append(role)
        session.add(user)
        await session.flush()

        activation_code = await ActivateCodeDAO.add_code(user_id=user.id, session=session)
        await session.commit()
        return activation_code, user.id

    @classmethod
    @connection
    async def find_one_or_none_by_id(cls, user_id: int, session: AsyncSession) -> User:
        query = select(User).where(User.id == int(user_id))
        user = await session.execute(query)
        return user.scalar_one_or_none()

    @classmethod
    @connection
    async def not_activated_users(cls, session: AsyncSession) -> Sequence[User]:
        query = select(User).where(
            User.is_active == False,
            User.is_active_email == True
        )
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

    @classmethod
    @connection
    async def activate_user_email(cls, user_id, session: AsyncSession):
        stmt = update(User).where(User.id == user_id).values(is_active_email=True)
        await session.execute(stmt)
        await session.commit()


class ActivateCodeDAO:

    @classmethod
    async def add_code(cls, user_id: int, session: AsyncSession) -> str:
        instance = ActivateCode(user_id=user_id, code=str(randint(10000, 99999)))
        session.add(instance)
        await session.flush()
        return instance.code

    @classmethod
    @connection
    async def get_by_id_or_none(cls, user_id: int, session: AsyncSession) -> ActivateCode:
        query = select(ActivateCode).where(ActivateCode.user_id == user_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()
