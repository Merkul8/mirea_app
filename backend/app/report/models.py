from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime

from sqlalchemy.orm import Mapped, validates

from database.db import Base


class Report(Base):

    __tablename__ = "report"

    id: Mapped[int] = Column(Integer, primary_key=True)
    title: Mapped[str] = Column(String)
    file_path: Mapped[str] = Column(String)
    public_service_id = Column(Integer, ForeignKey("user_mirea.id"))
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.now())


    def __repr__(self):
        return f"Report(id={self.id})"