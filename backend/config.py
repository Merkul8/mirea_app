import os
from dotenv import load_dotenv

load_dotenv()

MODE = os.getenv("MODE")
LOCAL_PORT = int(os.getenv("LOCAL_PORT"))
LOCAL_HOST = os.getenv("LOCAL_HOST")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
CATEGORIES_PUBLIC_SERVICES_PATH = os.getenv("CATEGORIES_PUBLIC_SERVICES_PATH")

REDIS_URL = os.getenv("REDIS_URL")


def get_db_url():
    return f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def get_auth_data():
    return {"secret_key": os.getenv("SECRET_KEY"), "refresh_secret_key": os.getenv("REFRESH_SECRET_KEY"), "algorithm": os.getenv("ALGORITHM")}

def smtp_data():
    return {"login": os.getenv("email_login"), "password": os.getenv("email_password")}
