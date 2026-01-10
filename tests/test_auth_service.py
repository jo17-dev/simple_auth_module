import pytest
from fastapi import HTTPException
from app.services.model import User
from app.services.model import UsedToken
from app.services.repositories.users import UserRepo
from datetime import datetime, timedelta

from app.services.auth_service import  refresh_token, validate_token


def test_refresh_token_expired(monkeypatch, db_session, token_view, refresh_token_datas):
    refresh_token_datas.exp = int(
        (datetime.now() - timedelta(minutes=1)).timestamp()
    )

    def mock_decrypt_token(token_view):
        return refresh_token_datas

    monkeypatch.setattr(
        "app.services.auth_service.decrypt_token",
        mock_decrypt_token
    )

    with pytest.raises(HTTPException) as exc:
        refresh_token(token_view, db_session)

    assert exc.value.status_code == 403

def test_refresh_token_non_existentt_user(monkeypatch, db_session, token_view, refresh_token_datas):
    def mock_get_user_by_id(self, user_id, db_session):
        return None

    def mock_decrypt_token(token_view):
        return refresh_token_datas

    monkeypatch.setattr(
        "app.services.auth_service.decrypt_token",
        mock_decrypt_token
    )

    monkeypatch.setattr(
        UserRepo,
        "get_by_id",
        mock_get_user_by_id
    )

    with pytest.raises(HTTPException) as exc:
        refresh_token(token_view, db_session)

    assert exc.value.status_code == 403



def test_refresh_token_bad_type(monkeypatch, db_session, token_view, refresh_token_datas):
    refresh_token_datas.typ = "bearer"

    def mock_get_user_by_id(self, user_id, db_session):
        return User()
        

    def mock_decrypt_token(token_view):
        return refresh_token_datas

    monkeypatch.setattr(
        "app.services.auth_service.decrypt_token",
        mock_decrypt_token
    )

    monkeypatch.setattr(
        UserRepo,
        "get_by_id",
        mock_get_user_by_id
    )

    with pytest.raises(HTTPException) as exc:
        refresh_token(token_view, db_session)

    assert exc.value.status_code == 401


def test_refresh_token_non_already_used_refresh_token(monkeypatch, db_session, token_view, refresh_token_datas):
    def mock_get_user_by_id(self, user_id, db_session):
        return User()

    def mock_decrypt_token(token_view):
        return refresh_token_datas

    def mock_recuperer_par_utilisateur_et_identifiant(self, user_id, db_session):
        return UsedToken()
    
    monkeypatch.setattr(
        "app.services.auth_service.decrypt_token",
        mock_decrypt_token
    )

    monkeypatch.setattr(
        UserRepo,
        "get_by_id",
        mock_get_user_by_id
    )

    monkeypatch.setattr(
        "app.services.auth_service.refresh_token_repo.recuperer_par_utilisateur_et_identifiant",
        mock_recuperer_par_utilisateur_et_identifiant
    )
    

    with pytest.raises(HTTPException) as exc:
        refresh_token(token_view, db_session)

    assert exc.value.status_code == 403


def test_refresh_token_sucess(monkeypatch, db_session, token_view, refresh_token_datas, valid_token_created):
    def mock_get_user_by_id(self, user_id, db_session):
        return User()

    def mock_decrypt_token(token_view):
        return refresh_token_datas

    def mock_recuperer_par_utilisateur_et_identifiant(self, user_id, db_session):
        return None
    
    def mock_create_refresh_and_access_tokens(user_id, user_role):
        return valid_token_created 
    
    monkeypatch.setattr(
        "app.services.auth_service.decrypt_token",
        mock_decrypt_token
    )

    monkeypatch.setattr(
        UserRepo,
        "get_by_id",
        mock_get_user_by_id
    )

    def mock_ajouter_refresh_token_repo(t, db_session):
        return UsedToken()

    monkeypatch.setattr(
        "app.services.auth_service.refresh_token_repo.recuperer_par_utilisateur_et_identifiant",
        mock_recuperer_par_utilisateur_et_identifiant
    )

    monkeypatch.setattr(
        "app.services.auth_service.create_refresh_and_access_tokens",
        mock_create_refresh_and_access_tokens
    )

    monkeypatch.setattr(
        "app.services.auth_service.refresh_token_repo.ajouter",
        mock_ajouter_refresh_token_repo
    )
    

    refresh_token(token_view, db_session)


# validate token

def test_validate_token_success(
    monkeypatch,
    db_session,
    token_view,
    token_datas
):
    
    def mock_get_user_by_id(self, user_id, db_session):
        return User()
    
    monkeypatch.setattr(
        UserRepo,
        "get_by_id",
        mock_get_user_by_id
    )
    monkeypatch.setattr(
        "app.services.auth_service.decrypt_token",
        lambda token: token_datas
    )

    result = validate_token(token_view, db_session)

    assert result == token_datas


def test_validate_token_expired(
    monkeypatch,
    db_session,
    token_view,
    token_datas
):
    
    token_datas.exp = int((datetime.now() - timedelta(minutes=5)).timestamp())
    def mock_get_user_by_id(self, user_id, db_session):
        return User()
    
    monkeypatch.setattr(
        UserRepo,
        "get_by_id",
        mock_get_user_by_id
    )
    monkeypatch.setattr(
        "app.services.auth_service.decrypt_token",
        lambda token: token_datas
    )

    with pytest.raises(HTTPException) as exc:
        validate_token(token_view, db_session)
    
    assert exc.value.status_code == 400

def test_validate_token_user_not_found(
    monkeypatch,
    db_session,
    token_view,
    token_datas
):
    def mock_get_user_by_id(self, user_id, db_session):
        return None
    
    monkeypatch.setattr(
        UserRepo,
        "get_by_id",
        mock_get_user_by_id
    )
    monkeypatch.setattr(
        "app.services.auth_service.decrypt_token",
        lambda token: token_datas
    )

    with pytest.raises(HTTPException) as exc:
        validate_token(token_view, db_session)
    
    assert exc.value.status_code == 400