from datetime import datetime

from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy.orm import validates

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy import Column, Integer, ForeignKey, Boolean, String, DateTime
import enum


class Base(AsyncAttrs, DeclarativeBase):
    pass


class UserRole(enum.Enum):
    assistant = "Ассистент"
    teacher = "Преподаватель"
    department_chair = "Заведующий кафедрой"
    rector_office = "Ответственный от ректората"


# class AcademicDegree(enum.Enum):
#     professor = "Профессор"
#     docent = "Доцент"
#     doctor = "Доктор"
#     graduate_student = "Аспирант"
#     teacher = "Преподаватель"
#
#
# class ScientificField(enum.Enum):
#     tech = "Технические науки"
#     phi_math = "Физико-математические науки"


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


class EmployeeMetrics(Base):
    __tablename__ = "employee_metrics"

    id: Mapped[int] = Column(Integer, primary_key=True)
    publication_count: Mapped[int] = Column(Integer)
    user_id = Column(Integer, ForeignKey("user.id"))


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


class ServiceType(enum.Enum):
    k1 = "К-1"
    k2 = "К-2"
    k3 = "К-3"
    q1 = "Q-1"
    q2 = "Q-2"
    other = "Прочее"

class PublicService(Base):

    __tablename__ = "public_service"

    id: Mapped[int] = Column(Integer, primary_key=True)
    title: Mapped[str] = Column(String)
    service_type: Mapped[str] = Column(
        PgEnum(
            ServiceType,
            name="service_type",
            create_type=False
               ),
        nullable=False
    )


class Publication(Base):

    __tablename__ = "publication"

    id: Mapped[int] = Column(Integer, primary_key=True)
    url: Mapped[str] = Column(String)
    title: Mapped[str] = Column(String)
    public_service_id = Column(Integer, ForeignKey("public_service.id"))
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.now())

    def __repr__(self):
        return f"User(id={self.id})"


class Report(Base):

    __tablename__ = "report"

    id: Mapped[int] = Column(Integer, primary_key=True)
    first_name: Mapped[str] = Column(String)
    last_name: Mapped[str] = Column(String)
    patronymic: Mapped[str] = Column(String)
    email: Mapped[str] = Column(String)
    password: Mapped[str] = Column(String)
    role = Column(PgEnum(UserRole, name="role", create_type=False))
    departament_id = Column(Integer, ForeignKey("departament.id"))
    is_active: Mapped[bool] = Column(Boolean, default=False)
    is_superuser: Mapped[bool] = Column(Boolean, default=False)

    def __repr__(self):
        return f"User(id={self.id})"