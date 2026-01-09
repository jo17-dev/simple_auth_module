from pydantic import BaseModel, Field
from typing import List
from enum import Enum
from app.interface.view_models.token import TokenCreated

class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"
    manager = "manager"


class UserBase(BaseModel):
    email: str  = Field(..., example="email@example.com")
    roles: List[RoleEnum] = Field(..., example=["user", "admin"])


class UserCreation(UserBase):
    password: str = Field(..., example="ReaaaalPass23word!")


class UserIdentifier(BaseModel):
    id: int

class UserInfo(UserBase):
    id: int


class UserCreated(UserBase, TokenCreated):
    email: str
    roles: List[RoleEnum]
