from app.services.model import UsedToken
from sqlalchemy.orm import Session
from app.services.exceptions.token_exception import TokenException
import uuid

class TokenRepository:
    def ajouter(self, refresh_token: UsedToken, db: Session):
        refresh_token.identifier = self.__generate_guuid()
        try:
            db.add(refresh_token)
            db.commit()
            db.refresh(refresh_token)
        except Exception as e:
            raise TokenException(f"TokenException :: ${e} ", "The the token  was not added in the db, sorry")
        
    def recuperer_par_utilisateur_et_identifiant(self, user_id:int, identifiant:str, db: Session):
        try:
            result = db.query(UsedToken).filter(UsedToken.identifier == identifiant and UsedToken.user_id == user_id).first()
            return result 
        except Exception as e:
            raise TokenException(f"TokenException :: ${e} ", "The the token  was not added in the db, sorry")
        
    def __generate_guuid(self):
        return str(uuid.uuid4())