import enum
from contextlib import asynccontextmanager
from typing import Callable, Awaitable, Any


from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

import config
from logger import logger


try:
    engine = create_async_engine(url=config.get_db_url())

except Exception as e:
    logger.error(f"Ошибка подключеня к базе {repr(e)}")
    engine = None

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


@asynccontextmanager
async def engine_session():
    async with async_session_maker() as session:
        yield session


def connection(method: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
    async def wrapper(*args, **kwargs) -> Any:
        async with async_session_maker() as session:
            try:
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    return wrapper

