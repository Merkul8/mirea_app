import uvicorn
from fastapi import FastAPI
from logger import logger
from contextlib import asynccontextmanager
from routing.routs import main_router
import config
from app.auth.auth import create_access_token


@asynccontextmanager
async def lifespan(app: FastAPI):



    logger.info("Сервер запущен")
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router=main_router)


if __name__ == "__main__":
    if config.MODE == "DEV":
        app_host = config.LOCAL_HOST
        app_port = config.LOCAL_PORT
    else:
        raise ValueError("Хост/Порт не определен")

    uvicorn.run(app, host=app_host, port=app_port, log_level="info")

