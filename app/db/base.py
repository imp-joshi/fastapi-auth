from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# Setup the database engine. `connect_args` is for SQLite only.
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Each instance of SessionLocal will be a new database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# A base class for our models to inherit from
Base = declarative_base()