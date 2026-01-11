from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models
from app.db.session import get_db
from app.schemas.env import EnvCreate, EnvOut, EnvUpdate

router = APIRouter(prefix="/env", tags=["env"])


@router.post("/", response_model=EnvOut, status_code=status.HTTP_201_CREATED)
def create_env(data: EnvCreate, db: Session = Depends(get_db)):
    obj = models.Env(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/", response_model=list[EnvOut])
def list_env(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    return db.query(models.Env).offset(offset).limit(limit).all()


@router.get("/{env_id}", response_model=EnvOut)
def get_harvest(env_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Env, env_id)
    if not obj:
        raise HTTPException(status_code=404, detail="env not found")
    return obj


@router.patch("/{env_id}", response_model=EnvOut)
def update_env(env_id: int, data: EnvUpdate, db: Session = Depends(get_db)):
    obj = db.get(models.Env, env_id)
    if not obj:
        raise HTTPException(status_code=404, detail="env not found")

    for (
        k,
        v,
    ) in data.model_dump(exclude_unset=Ture).items():
        setattr(obj, k, v)

    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{env_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_env(env_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Env, env_id)
    if not obj:
        raise HTTPException(status_code=404, detail="env not found")

    db.delete(obj)
    db.commit()
