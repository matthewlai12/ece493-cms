from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class ConfirmationTicket(Base):
    __tablename__ = "confirmationticket"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
