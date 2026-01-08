from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from data.database import Base
import datetime


class UsedToken(Base):
    __tablename__ = "used_tokens"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(255))
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)
    exp_date = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User")

    def __repr__(self):
        return f"<UsedToken(id={self.id}, user_id={self.utilisateur_id} >"
