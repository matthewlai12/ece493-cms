from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class ReviewInvitation(Base):
    __tablename__ = "reviewinvitation"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    submission_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    referee_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    paper_title: Mapped[str] = mapped_column(String(255), nullable=False)
    paper_abstract: Mapped[str] = mapped_column(Text, nullable=False, default="")
    sent_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    responded_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
