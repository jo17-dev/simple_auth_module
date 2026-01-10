import pytest
from fastapi import HTTPException
from app.services.model import User
from app.services.repositories.users import UserRepo
from app.services.repositories.roles import RoleRepo
from app.interface.view_models.user import UserCreated

from app.services.users_service import add_user

def test_add_user_invalid_email_and_password(db_session, valid_user_creation):
    valid_user_creation.email = "invalid"
    valid_user_creation.password = "123"

    with pytest.raises(HTTPException) as exc:
        add_user(valid_user_creation, db_session)

    assert exc.value.status_code == 400


def test_add_user_invalid_email(db_session, valid_user_creation):
    valid_user_creation.email = "invalid-email"

    with pytest.raises(HTTPException) as exc:
        add_user(valid_user_creation, db_session)

    assert exc.value.status_code == 400


def test_add_user_invalid_password(db_session, valid_user_creation):
    valid_user_creation.password = "password"

    with pytest.raises(HTTPException) as exc:
        add_user(valid_user_creation, db_session)

    assert exc.value.status_code == 400


def test_add_user_email_already_exists(
    monkeypatch,
    db_session,
    valid_user_creation
):
    def mocked_get_by_email(self, email, db):
        return User()

    monkeypatch.setattr(
        UserRepo,
        "get_by_email",
        mocked_get_by_email
    )

    with pytest.raises(HTTPException) as exc:
        add_user(valid_user_creation, db_session)

    assert exc.value.status_code == 400


def test_add_user_role_not_found(
    monkeypatch,
    db_session,
    valid_user_creation
):
    
    def mock_get_user_by_email(self, email, db):
        return None
    
    def mock_get_role_by_name(self, name, db):
        return None

    monkeypatch.setattr(
        UserRepo,
        "get_by_email",
        mock_get_user_by_email
    )

    monkeypatch.setattr(
        RoleRepo,
        "get_by_name",
        mock_get_role_by_name
    )

    with pytest.raises(HTTPException) as exc:
        add_user(valid_user_creation, db_session)

    assert exc.value.status_code == 400


def test_add_user_success(monkeypatch, valid_user_role ,valid_user_creation, db_session):

    def mock_get_user_by_email(self, email, db):
        return None
    
    def mock_add_user_repo(self, user_to_add, db):
        return User(id=21, email=user_to_add.email, roles = [valid_user_role])
    
    def mock_get_role_by_name(self, name, db):
        return valid_user_role
    

    monkeypatch.setattr(
        UserRepo,
        "get_by_email",
        mock_get_user_by_email
    )

    monkeypatch.setattr(
        UserRepo,
        "add",
        mock_add_user_repo
    )

    monkeypatch.setattr(
        RoleRepo,
        "get_by_name",
        mock_get_role_by_name
    )

    created_user = add_user(valid_user_creation, db_session)

    assert isinstance(created_user, UserCreated)
    assert created_user.email == valid_user_creation.email
    assert created_user.roles == valid_user_creation.roles


