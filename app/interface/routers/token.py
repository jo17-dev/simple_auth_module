from fastapi import APIRouter, Response, Depends
from app.interface.view_models.user import UserCreation
from app.interface.view_models.token import TokenDatas, TokenView, TokenCreated

router = APIRouter()

# issue token
@router.post("/issue")
def isssue_token(tokenDatas: TokenDatas )-> TokenCreated:
    pass

# auth users
@router.post("/validate")
def validate_token(token: TokenView)-> TokenDatas :
    pass

# refresh token 
@router.post("/refresh")
def refresh_token(token: TokenDatas)-> TokenCreated:
    pass