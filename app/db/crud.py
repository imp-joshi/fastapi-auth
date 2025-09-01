from sqlalchemy.orm import Session

from app import security
from app.db import models
from app.schemas import user as user_schema

def get_user_by_username(db: Session, username: str):
    """Retrieve a user from the database by their username."""
    return db.query(models.User).filter(models.User.username == username).first()

def get_role_by_name(db: Session, role_name: str):
    """Retrieve a role from the database by its name."""
    return db.query(models.Role).filter(models.Role.name == role_name).first()

def create_user(db: Session, user: user_schema.UserCreate, role_name: str = "User- User Search"):
    """Create a new user and assign them a default role."""
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    
    # Find the role in the DB. If it doesn't exist, this function won't create it.
    # The bootstrap script will be responsible for creating roles.
    role = get_role_by_name(db, role_name)
    if role:
        db_user.roles.append(role)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user