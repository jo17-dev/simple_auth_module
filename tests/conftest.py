import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.services.model  import User, Role
from app.services.model  import UsedToken
from app.data.database import Base
from datetime import datetime, timedelta
from app.interface.view_models.token  import TokenDatas, TokenView, TokenCreated
from app.interface.view_models.user  import UserCreation


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine)

    Base.metadata.create_all(engine)
    session = TestingSessionLocal()

    insert_roles_sql = text("INSERT INTO roles (title) VALUES ('USER'), ('MANAGER'), ('ADMIN')")
    session.execute(insert_roles_sql)
    session.commit()

    yield session

    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture
def user():
    return User(
        email="test@test.com",
        password="hashed_password_hahahaha"
    )

@pytest.fixture
def used_token():
    return UsedToken(
        content = "real.token.hahah",
        user_id = 23
    )

@pytest.fixture
def token_datas():
    return TokenDatas(uid="1", typ="bearer", role="admin", exp=int((datetime.now() + timedelta(minutes=5)).timestamp()), id_token=None)

@pytest.fixture
def refresh_token_datas():
    return TokenDatas(uid="1", typ="refresh", role=None, exp=int((datetime.now() + timedelta(minutes=5)).timestamp()), id_token="refresh123")

@pytest.fixture
def valid_user_creation():
    return UserCreation(
        email="test@example.com",
        password="Password1",
        roles=["user"]
    )

@pytest.fixture
def valid_user_role():
    return Role(id=1, title="USER")

@pytest.fixture
def token_view():
    return TokenView(token="fake-refresh-token")

@pytest.fixture
def valid_token_created():
    return TokenCreated(
        access_token="template.access.token",
        refresh_token="why.areyou.readingthis"
    )