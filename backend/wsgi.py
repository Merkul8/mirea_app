from pprint import pprint

import uvicorn
from fastapi import FastAPI
from logger import logger
from contextlib import asynccontextmanager

import config
from app.auth.dao import UserDAO
from app.auth.routs import auth_router
from app.report.routs import report_router
from app.notification.sender import Sender
from app.parsers.dao import ParserDAO
from app.parsers.scripts.publication_services_types import services_categories_to_db
from app.parsers.services import ElibraryParser
from database.filling import add_roles, add_departments


@asynccontextmanager
async def lifespan(app: FastAPI):

    # await services_categories_to_db()
    # await add_roles()
    # await add_departments()

    # await Sender.send(
    #     to_email="max.merkulov.00@mail.ru",
    #     subject="TEST",
    #     content="TEST",
    # )
    # user = await UserDAO.find_one_or_none_by_id(user_id=1)
    # author_data = ElibraryParser(user.elibrary_id)
    # data = author_data.elibrary_data()
    # pprint(data)
    # await ParserDAO.create_publications(data, user)

    logger.info("Сервер запущен")
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router=auth_router)
app.include_router(router=report_router)

if __name__ == "__main__":
    if config.MODE == "DEV":
        app_host = config.LOCAL_HOST
        app_port = config.LOCAL_PORT
    else:
        raise ValueError("Хост/Порт не определен")

    uvicorn.run(app, host=app_host, port=app_port, log_level="info")

