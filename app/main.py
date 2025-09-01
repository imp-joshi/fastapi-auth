from fastapi import FastAPI
from app.api.routers import auth, users
from app.db.base import Base, engine

# This line creates the database tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="fastapi-auth",
    description="A modular and configurable authentication and authorization system.",
    version="1.0.0",
)

# Include the API routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the FastAPI Auth API"}