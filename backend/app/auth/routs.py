from fastapi import APIRouter, HTTPException, status, Response, Depends, Cookie

from app.auth.auth import get_password_hash, authenticate_user, create_access_token, create_refresh_token, \
    refresh_access_token
from app.auth.dao import UserDAO, ActivateCodeDAO
from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.auth.shemas import UserRegister, UserLogin
from app.notification.sender import Sender
from background.worker import send_email

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
    code = await UserDAO.create_user(user_data.dict())
    # send_email.delay(subject="Код активации", to_email=user_data.email, content=code)
    await Sender.send(to_email=str(user_data.email), subject="Код активации", content=code)
    return {"message": f"Вы зарегистрированы в системе, на почту {user_data.email} придет сообщение об активации"}


@auth_router.post("/activate_account/")
async def activate_user(current_user: User = Depends(get_current_user)) -> dict:
    pass


@auth_router.post("/login/")
async def login_user(response: Response, user_data: UserLogin) -> dict:
    check = await authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверная почта или пароль')
    access_token = create_access_token({"sub": str(check.id)})
    refresh_token = create_refresh_token({"sub": str(check.id)})
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': refresh_token}


@auth_router.post("/refresh/")
async def refresh_user(response: Response, refresh_token: str = Cookie(None)) -> dict:
    new_access_token = await refresh_access_token(refresh_token)
    if new_access_token is not None:
        response.set_cookie(key="access_token", value=new_access_token, httponly=True)
        return {'access_token': new_access_token}
    else:
        return {"status": 500, "message": "Ошибка генерации нового refresh токена"}


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
