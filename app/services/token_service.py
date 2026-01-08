import jwt
from app.config.env import settings
from fastapi import HTTPException
from sqlalchemy.orm import Session
from argon2 import PasswordHasher
from datetime import datetime
from app.interface.view_models.token import TokenView, TokenDatas, TokenCreated
from datetime import timedelta
import uuid

password_hasher = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=2,
    hash_len=32,
    salt_len=16
)

# Generalate access and refresh tokens
def issue_token(user_id: int, rolesString: str)-> TokenCreated:
    return create_refresh_and_access_tokens(user_id, user_role=rolesString)

# create a token string based on datas
def create_token(data: dict):
    chaine = data.copy()
    try:
        encoded_jwt = jwt.encode(chaine, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    except Exception as e:
        print(f"errreur de generation du token {e} ")
        raise e

# decrypt token datas
def decrypt_token(token_view:TokenView)->TokenDatas:
    decoded_values = None
    try:
        decoded_values = jwt.decode(token_view.token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        response = TokenDatas(
            uid= decoded_values.get('sub'),
            typ= decoded_values.get('typ'),
            exp=decoded_values.get('exp'),
            role=decoded_values.get('role'),
            id_token=decoded_values.get('id_token')
        )
        # petites verifs
        if response.typ == 'refresh':
            if (response.id_token is None) or (response.role is not None) or (response.exp is None):
                raise ValueError("datas retreived from token doesnt look familar")
        elif response.typ == "bearer":
            if response.role is None:
                raise ValueError("datas retreived from token doesnt look familar")
        return response
    except ValueError as v:
        raise HTTPException(400, "datas retreived from token doesnt look familar")
    except Exception as e:
        raise HTTPException(401, "couldn't decrypt the token")


def create_refresh_and_access_tokens(user_id:int, user_role:str, id_refresh_token:str = str(uuid.uuid4())) -> TokenCreated :
    try:
        access_token = create_token({
            "sub": str(user_id), # PyJWT à besoin du sub en string
            "role":  user_role,
            "typ": "bearer",
            "exp": (int) ((datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp())
        })

        refresh_token = create_token({
            "sub": str(user_id), # PyJWT à besoin du sub en string
            "typ": "refresh",
            "id_token": id_refresh_token, # identifiant unique du token
            "exp": (int) ((datetime.now() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)).timestamp())
        })

        return TokenCreated(
            access_token=access_token,
            refresh_token=refresh_token
        )
    except Exception as e:
        raise HTTPException(500, "Impossible de générer de token")