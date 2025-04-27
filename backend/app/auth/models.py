from datetime import datetime
from typing import List
import enum
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy.orm import Mapped, validates, relationship, mapped_column

from database.db import Base



class EmployeeMetrics(Base):
    __tablename__ = "employee_metrics"

    id: Mapped[int] = Column(Integer, primary_key=True)
    publication_count: Mapped[int] = Column(Integer)
    user_id = Column(Integer, ForeignKey("user_mirea.id"))


class Role(Base):
    __tablename__ = "role"
    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String, unique=True)
    users: Mapped[List["User"]] = relationship(secondary="user_role", back_populates="roles")

    def __repr__(self):
        return f"Role(name={self.name})"


class UserRole(Base):
    __tablename__ = "user_role"

    id: Mapped[int] = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey("role.id"), index=True)
    user_id = Column(Integer, ForeignKey("user_mirea.id"), index=True)


class User(Base):

    __tablename__ = "user_mirea"

    id: Mapped[int] = Column(Integer, primary_key=True)
    first_name: Mapped[str] = Column(String)
    last_name: Mapped[str] = Column(String)
    patronymic: Mapped[str] = Column(String)
    email: Mapped[str] = Column(String)
    elibrary_id: Mapped[int] = Column(Integer)
    password: Mapped[str] = Column(String)
    departament_id = Column(Integer, ForeignKey("departament.id"))
    is_active_email: Mapped[bool] = Column(Boolean, default=False)
    is_active: Mapped[bool] = Column(Boolean, default=False)
    is_superuser: Mapped[bool] = Column(Boolean, default=False)
    work_type: Mapped[str] = Column(String)
    post: Mapped[str] = Column(String)
    academic_degree: Mapped[str] = Column(String)


    roles: Mapped[List["Role"]] = relationship(secondary="user_role", back_populates="users")
    publications: Mapped[List["Publication"]] = relationship(secondary="user_publication", back_populates="users")

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
    institute: Mapped["Institute"] = relationship(back_populates="departments")

    def __repr__(self):
        return f"Departament(id={self.id})"


class Institute(Base):

    __tablename__ = "institute"

    id: Mapped[int] = Column(Integer, primary_key=True)
    title: Mapped[str] = Column(String)
    departments: Mapped[list["Departament"]] = relationship(back_populates="institute")

    def __repr__(self):
        return f"Institute(id={self.id})"


class ActivateCode(Base):
    __tablename__ = "activate_code"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_mirea.id"), index=True, unique=True)
    code: Mapped[str] = mapped_column(String)


class ServiceType(enum.Enum):
    K1 = "К1"
    K2 = "К2"
    K3 = "К3"
    other = "other"

class PublicService(Base):

    __tablename__ = "public_service"

    id: Mapped[int] = Column(Integer, primary_key=True)
    title: Mapped[str] = Column(String)
    service_type: Mapped[ServiceType] = Column(
        PgEnum(
            ServiceType,
            name="service_type",
            create_type=True
               ),
        nullable=False
    )


class AuthorType(enum.Enum):
    collaborator = "соавтор"
    author = "автор"


class Publication(Base):

    __tablename__ = "publication"

    id: Mapped[int] = Column(Integer, primary_key=True)
    citations: Mapped[str] = Column(String)
    title: Mapped[str] = Column(String)
    public_service_id = Column(Integer, ForeignKey("public_service.id"))
    public_service: Mapped[str] = Column(String)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.now)
    authors: Mapped[str] = Column(String)
    publication_year: Mapped[str] = Column(String)
    author_type: Mapped[AuthorType] = Column(
        PgEnum(
            AuthorType,
            name="author_type",
            create_type=False
        ),
        nullable=False
    )
    users: Mapped[List["User"]] = relationship(secondary="user_publication", back_populates="publications")

    def __repr__(self):
        return f"Publication(id={self.id})"


class UserPublication(Base):
    __tablename__ = "user_publication"

    id: Mapped[int] = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user_mirea.id"))
    publication_id = Column(Integer, ForeignKey("publication.id"))
