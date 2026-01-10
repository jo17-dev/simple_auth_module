from datetime import datetime
from fastapi import status, HTTPException
from app.config.env import settings
from sqlalchemy.orm import Session
from argon2 import PasswordHasher
from app.services.repositories.users import UserRepo
from app.services.repositories.roles import RoleRepo
from app.services.repositories.used_token import TokenRepository
from app.services.model import UsedToken
from app.interface.view_models.token import TokenView, TokenCreated
from app.interface.view_models.user import UserCreation, UserCreated
from app.services.model import User
from app.services.token_service import  create_refresh_and_access_tokens, decrypt_token
from app.services.exceptions.user_exception import UserException
import re

password_hasher = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=2,
    hash_len=32,
    salt_len=16
)


user_repo = UserRepo()
role_repo = RoleRepo()
refresh_token_repo = TokenRepository()

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
    

# add a user
# 1. verifier la consistence du mot de passe & l'email
# 2. verifier l'existence de l'email dans la bd
# 3. verifer l'existence des roles dans la db & les recupérerà
# 4. ajout de l'utilisateur
def add_user(user_to_add: UserCreation, db_session: Session )-> UserCreated:
    email_valid = (re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", user_to_add.email) is not None)
    password_valid = (re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$', user_to_add.password) is not None)

    if email_valid is False and password_valid is False:
        raise HTTPException(400, "Password and email are not valid")
    elif email_valid is False:
        raise HTTPException(400, "Email is not valid")
    elif password_valid is False:
        raise HTTPException(400, "Password valid is not valid. it should have lowercase, uppercase, number, special characters and at least 6 of length ")

    try:
        if user_repo.get_by_email(user_to_add.email, db_session) is not None:
            raise HTTPException(400, "A user with this email already exists here, sorry")
    except UserException as e:
        raise HTTPException(500, e.user_description)

    roles = []
    for item in user_to_add.roles:
        current_role = role_repo.get_by_name(item, db=db_session)
        if current_role is None:
            raise HTTPException(400, f"the role +{item}+ does not exists")
        else:
            roles.append(current_role)

    prepared_user = User()
    prepared_user.email = user_to_add.email
    prepared_user.password = hash_string(user_to_add.password)
    prepared_user.roles = roles

    added_user = None
    try:
        added_user = user_repo.add(prepared_user, db_session)
    except UserException as e:
        raise HTTPException(500, e.user_description)
    
    tokens = create_refresh_and_access_tokens(added_user.id, settings.ROLE_SEPARATOR.join(user_to_add.roles))

    result = UserCreated(email=user_to_add.email , roles=user_to_add.roles, access_token=tokens.access_token, refresh_token=tokens.refresh_token)

    return result