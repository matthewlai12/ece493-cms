from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class Decision(Base):
    __tablename__ = "decision"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    submission_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    outcome: Mapped[str] = mapped_column(String(20), nullable=False)
    decided_by: Mapped[str] = mapped_column(String(255), nullable=False)
    decided_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    notes: Mapped[str] = mapped_column(Text, nullable=False, default="")
