from core.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, DateTime, JSON, String
from datetime import datetime


class City(Base):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    request_id: Mapped[str] = mapped_column(String, nullable=True)
    time: Mapped[datetime] = mapped_column(DateTime)
    information: Mapped[JSON] = mapped_column(JSON)



