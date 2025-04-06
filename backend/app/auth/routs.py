from fastapi import APIRouter, HTTPException, status, Response, Depends

from app.auth.auth import get_password_hash, authenticate_user, create_access_token
from app.auth.dao import UserDAO
from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.auth.shemas import UserRegister, UserLogin

auth_router = APIRouter(tags=["Авторизация и аутентификация"])


@auth_router.post("/register/")
async def register_user(user_data: UserRegister) -> dict:
    user = await UserDAO.find_one_or_none(email=user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    user_data.password = get_password_hash(user_data.password)
    await UserDAO.create_user(user_data.dict())
    return {"message": f"Вы зарегистрированы в системе, на почту {user_data.email} придет сообщение об активации"}


@auth_router.post("/login/")
async def login_user(response: Response, user_data: UserLogin) -> dict:
    check = await authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверная почта или пароль')
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': None}


@auth_router.post("/logout/")
async def logout_user(response: Response) -> dict:
    response.delete_cookie(key="users_access_token")
    return {"message": "Logout done."}


@auth_router.get("/me/")
async def get_me(user_data: User = Depends(get_current_user)):
    return user_data


@auth_router.get("/users_to_activate/")
async def users_to_activate(user_data: User = Depends(get_current_user)):
    if user_data.is_superuser:
        users = await UserDAO.not_activated_users()
        return {"users": users}
    else:
        return {"status_code": 403, "message": "Недостаточно прав."}


@auth_router.post("/activate_user/")
async def activate_user(user_id: int, user_data: User = Depends(get_current_user)):
    if user_data.is_superuser:
        await UserDAO.activate_user_by_id(user_id=user_id)
        # send_message to user_id
        return {"status_code": 200, "message": f"Пользователь с id {user_id} активирован."}
    else:
        return {"status_code": 403, "message": "Недостаточно прав."}
