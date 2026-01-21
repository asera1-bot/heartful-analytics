from sqlalchemy import select, func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from datetime import timezone

from app import models
from app.schemas.harvest import HarvestCreate, HarvestUpdate

def _month_from_measured_at(dt) -> str:
    #dtはtimezone付きの想定(Pydanticがdatetimeにしてくれる)
    #JSTで運用するならdt.astimezone(ZoneInfo("Azia/Tokyo"))にしてから月を切る
    return dt.strftime("%Y-%m")

def create(db: Session, data: HarvestCreate):
    payload = data.model_dump()

    if payload.get("month") is None:
        payload["month"] = data.measured_at.strftime("%Y-%m")

    obj = models.Harvest(**payload)
    db.add(obj)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="harvest already exists for company, crop, measured_at and measure_no",
        )
    db.refresh(obj)
    return obj

    # psycopgの本体例外がe.origに入る
    if isinstance(e.orig, UniqueViolation):
        raise HTTPException(status_code=409, detail="harvest already exists (unique constraint)")
    if isinstance(e.orig, NotNullViolation):
        raise HTTPException(status_code=400, detail="required field is missing (NOT NULL violation)")

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=str(e.orig))
    db.refresh(obj)
    return obj


def get(db: Session, harvest_id: int):
    return db.get(models.Harvest, harvest_id)


def list(db: Session, limit: int, offset: int):
    return db.query(models.Harvest).offset(offset).limit(limit).all()


def update(db: Session, obj, data: HarvestUpdate):
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


def delete(db: Session, obj):
    db.delete(obj)
    db.commit()
