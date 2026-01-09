from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
import datetime
from app.data.database import Base
from app.services.models.user_role import user_role

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    
    # Défaut MySQL pour la création et modification
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)

    roles = relationship("Role", secondary=user_role, back_populates="users")
    def __repr__(self):
        return f"<Utilisateur(id={self.id}, email={self.email}, role={self.roles}>"
