from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db import models
from app.db.base import SessionLocal
from app.db.crud import get_user_by_username
from app.schemas import token as token_schema

# This points to the URL that clients will use to get a token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency to get the current user from a JWT token
def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db)
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = token_schema.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = get_user_by_username(db, username=token_data.username)
    if user is None or not user.is_active:
        raise credentials_exception
    return user

# Dependency factory to require a specific role
def require_role(required_role: str):
    """
    Returns a dependency that checks if the current user has the required role.
    This is the core of the authorization system.
    """
    def _require_role(current_user: Annotated[models.User, Depends(get_current_user)]):
        user_roles = {role.name for role in current_user.roles}
        if required_role not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User does not have the required role: {required_role}",
            )
        return current_user

    return _require_role