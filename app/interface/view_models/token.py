from pydantic import BaseModel


class TokenView(BaseModel):
    token: str


class TokenDatas(BaseModel):
    uid: str
    typ: str
    exp: int
    role: str


class TokenCreated(BaseModel):
    access_token: str
    refresh_token: str