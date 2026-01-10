from app.interface.view_models.token import TokenView, TokenCreated, TokenDatas
from app.interface.view_models.user import UserLogin
from sqlalchemy.orm import Session
from app.services.repositories.users import UserRepo
from argon2 import PasswordHasher
from app.services.repositories.used_token import TokenRepository
from app.services.model import UsedToken
from fastapi import HTTPException
from app.config.env import settings
from datetime import datetime
from app.services.token_service import  create_refresh_and_access_tokens, decrypt_token

user_repo = UserRepo()
refresh_token_repo = TokenRepository()


password_hasher = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=2,
    hash_len=32,
    salt_len=16
)

def hash_string(target: str) -> str:
    try:
        return password_hasher.hash(target)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Hashstring password exception"
        )

def verify_hashed_string(target: str, hashed: str) -> bool:
    try:
        return password_hasher.verify(hashed, target)
    except Exception as e:
        print(f"Erreur de verification de mot de passe {e} ")
        raise HTTPException(500, "quelque chose s'est mal passé.. revenez plus tards")


def log_in(user_login_datas: UserLogin, db: Session)->TokenCreated:
    found_user = user_repo.get_by_email(user_login_datas.email, db)

    if found_user is None:
        raise HTTPException(400, "Try again.. ")
    
    if verify_hashed_string(user_login_datas.password, found_user.password) == False:
        raise HTTPException(400, "Try again ")
    
    roles_stringified =""

    for role_item in found_user.roles:
        roles_stringified = roles_stringified + settings.ROLE_SEPARATOR + role_item.title
    
    tokens = create_refresh_and_access_tokens(found_user.id, roles_stringified)

    return tokens

# recrer un nouveau à partir d'un token de rafraichissement
# 1. decoder le token
# 2. verifier par son sub s'il a déjas été utilisé
# 3. si est utilié renvoyé 403 forbidden
# si elle n'es pas encore enregistrer, l'enregistrer et recréer les un nouveau duo de access & refresh token
# créer les tokens
def refresh_token(refresh_token: TokenView, db: Session) ->TokenCreated :
    try:
        decoded_values = decrypt_token(refresh_token.token)
        expiration_timestamp = decoded_values.exp
        user_id = int(decoded_values.uid)

        if expiration_timestamp and datetime.fromtimestamp(expiration_timestamp) < datetime.now():
            print("Token expiré 1")
            raise HTTPException(403, "Token expired")
        
        user = user_repo.get_by_id(user_id, db)
        
        if not user:
            print("Token non valide")
            raise HTTPException(403, "Invalid token. the user does not exist anymore")
        
        if decoded_values.typ != "refresh":
            raise HTTPException(401, "Bad token type. you need to provide a refresh token here")
        else:
            # verification de la validité du token
            used_token = refresh_token_repo.recuperer_par_utilisateur_et_identifiant(user_id, decoded_values.id_token , db)

            if used_token is None:
                used_refresh_token = UsedToken()
                used_refresh_token.user_id = user.id
                used_refresh_token.identifier = decoded_values.id_token
                token_view = create_refresh_and_access_tokens(user.id , settings.ROLE_SEPARATOR.join(user.roles))

                refresh_token_repo.ajouter(used_refresh_token, db)

                return token_view
            else:
                print("Refresh token invalide. déjas utilisé")
                raise HTTPException(403, "Refresh token invalide. déjas utilisé")
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(500, f"impossible de creer le token de rafraichissement:: {e} ")


def validate_token(token_view: TokenView, db: Session)->TokenDatas:
    decoded_values = decrypt_token(token_view.token)
    expiration_timestamp = decoded_values.exp
    user_id = int(decoded_values.uid)

    if expiration_timestamp and datetime.fromtimestamp(expiration_timestamp) < datetime.now():
        print("Token expiré 1")
        raise HTTPException(400, "Token expired")
    
    user = user_repo.get_by_id(user_id, db)
    
    if not user:
        print("Token non valide")
        raise HTTPException(400, "Invalid token. the user does not exist anymore")
    return decoded_values