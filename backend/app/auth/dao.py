
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
    async def create_user(cls, data, session: AsyncSession) -> str:
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

        user_role = UserRole(user_id=user.id, role_id=role.id)
        session.add(user_role)
        await session.commit()
        activation_code = await ActivateCodeDAO.add_code(user_id=user.id)
        print(activation_code)
        await session.commit()
        return activation_code

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


class ActivateCodeDAO:

    @classmethod
    @connection
    async def add_code(cls, user_id: int, session: AsyncSession) -> str:
        instance = ActivateCode(user_id=user_id, code=str(randint(10000, 99999)))
        session.add(instance)
        await session.flush()
        return instance.code
