from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Harvest(Base):
    __tablename__ = "harvest"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    month: Mapped[str] = mapped_column(String(7), index=True)  # YYYY-MM

    company: Mapped[str] = mapped_column(String(100), index=True)
    crop: Mapped[str] = mapped_column(String(100), index=True)
    amount_kg: Mapped[float] = mapped_column(Float)
