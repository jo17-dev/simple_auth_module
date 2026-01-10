from fastapi import APIRouter, Response, Depends, HTTPException
from app.interface.view_models.token import TokenDatas, TokenView, TokenCreated
from app.interface.view_models.user import UserLogin
from app.data.database import get_db
from app.services.auth_service import log_in, refresh_token, validate_token
from sqlalchemy.orm import Session
router = APIRouter()

# take email & password to provide a refresh && access token
@router.post("/login")
def login(user_login_datas: UserLogin, db: Session = Depends(get_db) ):
    try:
        return log_in(user_login_datas, db)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(500, f"something unexpected happened.. please contact the admins :: {e} ")

# takes a refresh token and provide a new duo token
@router.post("/refresh")
def refresh(token: TokenView, db: Session = Depends(get_db))-> TokenCreated:
    try:
        created_token = refresh_token(token, db)
        return created_token
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(500, "something unexpected happened.. please contact the admins")

# takes a token, decrypt and send it back
@router.post("/validate")
def validate(token: TokenView, db: Session = Depends(get_db))-> TokenDatas :
    try:
        validated_datas = validate_token(token, db)
        return validated_datas
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(500, "something unexpected happened.. please contact the admins")