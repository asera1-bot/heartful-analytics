from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.core.db import get_db
from app.auth import authenticate_user, create_access_token
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db),
):
    ok = authenticate_uesr(form.username, form.password)
    if not ok:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_access_token(sub=form.username)
    return{"access_token": token, "token_type": "bearer"}
