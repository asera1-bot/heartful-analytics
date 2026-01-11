from typing import Optional

from pydantic import BaseModel, Field

MONTH_PATTERN = r"^\d{4}-\d{2}$"


class HarvestBase(BaseModel):
    month: str = Field(pattern=MONTH_PATTERN)
    company: str
    crop: str
    amount_kg: float


class HarvestCreate(HarvestBase):
    month: str
    company: str
    crop: str
    amount_kg: float


class HarvestUpdate(BaseModel):
    month: Optional[str] = Field(default=None, pattern=MONTH_PATTERN)
    company: Optional[str] = None
    crop: Optional[str] = None
    amount_kg: Optional[float] = None


class HarvestOut(HarvestBase):
    id: int

    model_config = {"from_attributes": True}
