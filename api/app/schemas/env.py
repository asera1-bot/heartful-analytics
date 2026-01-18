from typing import Optional

from pydantic import BaseModel


class EnvBase(BaseModel):
    month: str
    temperature: float
    humidity: float
    medium: str
    water_content: float
    illuminance: float


class EnvCreate(EnvBase):
    pass


class EnvUpdate(BaseModel):
    month: Optional[str] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    medium: Optional[str] = None
    water_content: Optional[float] = None
    illuminance: Optional[float] = None


class EnvOut(EnvBase):
    id: int

    class Config:
        from_attributes = True
