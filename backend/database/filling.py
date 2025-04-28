from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import Role, Institute, Departament
from database.db import connection


@connection
async def add_roles(session: AsyncSession) -> None:
    roles_data = [
        {"name": "admin"},
        {"name": "boss"},
        {"name": "teacher"},
        {"name": "assistant"},
        {"name": "student"},
    ]

    # Создаем и выполняем запрос
    stmt = insert(Role).values(roles_data)
    await session.execute(stmt)
    await session.commit()

@connection
async def add_departments(session: AsyncSession) -> None:
    institutes = [
        Institute(
            title="Институт информационных технологий",
            departments=[
                Departament(title="Кафедра программирования"),
                Departament(title="Кафедра искусственного интеллекта")
            ]
        ),
        Institute(
            title="Институт экономики",
            departments=[
                Departament(title="Кафедра финансов"),
                Departament(title="Кафедра бухгалтерского учета")
            ]
        ),
        Institute(
            title="Институт перспективных технологий и индустриального программирования",
            departments=[
                Departament(title="Индустриальное программирование"),
                Departament(title="Индустриальное программирование(Front-end)")
            ]
        )
    ]

    session.add_all(institutes)
    await session.commit()
