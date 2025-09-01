from pydantic import BaseModel

# --- Role Schemas ---
class RoleBase(BaseModel):
    name: str

class RoleRead(RoleBase):
    id: int

# --- User Schemas ---
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    is_active: bool
    roles: list[RoleRead] = []

    class Config:
        # This allows Pydantic to read data from ORM objects
        from_attributes = True