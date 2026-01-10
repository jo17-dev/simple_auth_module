from pydantic import BaseModel, Field
from typing import List
from enum import Enum
from app.interface.view_models.token import TokenCreated

class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"
    manager = "manager"


class UserBase(BaseModel):
    email: str  = Field(..., json_schema_extra="email@example.com")
    roles: List[RoleEnum] = Field(..., json_schema_extra=["user", "admin"])


class UserCreation(UserBase):
    password: str = Field(..., json_schema_extra="ReaaaalPass23word!")


class UserIdentifier(BaseModel):
    id: int

class UserInfo(UserBase):
    id: int


class UserCreated(UserBase, TokenCreated):
    email: str
    roles: List[RoleEnum]
