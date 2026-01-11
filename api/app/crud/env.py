from sqlalchemy.orm import Session

from app import models
from app.schemas.env import EnvCreate, EnvUpdate


def create(db: Session, data: EnvCreate):
    obj: models.Env(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get(db: Session, env_id: int):
    return db.get(models.Env, env_id)


def list(db: Session, limit: int, offset: int):
    return db.query(models.Env).offset(offset).limit(limit).all()


def update(db: Session, obj, data: EnvUpdate):
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


def delete(db: Session, obj):
    db.delete(obj)
    db.commit()
