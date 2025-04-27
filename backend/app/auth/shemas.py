from pydantic import BaseModel, EmailStr, Field

from app.auth.models import UserRole


class UserRegister(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")
    first_name: str = Field(..., min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    last_name: str = Field(..., min_length=3, max_length=50, description="Фамилия, от 3 до 50 символов")
    patronymic: str = Field(..., min_length=3, max_length=50, description="Отчество, от 3 до 50 символов")
    elibrary_id: int = Field(..., description="ID пользователя в системе elibrary.")
    role: str = Field(..., description="Роль")
    work_type: str = Field(..., description="Тип трудоустройства")
    post: str = Field(..., description="Должность")
    academic_degree: str = Field(..., description="Ученая степень")
    departament_id: int = Field(..., description="ID кафедры")


class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")
