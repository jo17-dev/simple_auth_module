import pytest
from app.services.repositories.users import UserRepo
from app.services.exceptions.user_exception import UserException


def test_add_user_success(db_session, user):
    repo = UserRepo()

    result = repo.add(user, db_session)

    assert result.id is not None
    assert result.email == "test@test.com"


def test_add_user_exception(db_session, user, monkeypatch):
    repo = UserRepo()

    def mock_commit():
        raise Exception("DB error")

    monkeypatch.setattr(db_session, "commit", mock_commit)

    with pytest.raises(UserException):
        repo.add(user, db_session)


def test_get_by_id_found(db_session, user):
    repo = UserRepo()
    created_user = repo.add(user, db_session)

    result = repo.get_by_id(created_user.id, db_session)

    assert result is not None
    assert result.id == created_user.id


def test_get_by_id_not_found(db_session):
    repo = UserRepo()

    result = repo.get_by_id(999, db_session)

    assert result is None


def test_get_by_email_found(db_session, user):
    repo = UserRepo()
    repo.add(user, db_session)

    result = repo.get_by_email("test@test.com", db_session)

    assert result is not None
    assert result.email == "test@test.com"


def test_get_by_email_not_found(db_session):
    repo = UserRepo()

    result = repo.get_by_email("unknown@test.com", db_session)

    assert result is None


def test_delete_user_success(db_session, user):
    repo = UserRepo()
    created_user = repo.add(user, db_session)

    repo.delete(created_user.id, db_session)

    deleted_user = repo.get_by_id(created_user.id, db_session)
    assert deleted_user is None


def test_delete_user_exception(db_session, monkeypatch):
    repo = UserRepo()

    def mock_commit():
        raise Exception("DB delete error")

    monkeypatch.setattr(db_session, "commit", mock_commit)

    with pytest.raises(UserException):
        repo.delete(1, db_session)
