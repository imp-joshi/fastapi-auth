from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import security
from app.api import deps
from app.db import crud
from app.schemas import token as token_schema, user as user_schema

router = APIRouter()

@router.post("/register", response_model=user_schema.UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user: user_schema.UserCreate, db: Session = Depends(deps.get_db)):
    """
    Register a new user with a default role.
    """
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@router.post("/token", response_model=token_schema.Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(deps.get_db)
):
    """
    Authenticate a user and return an access token.
    """
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}