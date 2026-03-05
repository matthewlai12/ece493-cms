from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class Review(Base):
    __tablename__ = "review"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    submission_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    referee_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    comments: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="submitted")
    submitted_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
