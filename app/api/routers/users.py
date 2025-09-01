from fastapi import APIRouter, Depends
from app.api import deps
from app.db import models
from app.schemas import user as user_schema

router = APIRouter()

@router.get("/me", response_model=user_schema.UserRead)
def read_current_user(
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Fetch the profile of the currently logged-in user.
    """
    return current_user

@router.get("/admin/dashboard", dependencies=[Depends(deps.require_role("admin-Super User"))])
def read_admin_dashboard(
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    An example endpoint protected by the 'admin-Super User' role.
    """
    return {"message": f"Welcome Admin {current_user.username}! This is your secret dashboard."}