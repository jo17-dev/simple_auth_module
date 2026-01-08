from sqlalchemy import Column, Integer, String, DateTime
import datetime
from app.data.database import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    
    # Défaut MySQL pour la création et modification
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)

    def __repr__(self):
        return f"<Utilisateur(id={self.id}, email={self.email}, role={self.role})>"
