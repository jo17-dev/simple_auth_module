from interface.model_view.user_entity import UtilisateurCreation, ROLE, UtilisateurInfo, UtilisateurLogin
from services.model.utilisateur_model import Utilisateur
from services.model.token_model import Token
from datetime import datetime
from utils.response_template import ReponseTemplate
from fastapi import status, HTTPException
from config.env import settings
import jwt
from sqlalchemy.orm import Session
from argon2 import PasswordHasher
from services.auth_service import creer_token
from services.repositories.users import UserRepo

password_hasher = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=2,
    hash_len=32,
    salt_len=16
)


user_repo = UserRepo()


def hash_string(password: str) -> str:
    try:
        return password_hasher.hash(password)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur de chiffrement du mot de passe : {str(e)}"
        )


def verify_hashed_string(password: str, hashed: str) -> bool:
    try:
        return password_hasher.verify(hashed, password)
    except Exception as e:
        print(f"Erreur de verification de mot de passe {e} ")
        # raise HTTPException(500, "quelque chose s'est mal passé.. revenez plus tards")
        return False
    

# recrer un nouveau à partir d'un token de rafraichissement
# 1. decoder le token
# 2. verifier par son sub s'il a déjas été utilisé
# 3. si est utilié renvoyé 403 forbidden
# si elle n'es pas encore enregistrer, l'enregistrer et recréer les un nouveau duo de access & refresh token
def refresh_token(refresh_token: SimpleToken, db: Session) ->TokenView :
    try:
        decodedvalues = jwt.decode(refresh_token.token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        print(f"decoded values: {decodedvalues} ")
        expiration_timestamp = decodedvalues.get('exp')
        user_id = int(decodedvalues.get('sub'))
        
        if expiration_timestamp and datetime.fromtimestamp(expiration_timestamp) < datetime.now():
            print("Token expiré 1")
            raise HTTPException(403, "Token non valide")
        
        # utilisateur = db.query(Utilisateur).filter(Utilisateur.id == user_id).first()
        utilisateur = utilisateur_repo.recuperer_par_id(user_id, db)
        
        if not utilisateur:
            print("Token non valide")
            raise HTTPException(403, "Token non valide")
        
        if decodedvalues.get('typ') != "refresh":
            raise HTTPException(401, "Mauvais type de token. nous attendons ici un refresh token")
        else:
            # verification de la validité du token
            used_token = refresh_token_repo.recuperer_par_utilisateur_et_identifiant(int(decodedvalues.get('sub')), decodedvalues.get("id_token"), db)

            if used_token is None:
                used_refresh_token = UsedRefreshToken()
                used_refresh_token.utilisateur_id = utilisateur.id
                used_refresh_token.identifier = decodedvalues.get('id_token')
                token_view = create_refresh_and_access_tokens(utilisateur.id, utilisateur.role)

                refresh_token_repo.ajouter(used_refresh_token, db)

                return token_view
            else:
                print("Refresh token invalide. déjas utilisé")
                raise HTTPException(403, "Refresh token invalide. déjas utilisé")
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"------------////---/// execption occurred:: {e} ")
        raise HTTPException(500, "impossible de creer le token de rafraichissement")