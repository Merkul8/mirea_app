from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
import enum

from sqlalchemy.orm import Mapped

from database.db import Base


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


class Publication(Base):

    __tablename__ = "publication"

    id: Mapped[int] = Column(Integer, primary_key=True)
    url: Mapped[str] = Column(String)
    title: Mapped[str] = Column(String)
    public_service_id = Column(Integer, ForeignKey("public_service.id"))
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.now())

    def __repr__(self):
        return f"Publication(id={self.id})"


class AuthorType(enum.Enum):
    collaborator = "соавтор"
    author = "автор"


class UserPublication(Base):
    __tablename__ = "user_publication"

    id: Mapped[int] = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user_mirea.id"))
    publication_id = Column(Integer, ForeignKey("publication.id"))
    service_type: Mapped[str] = Column(
        PgEnum(
            AuthorType,
            name="author_type",
            create_type=False
        ),
        nullable=False
    )
