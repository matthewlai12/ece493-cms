from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class ConferenceRegistration(Base):
    __tablename__ = "conferenceregistration"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
