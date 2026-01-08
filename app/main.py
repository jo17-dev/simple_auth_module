from fastapi import FastAPI, APIRouter
from data.database import get_db

app = FastAPI()

router = APIRouter(prefix="/token")
@router.get("")
def getToken():
    pass

get_db()

app.include_router(router)