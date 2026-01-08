from sqlalchemy.orm import Session
from app.services.exceptions.user_exception import UserException
from app.services.model import User

class UserRepo:
    def add(self, user: User, db: Session)->User:
        try:
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except Exception as e:
            raise UserException(f"UserException :: ${e} ", "The user was not added in the db, sorry")

    def update(self):
        pass

    def delete(self, user_id: int, db: Session):
        try:
            db.query(User).filter(User.id == user_id).delete()
            db.commit()
        except Exception as e:
            raise UserException(f"UserException :: ${e} ", "Ther user was not delete due to error in our db")

    def get_by_id(self, user_id: int, db: Session)->(User | None):
        try:
            user = db.query(User).filter(User.id == user_id).first()
            return user
        except Exception as e:
            raise UserException(f"UserException :: ${e} ", "Ther user was not delete due to error in our db")

    def get_by_email(self, email: str, db: Session):
        try:
            user = db.query(User).filter(User.email == email).first()
            return user
        except Exception as e:
            raise UserException(f"UserException :: ${e} ", "Something bad happened in our db")