from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

UserRole = Table(
    "user_role",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
)