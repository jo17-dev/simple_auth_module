import pytest


from app.services.repositories.used_token import TokenRepository
from app.services.exceptions.token_exception import TokenException

def test_add_user_success(db_session, used_token):
    repo = TokenRepository()

    repo.ajouter(used_token, db_session)

    assert used_token.id is not None
    assert used_token.identifier is not None
    assert used_token.user_id == 23
    assert used_token.content == "real.token.hahah"

def test_add_user_failed(db_session, used_token, monkeypatch):
    repo = TokenRepository()

    # mocking commit to raise error
    def mock_commit():
        raise Exception("DB error")

    monkeypatch.setattr(db_session, "commit", mock_commit)

    with pytest.raises(TokenException):
        repo.ajouter(used_token, db_session)