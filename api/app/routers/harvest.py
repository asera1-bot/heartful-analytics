from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.harvest import Harvest
from app.schemas.harvest import HarvestCreate, HarvestOut, HarvestUpdate

router = APIRouter(prefix="/harvest", tags=["harvest"])


@router.get("/", response_model=dict)
def list_harvest(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    total = db.execute(select(func.count()).select_from(Harvest)).scalar_one()
    items = (
        db.execute(select(Harvest).order_by(Harvest.id).limit(limit).offset(offset)).scalars().all()
    )

    items_out = [HarvestOut.model_validate(x) for x in items]

    return {"total": total, "limit": limit, "offset": offset, "items": items_out}


@router.get("/{harvest_id}", response_model=HarvestOut)
def get_harvest(harvest_id: int, db: Session = Depends(get_db)):
    obj = db.get(Harvest, harvest_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Harvest not found")
    return obj


@router.post("/", response_model=HarvestOut, status_code=201)
def create_harvest(
    data: HarvestCreate,
    db: Session = Depends(get_db),
):
    obj = Harvest(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.patch("/{harvest_id}", response_model=HarvestOut)
def update_harvest(
    harvest_id: int,
    data: HarvestUpdate,
    db: Session = Depends(get_db),
):
    obj = db.get(Harvest, harvest_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Harvest not found")

    payload = data.model_dump(exclude_unset=True)
    for k, v in payload.items():
        setattr(obj, k, v)

    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{harvest_id}", status_code=204)
def delete_harvest(
    harvest_id: int,
    db: Session = Depends(get_db),
):
    obj = db.get(Harvest, harvest_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Harvest not found")

    db.delete(obj)
    db.commit()
    return Response(status_code=204)
