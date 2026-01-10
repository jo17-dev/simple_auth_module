from fastapi import APIRouter, Depends, HTTPException
from app.interface.view_models.user import UserCreation, UserInfo, UserCreated
from app.interface.view_models.token import TokenView
from app.services.users_service import add_user, get_user_infos, delete
from app.data.database import get_db
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
security = HTTPBearer()

# create a user a( and issue a token )
@router.post("/")
def create_user(user: UserCreation, db: Session = Depends(get_db))->UserCreated:
    try:
        new_user_infos = add_user(user, db)
        return new_user_infos
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(500, e)

# get a user infos
@router.get("/")
def get_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db))->UserInfo:
    try:
        token_view = TokenView(token=credentials.credentials)
        retreived_user_infos = get_user_infos(token_view, db)
        return retreived_user_infos
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(500, e)

# update a user
@router.put("/")
def update_user(user: UserCreation):
    pass

# delete a user
@router.delete("/")
def delete_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    try:
        token_view = TokenView(token=credentials.credentials)
        retreived_user_infos = delete(token_view, db)
        return retreived_user_infos
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(500, e)
