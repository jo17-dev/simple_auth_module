from app.services.model import UsedToken
from sqlalchemy.orm import Session

class TokenRepository:
    def ajouter(self, refresh_token: UsedToken, db: Session):
        try:
            db.add(refresh_token)
            db.commit()
            db.refresh(refresh_token)
        except Exception as e:
            print("-- Erreur lie à la BD lors de l'ajout du refresh token utilsé")
            raise e
        
    def recuperer_par_utilisateur_et_identifiant(self, utilisateur_id:int, identifiant:str, db: Session):
        try:
            result = db.query(UsedToken).filter(UsedToken.identifier == identifiant).first()
            return result 
        except Exception as e:
            print("-- Erreur lie à la BD lors de la verification de refresh tokens utilisés")
            raise e