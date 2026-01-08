from pydantic import BaseModel, Field, List
from typing import List
from enum import Enum

class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"
    manager = "manager"


class UserCreation(BaseModel):
    email: str  = Field(..., example="email@example.com")
    password: str = Field(..., example="ReaaaalPassword!")
    role: str = Field("user",example="Client")


class UserIdentifier(BaseModel):
    id: int

class UserInfo(BaseModel):
    id: int
    email: str  = Field(..., example="email@example.com")
    roles: List[RoleEnum] = Field(..., example=["user", "admin"])
