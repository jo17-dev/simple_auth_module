import pytest
from fastapi import HTTPException
from datetime import datetime, timedelta
import jwt
import uuid
from app.config.env import settings

from app.services.token_service import (
    create_token,
    decrypt_token,
    create_refresh_and_access_tokens,
    issue_token
)
from app.interface.view_models.token import TokenView, TokenDatas, TokenCreated


# --- Tests create_token ---
def test_create_token_success(token_datas):
    data = {"sub": str(token_datas.uid), "typ": token_datas.typ, "role": token_datas.role}
    token = create_token(data)
    assert isinstance(token, str)
    decoded = jwt.decode(token, settings.SECRET_KEY , algorithms=[settings.ALGORITHM])
    assert decoded["sub"] == str(token_datas.uid)
    assert decoded["typ"] == token_datas.typ


def test_create_token_raises(monkeypatch):
    # Forcer jwt.encode à lever une exception
    def fake_encode(*args, **kwargs):
        raise Exception("JWT error")
    monkeypatch.setattr("jwt.encode", fake_encode)

    with pytest.raises(Exception):
        create_token({"sub": "1"})


# --- Tests create_refresh_and_access_tokens ---
def test_create_refresh_and_access_tokens_returns_tokens(monkeypatch):
    fixed_uuid = "123e4567-e89b-12d3-a456-426614174000"
    monkeypatch.setattr("uuid.uuid4", lambda: uuid.UUID(fixed_uuid))
    
    tokens: TokenCreated = create_refresh_and_access_tokens(user_id=1, user_role="admin")
    assert isinstance(tokens.access_token, str)
    assert isinstance(tokens.refresh_token, str)

    decoded_access = jwt.decode(tokens.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    decoded_refresh = jwt.decode(tokens.refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    assert decoded_access["sub"] == "1"
    assert decoded_access["role"] == "admin"
    assert decoded_access["typ"] == "bearer"

    assert decoded_refresh["sub"] == "1"
    assert decoded_refresh["typ"] == "refresh"
    assert decoded_refresh["id_token"] 


# --- Tests decrypt_token ---
def test_decrypt_token_bearer_success(token_datas):
    # Créer un token valide
    token_str = create_token({
        "sub": str(token_datas.uid),
        "role": token_datas.role,
        "typ": "bearer",
        "exp": token_datas.exp
    })
    token_view = TokenView(token=token_str)
    result = decrypt_token(token_view)
    assert isinstance(result, TokenDatas)
    assert result.uid == token_datas.uid
    assert result.role == token_datas.role
    assert result.typ == token_datas.typ


def test_decrypt_token_refresh_success(refresh_token_datas):
    token_str = create_token({
        "sub": str(refresh_token_datas.uid),
        "typ": "refresh",
        "id_token": refresh_token_datas.id_token,
        "exp": refresh_token_datas.exp
    })
    token_view = TokenView(token=token_str)
    result = decrypt_token(token_view)
    assert isinstance(result, TokenDatas)
    assert result.id_token == refresh_token_datas.id_token
    assert result.typ == "refresh"


def test_decrypt_token_invalid_type_raises():
    # token qui viole les règles
    token_str = create_token({
        "sub": "1",
        "typ": "bearer",
        "role": None,
        "exp": int((datetime.now() + timedelta(minutes=5)).timestamp())
    })
    token_view = TokenView(token=token_str)
    with pytest.raises(HTTPException) as exc:
        decrypt_token(token_view)
    assert exc.value.status_code == 400


def test_decrypt_token_invalid_jwt_raises():
    token_view = TokenView(token="not.a.real.token")
    with pytest.raises(HTTPException) as exc:
        decrypt_token(token_view)
    assert exc.value.status_code == 401


def test_issue_token_returns_token_created():
    user_id=34
    roleString="admin|guest"
    token_created: TokenCreated = issue_token(user_id, roleString)
    assert isinstance(token_created.access_token, str)
    assert isinstance(token_created.refresh_token, str)
