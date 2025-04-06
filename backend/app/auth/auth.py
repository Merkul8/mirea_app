from datetime import datetime, timezone, timedelta

from passlib.context import CryptContext
from jose import jwt
from pydantic import EmailStr

from app.auth.dao import UserDAO
from config import get_auth_data

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)  # refresh token живёт дольше
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encoded_jwt = jwt.encode(to_encode, auth_data['refresh_secret_key'], algorithm=auth_data['algorithm'])
    return encoded_jwt

async def authenticate_user(email: EmailStr, password: str):
    user = await UserDAO.find_one_or_none(email=email)
    if not user or verify_password(plain_password=password, hashed_password=user.password) is False:
        return None
    return user


async def refresh_access_token(refresh_token: str):
    auth_data = get_auth_data()
    payload = jwt.decode(
        refresh_token,
        auth_data['refresh_secret_key'],
        algorithms=[auth_data['algorithm']]
    )
    user_id = payload.get("sub")  # или другой ключ, по которому хранится email
    if user_id is None:
        return None

    user = await UserDAO.find_one_or_none_by_id(user_id=user_id)
    if user is None:
        return None

    new_access_token = create_access_token(data={"sub": str(user.id)})
    return new_access_token

