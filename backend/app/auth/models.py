from typing import List

from sqlalchemy import Column, Integer, ForeignKey, String, Boolean

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
    # academic_degree = Column(PgEnum(AcademicDegree, name="academic_degree", create_type=False), nullable=False)
    # scientific_field = Column(PgEnum(ScientificField, name="scientific_field", create_type=False), nullable=False)
    password: Mapped[str] = Column(String)
    departament_id = Column(Integer, ForeignKey("departament.id"))
    is_active_email: Mapped[bool] = Column(Boolean, default=False)
    is_active: Mapped[bool] = Column(Boolean, default=False)
    is_superuser: Mapped[bool] = Column(Boolean, default=False)

    roles: Mapped[List["Role"]] = relationship(secondary="user_role", back_populates="users")

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

