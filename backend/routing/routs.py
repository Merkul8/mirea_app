from fastapi import APIRouter, HTTPException, status, Response, Depends

from app.auth.auth import get_password_hash, authenticate_user, create_access_token
from app.auth.dao import UserDAO
from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.auth.shemas import UserRegister, UserLogin

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


@main_router.post("/login/")
async def login_user(response: Response, user_data: UserLogin) -> dict:
    check = await authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверная почта или пароль')
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': None}


@main_router.post("/logout/")
async def logout_user(response: Response) -> dict:
    response.delete_cookie(key="users_access_token")
    return {"message": "Logout done."}


@main_router.get("/me/")
async def get_me(user_data: User = Depends(get_current_user)):
    return user_data


