from sqlalchemy.orm import Session
from app.services.exceptions.role_exception import RoleException
from app.services.model import Role


class RoleRepo:
    def add(self, role: Role, db: Session)->Role:
        role.title = role.title.upper()
        db.add(role)
        try:
            db.commit()
            db.refresh(role)
            return role
        except Exception as e:
            raise RoleException(f"UserException :: ${e} ", "The user was not added in the db, sorry")
    
    def get_by_name(self, name: str, db: Session)->(Role | None):
        try:
            role = db.query(Role).filter(Role.title == name.upper()).first()
            return role
        except Exception as e:
            raise RoleException(f"UserException :: ${e} ", "Ther user was not delete due to error in our db")