from fastapi import APIRouter, HTTPException, status

from app.auth.auth import get_password_hash
from app.auth.dao import UserDAO
from app.auth.shemas import UserRegister

main_router = APIRouter(tags=["Публикационная Активность МИРЭА"])



@main_router.post("/register/")
async def register_user(user_data: UserRegister) -> dict:
    user = await UserDAO.find_one_or_none(email=user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    user_data.password = get_password_hash(user_data.password)
    await UserDAO.create_user(user_data.dict())
    return {'message': 'Вы успешно зарегистрированы!'}