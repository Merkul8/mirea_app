from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse, FileResponse

from app.auth.dao import UserDAO
from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.report.services import Report

report_router = APIRouter(tags=["Генерация отчета"])


@report_router.post("/reports/user")
async def user_report(
        user_id: int,
        current_user: User = Depends(get_current_user)
):
    user = await UserDAO.find_one_or_none_by_id(user_id)
    if not user:
        JSONResponse(status_code=404, content={"message": f"Нет пользователя с id {user_id}"})
    report = Report(user=user)
    file_name = await report.get_user_report()
    print(file_name)
    return FileResponse(path=f"C:\\Users\merku\PycharmProjects\mirea_app\\backend\static\\{file_name}", filename=file_name)


@report_router.post("/reports/departament")
async def departament_report(
        current_user: User = Depends(get_current_user)
):
    users = await UserDAO.get_users_by_departament(current_user.departament_id)
    if not users:
        JSONResponse(status_code=404, content={"message": f"Не найдено пользователей с такой кафедрой."})
    report = Report(users=users)
    file_name = await report.get_users_report()
    print(file_name)
    return FileResponse(path=f"C:\\Users\merku\PycharmProjects\mirea_app\\backend\static\\{file_name}", filename=file_name)