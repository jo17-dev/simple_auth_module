from fastapi import APIRouter
from app.interface.view_models.user import UserCreation, UserIdentifier, UserInfo

router = APIRouter()

# create a user a( and issue a token )
@router.post("")
def create_user(user: UserCreation )->UserInfo:
    pass

# get a user infos
@router.get("")
def get_user(user: UserCreation)->UserInfo:
    pass

# update a user
@router.put("")
def update_user(user: UserCreation):
    pass

# delete a user
@router.delete("")
def delete_user(user: UserCreation):
    pass