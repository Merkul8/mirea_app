from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
import enum

from sqlalchemy.orm import Mapped, validates

from database.db import Base



class EmployeeMetrics(Base):
    __tablename__ = "employee_metrics"

    id: Mapped[int] = Column(Integer, primary_key=True)
    publication_count: Mapped[int] = Column(Integer)
    user_id = Column(Integer, ForeignKey("user.id"))


class UserRole(enum.Enum):
    assistant = "Ассистент"
    teacher = "Преподаватель"
    department_chair = "Заведующий кафедрой"
    rector_office = "Ответственный от ректората"


class User(Base):

    __tablename__ = "user"

    id: Mapped[int] = Column(Integer, primary_key=True)
    first_name: Mapped[str] = Column(String)
    last_name: Mapped[str] = Column(String)
    patronymic: Mapped[str] = Column(String)
    email: Mapped[str] = Column(String)
    # academic_degree = Column(PgEnum(AcademicDegree, name="academic_degree", create_type=False), nullable=False)
    # scientific_field = Column(PgEnum(ScientificField, name="scientific_field", create_type=False), nullable=False)
    password: Mapped[str] = Column(String)
    role = Column(PgEnum(UserRole, name="role", create_type=False))
    departament_id = Column(Integer, ForeignKey("departament.id"))
    is_active: Mapped[bool] = Column(Boolean, default=False)
    is_superuser: Mapped[bool] = Column(Boolean, default=False)

    def __repr__(self):
        return f"User(id={self.id})"

    @validates("email")
    def validate_email(self, key, email):
        if "@" not in email:
            raise ValueError("email не прошел валидацию, отсутствует символ '@'.")
        return email


class Departament(Base):

    __tablename__ = "departament"

    id: Mapped[int] = Column(Integer, primary_key=True)
    title: Mapped[str] = Column(String)
    institute_id = Column(Integer, ForeignKey("institute.id"))

    def __repr__(self):
        return f"Departament(id={self.id})"


class Institute(Base):

    __tablename__ = "institute"

    id: Mapped[int] = Column(Integer, primary_key=True)
    title: Mapped[str] = Column(String)

    def __repr__(self):
        return f"Institute(id={self.id})"