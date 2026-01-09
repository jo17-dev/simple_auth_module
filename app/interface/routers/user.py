from fastapi import APIRouter, Depends, HTTPException
from app.interface.view_models.user import UserCreation, UserInfo, UserCreated
from app.services.users_service import add_user
from app.data.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

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
def get_user(user: UserCreation)->UserInfo:
    pass

# update a user
@router.put("/")
def update_user(user: UserCreation):
    pass

# delete a user
@router.delete("/")
def delete_user(user: UserCreation):
    pass