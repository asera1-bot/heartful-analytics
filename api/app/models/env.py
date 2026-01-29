from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Env(Base):
    __tablename__ = "env"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    month: Mapped[str] = mapped_column(String(7), index=True)  # YYYY-MM

    temperature: Mapped[float] = mapped_column(Float)
    humidity: Mapped[float] = mapped_column(Float)
    medium: Mapped[str] = mapped_column(String(50))
    water_content: Mapped[float] = mapped_column(Float)
    illuminance: Mapped[float] = mapped_column(Float)
