from pprint import pprint

from fastapi import APIRouter, HTTPException, status, Response, Depends, Cookie, Query
from sqlalchemy.sql.functions import user
from starlette.responses import JSONResponse

from app.auth.auth import get_password_hash, authenticate_user, create_access_token, create_refresh_token, \
    refresh_access_token
from app.auth.dao import UserDAO, ActivateCodeDAO, RoleDAO, MetricsDAO
from app.auth.dependencies import get_current_user
from app.auth.models import User, UserRole, Publication
from app.auth.shemas import UserRegister, UserLogin, VerifyUser, UserMetric, DepartamentMetric
from app.notification.sender import Sender
from app.parsers.dao import ParserDAO
from app.parsers.services import ElibraryParser
from database.db import engine_session

auth_router = APIRouter(tags=["Авторизация и аутентификация"])


@auth_router.post("/register/")
async def register_user(user_data: UserRegister) -> dict:
    pprint(user_data)
    user = await UserDAO.find_one_or_none(email=user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    user_data.password = get_password_hash(user_data.password)
    code, user_id = await UserDAO.create_user(user_data.dict())
    # send_email.delay(subject="Код активации", to_email=user_data.email, content=code)
    await Sender.send(to_email=str(user_data.email), subject="Код активации", content=code)
    return {"message": f"Вы зарегистрированы в системе, на почту {user_data.email} придет сообщение об активации",
            "user_id": user_id}


@auth_router.post("/activate_account/")
async def activate_user(verify_data: VerifyUser) -> JSONResponse:
    user = await UserDAO.find_one_or_none_by_id(verify_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден в системе.")
    code_instance = await ActivateCodeDAO.get_by_id_or_none(user.id)
    if code_instance.code == verify_data.activation_code:
        await UserDAO.activate_user_email(user.id)
        content = {"message": f"Почта {user.email} пользователя с id {user.id} подтверждена."}
        return JSONResponse(content=content, status_code=200)
    else:
        content = {"message": f"Неверно введен код подтверждения почты."}
        return JSONResponse(content=content, status_code=404)


@auth_router.post("/login/")
async def login_user(response: Response, user_data: UserLogin) -> dict:
    check = await authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверная почта или пароль')
    if check.is_active:
        access_token = create_access_token({"sub": str(check.id)})
        refresh_token = create_refresh_token({"sub": str(check.id)})
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,  # Для HTTPS
            samesite='lax',  # Или 'none' если фронт и бек на разных доменах
            domain='localhost'
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,  # Для HTTPS
            samesite='lax',  # Или 'none' если фронт и бек на разных доменах
            domain='localhost'
        )
        return {'access_token': access_token, 'refresh_token': refresh_token}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Аккаунт ещё не активирован, ждите подтверждения администратором.")


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
    user_roles = await UserDAO.get_user_roles(user_id=user_data.id)
    return {
        "name": user_data.first_name,
        "last_name": user_data.last_name,
        "patronymic": user_data.patronymic,
        "email": user_data.email,
        "work_type": user_data.work_type,
        "academic_degree": user_data.academic_degree,
        "post": user_data.post,
        "elibrary_id": user_data.elibrary_id,
        "roles": user_roles
    }


@auth_router.patch("/add-role/")
async def add_role_to_user(
        user_id: int = Query(..., description="ID пользователя"),
        role_name: str = Query(..., description="Роль"),
        user: User = Depends(get_current_user)
) -> dict:
    if user.is_superuser:
        role = await RoleDAO.get_role_by_name(role_name)
        user = await UserDAO.find_one_or_none_by_id(user_id)
        user_roles = await UserDAO.get_user_roles(user_id=user.id)
        if role.name in user_roles:
            return {"status_code": 200, "message": f"У пользователя с id {user.id} уже есть роль {role.name}."}
        if user is None:
            raise HTTPException(status_code=404, detail=f"Пользователь с id {user_id} не найден.")
        if role is None:
            raise HTTPException(status_code=404, detail=f"Неправильно введена роль.")
        user_role = UserRole(role_id=role.id, user_id=user.id)
        await RoleDAO.add_user_role(user_role)
        return {"status_code": 200, "data": user_role.id}

    else:
        return {"status_code": 403, "message": "Недостаточно прав."}


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
        author_data = ElibraryParser(user_data.elibrary_id)
        data = author_data.elibrary_data()
        pprint(data)
        await ParserDAO.create_publications(data, user_data)
        # send_message to user_id
        return {"status_code": 200, "message": f"Пользователь с id {user_id} активирован."}
    else:
        return {"status_code": 403, "message": "Недостаточно прав."}


@auth_router.get("/department-users/")
async def department_users(user: User = Depends(get_current_user)):
    roles = await UserDAO.get_user_roles(user.id)
    if "boss" in roles:
        users = await UserDAO.get_users_by_departament(dep_id=user.departament_id)
        return {"data": [user.to_json() for user in users]}
    else:
        return {"status_code": 403, "message": "Недостаточно прав."}


# @auth_router.get("/users/{user_id}")
# async def get_users(user_id: int, current_user: User = Depends(get_current_user)):
#     user = await UserDAO.find_one_or_none_by_id(user_id)
#     return user


@auth_router.get("/metrics/{user_id}")
async def get_metrics(user_id: int, current_user: User = Depends(get_current_user)):
    roles = await UserDAO.get_user_roles(current_user.id)
    if "boss" in roles:
        metric = await MetricsDAO.get_metrics_by_user_id(user_id=user_id)
        return metric
    else:
        return {"status_code": 403, "message": "Недостаточно прав."}


@auth_router.patch("/metrics/update/{user_id}")
async def update_metrics(user_id: int, pub_count: int, current_user: User = Depends(get_current_user)):
    roles = await UserDAO.get_user_roles(current_user.id)
    if "boss" in roles:
        await MetricsDAO.update_metrics_by_user_id(user_id=user_id, pub_count=pub_count)
    else:
        return {"status_code": 403, "message": "Недостаточно прав."}


@auth_router.post("/metrics/create")
async def create_metrics(metric_data: UserMetric, current_user: User = Depends(get_current_user)):
    roles = await UserDAO.get_user_roles(current_user.id)
    if "boss" in roles:
        await MetricsDAO.create_metrics(metric_data.dict())
    else:
        return {"status_code": 403, "message": "Недостаточно прав."}


@auth_router.post("/metrics/departament/create")
async def create_metrics(metric_data: DepartamentMetric, current_user: User = Depends(get_current_user)):
    roles = await UserDAO.get_user_roles(current_user.id)
    if "boss" in roles:
        data = metric_data.dict()
        data["departament_id"] = current_user.departament_id
        await MetricsDAO.create_dep_metrics(data)
    else:
        return {"status_code": 403, "message": "Недостаточно прав."}


@auth_router.get("/user/publications/")
async def user_publications(current_user: User = Depends(get_current_user)):
    publications = await ParserDAO.get_user_publications(current_user.id)
    return {
        "data": [publication.to_dict() for publication in publications],
    }


@auth_router.get("/user/publications/read/{user_id}")
async def user_publications(user_id: int, current_user: User = Depends(get_current_user)):
    publications = await ParserDAO.get_user_publications(user_id)
    return {
        "data": [publication.to_dict() for publication in publications],
    }