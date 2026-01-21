from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

MONTH_PATTERN = r"^\d{4}-\d{2}$"


class HarvestBase(BaseModel):
    month: Optional[str] = Field(default=None, pattern=MONTH_PATTERN)
    company: str
    crop: str
    amount_kg: float
    measured_at: datetime
    measure_no: Optional[int] = Field(default=None, ge=1)

class HarvestCreate(HarvestBase):
    pass

class HarvestUpdate(BaseModel):
    month: Optional[str] = Field(default=None, pattern=MONTH_PATTERN)
    company: Optional[str] = None
    crop: Optional[str] = None
    amount_kg: Optional[float] = None
    measured_at: Optional[datetime] = None
    measure_no: Optional[int] = Field(default=None, ge=1)

class HarvestOut(HarvestBase):
    id: int
    model_config = {"from_attributes": True}
