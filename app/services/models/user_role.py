from sqlalchemy import Column, ForeignKey, Table, Integer
from sqlalchemy.orm import declarative_base
from app.data.database import Base

# Table d'association pour la relation many-to-many
user_role = Table(
    'user_role',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    extend_existing=True
)