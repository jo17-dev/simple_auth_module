import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.services.model  import User
from app.services.model  import UsedToken
from app.data.database import Base


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine)

    Base.metadata.create_all(engine)
    session = TestingSessionLocal()

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