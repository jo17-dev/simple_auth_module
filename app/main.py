from fastapi import FastAPI, APIRouter
from data.database import get_db
from app.interface.routers.auth import router as auth_router
from app.interface.routers.user import router as user_router
from app.config.logger import logger
from app.config.env import settings

app = FastAPI(
    title="S.A.M - simple auth module", 
    description="sam is a fastapi module who manages authentification via tokens and users via thiers email, password and roles ",
    version=settings.API_VERSION
    )
app_router = APIRouter()
app_router.include_router(auth_router, prefix="/auth", tags=["Token management"])
app_router.include_router(user_router, prefix="/user", tags=["Users management"])

app.include_router(app_router)