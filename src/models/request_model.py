from core.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, DateTime, String
from datetime import datetime


class RequestModel(Base):
    __tablename__ = 'request'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    request_id: Mapped[str] = mapped_column(String)
    total_cities: Mapped[int] = mapped_column(Integer)
    processed_city: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)




