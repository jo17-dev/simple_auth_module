from pydantic import BaseModel, Field
from typing import List
from enum import Enum
from app.interface.view_models.token import TokenCreated

class RoleEnum(str, Enum):
    admin = "admin"
    client = "client"
    employee = "employee" 


class UserBase(BaseModel):
    email: str  = Field(..., json_schema_extra={"example": "email@example.com"})
    roles: List[RoleEnum] = Field(..., json_schema_extra={"example": ["employee", "admin"]})


class UserCreation(UserBase):
    password: str = Field(..., json_schema_extra="ReaaaalPass23word!")


class UserLogin(BaseModel):
    email: str  = Field(..., json_schema_extra={"example": "email@example.com"})
    password: str = Field(..., json_schema_extra={"example": "ReaaaalPass23word!"})

class UserIdentifier(BaseModel):
    id: int

class UserInfo(UserBase):
    id: int


class UserCreated(UserBase, TokenCreated):
    email: str
    roles: List[RoleEnum]

class UserUpdate(BaseModel):
    password: str | None = None
    email: str | None = None