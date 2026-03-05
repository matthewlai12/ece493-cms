from datetime import datetime

from sqlalchemy import DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class RegistrationPrice(Base):
    __tablename__ = "registrationprice"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    active_from: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    active_to: Mapped[datetime] = mapped_column(DateTime, nullable=False)
