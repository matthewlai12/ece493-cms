from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class Payment(Base):
    __tablename__ = "payment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
