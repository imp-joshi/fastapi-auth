from sqlalchemy.orm import Session
import os
import sys

# Add the project root to the Python path to allow importing 'app'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.base import SessionLocal
from app.db import models
from app.security import get_password_hash

# --- CONFIGURATION ---
# It's better to get these from environment variables for production
SUPERUSER_USERNAME = os.getenv("SUPERUSER_USERNAME", "superadmin")
SUPERUSER_PASSWORD = os.getenv("SUPERUSER_PASSWORD", "SuperSecretPassword123!")

ROLES_TO_CREATE = [
    "admin-Super User",
    "Admin-Department wise",
    "User- Developer Search",
    "User- User Search",
]

def initial_setup(db: Session):
    print("--- Starting Initial Setup ---")

    # 1. Create all necessary roles
    for role_name in ROLES_TO_CREATE:
        role = db.query(models.Role).filter(models.Role.name == role_name).first()
        if not role:
            print(f"Creating role: {role_name}")
            db_role = models.Role(name=role_name)
            db.add(db_role)
        else:
            print(f"Role '{role_name}' already exists.")
    db.commit()

    # 2. Create the first Super User
    superuser = db.query(models.User).filter(models.User.username == SUPERUSER_USERNAME).first()
    if not superuser:
        print(f"Creating Super User: {SUPERUSER_USERNAME}")
        hashed_password = get_password_hash(SUPERUSER_PASSWORD)
        
        superuser_role = db.query(models.Role).filter(models.Role.name == "admin-Super User").one()
        
        db_user = models.User(
            username=SUPERUSER_USERNAME,
            hashed_password=hashed_password,
            is_active=True,
        )
        db_user.roles.append(superuser_role)
        db.add(db_user)
        db.commit()
        print("Super User created successfully.")
    else:
        print(f"Super User '{SUPERUSER_USERNAME}' already exists.")
    
    print("--- Initial Setup Finished ---")

if __name__ == "__main__":
    print("Running bootstrap script...")
    db = SessionLocal()
    try:
        initial_setup(db)
    finally:
        db.close()