from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app import models
from app.schemas.harvest import HarvestCreate, HarvestUpdate


def create(db: Session, data: HarvestCreate):
    obj = models.Harvest(**data.model_dump())
    db.add(obj)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="harvest already exists for this month and company and crop",
        )
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
