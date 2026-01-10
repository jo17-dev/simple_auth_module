from fastapi import HTTPException
from app.config.env import settings
from sqlalchemy.orm import Session
from app.services.repositories.users import UserRepo
from app.services.repositories.roles import RoleRepo
from app.interface.view_models.token import TokenView
from app.interface.view_models.user import UserCreation, UserCreated, UserInfo
from app.services.model import User
from app.services.token_service import  create_refresh_and_access_tokens, decrypt_token
from app.services.exceptions.user_exception import UserException
from app.services.auth_service import hash_string
from datetime import datetime
import re


user_repo = UserRepo()
role_repo = RoleRepo()

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

def get_user_infos(token_view: TokenView, db: Session)->UserInfo:
    decoded_values = decrypt_token(token_view)
    expiration_timestamp = decoded_values.exp
    user_id = int(decoded_values.uid)

    if expiration_timestamp and datetime.fromtimestamp(expiration_timestamp) < datetime.now():
        raise HTTPException(401, "Token expired")
    
    user = user_repo.get_by_id(user_id, db)
    
    if not user:
        raise HTTPException(404, "The user was not found.")
    
    result = UserInfo(email = user.email, roles=[ item.title.lower() for item in user.roles], id=user_id)
    return result