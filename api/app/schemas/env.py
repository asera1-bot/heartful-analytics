from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class EnvBase(BaseModel):
    measured_at: datetime
    temperature: Optional[float] = None
    humidity: Optional[float] = None


class EnvCreate(EnvBase):
    pass


class EnvUpdate(BaseModel):
    measured_at: Optional[datetime] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None


class EnvOut(EnvBase):
    id: int

    class Config:
        from_attributes = True
