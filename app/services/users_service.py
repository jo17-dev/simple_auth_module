from fastapi import HTTPException
from app.config.env import settings
from sqlalchemy.orm import Session
from app.services.repositories.users import UserRepo
from app.services.repositories.roles import RoleRepo
from app.interface.view_models.token import TokenView
from app.interface.view_models.user import UserCreation, UserCreated, UserInfo, UserUpdate
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
    email_valid = is_a_valid_email(user_to_add.email)
    password_valid = is_a_valid_password(user_to_add.password)
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
    
    tokens = create_refresh_and_access_tokens(added_user.id, [ item.title.lower() for item in added_user.roles])

    result = UserCreated(email=user_to_add.email , roles=user_to_add.roles, access_token=tokens.access_token, refresh_token=tokens.refresh_token)

    return result

def get_user_infos(token_view: TokenView, db: Session)->UserInfo:
    try:
        user = validate_token_and_get_related_user(token_view, db)
        if not user:
            raise HTTPException(404, "The user was not found.")
        result = UserInfo(email = user.email, roles=[ item.title.lower() for item in user.roles], id=user.id)
        return result
    except HTTPException as he:
        raise he
    except UserException as ue:
        raise HTTPException(500, ue.user_description)

def delete(token_view: TokenView, db: Session)->bool:
    decoded_values = decrypt_token(token_view)
    expiration_timestamp = decoded_values.exp
    user_id = int(decoded_values.uid)

    if expiration_timestamp and datetime.fromtimestamp(expiration_timestamp) < datetime.now():
        raise HTTPException(401, "Token expired")
    
    try:        
        user = user_repo.get_by_id(user_id, db)    
        if not user:
            raise HTTPException(404, "The user was not found.")
        else:
            user_repo.delete(user_id, db)
    except UserException as ue:
        raise HTTPException(500, ue.user_description)
    return True


def update(token_view: TokenView, user_update_datas: UserUpdate ,db: Session):
    user = validate_token_and_get_related_user(token_view, db)
    if user is None:
        raise HTTPException(404, "The corresponding user does not exists anymore")
    
    if user_update_datas.password is not None:
        if  not is_a_valid_password(user_update_datas.password):
            raise HTTPException(400, "Password valid is not valid. it should have lowercase, uppercase, number, special characters and at least 6 of length ")
        user.password = hash_string(user_update_datas.password)
    if user_update_datas.email is not None:
        if not is_a_valid_email(user_update_datas.email):
            raise HTTPException(400, "This email is not valid")
        if user_repo.get_by_email(user_update_datas.email, db) is not None:
            raise HTTPException(400, "You can't use this email. please double check it")
        user.email = user_update_datas.email

        user_repo.update(user, db)
        
    if (user_update_datas.email is None) and (user_update_datas.password is None):
        raise HTTPException(400, "Nothing was updated since you didn't specified anything")
        

def validate_token_and_get_related_user(token_view: TokenView, db: Session)->User:
    decoded_values = decrypt_token(token_view)
    expiration_timestamp = decoded_values.exp
    user_id = int(decoded_values.uid)

    if expiration_timestamp and datetime.fromtimestamp(expiration_timestamp) < datetime.now():
        raise HTTPException(401, "Token expired")
    user = user_repo.get_by_id(user_id, db)
    return user

# checks if a string is actually a valid email
def is_a_valid_email(target:str):
    return  (re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", target) is not None)


# checks if a string is actually a valid password
def is_a_valid_password(target:str):
    return (re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$', target) is not None)