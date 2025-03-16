from pydantic import BaseModel, EmailStr, Field

from database.models import UserRole


class UserRegister(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")
    first_name: str = Field(..., min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    last_name: str = Field(..., min_length=3, max_length=50, description="Фамилия, от 3 до 50 символов")
    patronymic: str = Field(..., min_length=3, max_length=50, description="Отчество, от 3 до 50 символов")
    role: UserRole = Field(..., description="Роль")
    departament_id: int = Field(..., description="ID кафедры")