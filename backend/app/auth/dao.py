from typing import Sequence

from sqlalchemy import select, update
from random import randint
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import connection
from app.auth.models import User, Role, UserRole, ActivateCode, Departament, EmployeeMetrics


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
        stmt = update(User).where(User.id == user_id).values(is_active=True)
        result = await session.execute(stmt)
        await session.commit()
        return result.rowcount

    @classmethod
    @connection
    async def activate_user_email(cls, user_id, session: AsyncSession):
        stmt = update(User).where(User.id == user_id).values(is_active_email=True)
        await session.execute(stmt)
        await session.commit()

    @classmethod
    @connection
    async def get_users_by_departament(cls, dep_id: int, session: AsyncSession) -> Sequence[User]:
        query = select(User).join(Departament, Departament.id == User.departament_id).where(Departament.id == dep_id)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    @connection
    async def get_user_roles(cls, user_id: int, session: AsyncSession) -> list[str]:
        query = select(Role).join(
            UserRole, UserRole.role_id == Role.id).join(
            User, User.id == UserRole.user_id).where(
            User.id == user_id)
        result = await session.execute(query)
        return [instance.name for instance in result.scalars().all()]


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


class DepartamentDAO:

    @classmethod
    @connection
    async def dep_by_id(cls, dep_id: int, session: AsyncSession) -> Departament:
        query = select(Departament).where(Departament.id == dep_id)
        result = await session.execute(query)
        return result.scalar()


class RoleDAO:

    @classmethod
    @connection
    async def get_role_by_name(cls, name: str, session: AsyncSession) -> Role:
        query = select(Role).where(Role.name == name)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    @connection
    async def add_user_role(cls, role: UserRole, session: AsyncSession) -> None:
        session.add(role)
        await session.commit()


class MetricsDAO:

    @classmethod
    @connection
    async def get_metrics_by_user_id(cls, user_id: int, session: AsyncSession) -> EmployeeMetrics:
        query = select(EmployeeMetrics).where(EmployeeMetrics.user_id == user_id)
        result = await session.execute(query)
        return result.scalars().first()

    @classmethod
    @connection
    async def update_metrics_by_user_id(cls, user_id: int, pub_count: int, session: AsyncSession) -> None:
        stmt = update(EmployeeMetrics).where(EmployeeMetrics.user_id == user_id).values(publication_count=pub_count)
        await session.execute(stmt)
        await session.commit()

    @classmethod
    @connection
    async def create_metrics(cls, user_id: int, pub_count: int, session: AsyncSession) -> None:
        instance = EmployeeMetrics(user_id=user_id, publication_count=pub_count)
        session.add(instance)
        await session.commit()
