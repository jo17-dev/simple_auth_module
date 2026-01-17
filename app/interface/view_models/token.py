from pydantic import BaseModel


class TokenView(BaseModel):
    token: str


class TokenDatas(BaseModel):
    uid: str = None
    typ: str = None
    exp: int | None = None
    role: list | None = None
    id_token: str | None = None


class TokenCreated(BaseModel):
    access_token: str
    refresh_token: str