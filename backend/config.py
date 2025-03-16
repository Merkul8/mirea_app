import os
from dotenv import load_dotenv

load_dotenv()

MODE = os.getenv("MODE")
LOCAL_PORT = os.getenv("LOCAL_PORT")
LOCAL_HOST = os.getenv("LOCAL_HOST")

DB_HOST=os.getenv("DB_HOST")
DB_PORT=os.getenv("DB_PORT")
DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_NAME=os.getenv("DB_NAME")


def get_db_url():
    return (f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")